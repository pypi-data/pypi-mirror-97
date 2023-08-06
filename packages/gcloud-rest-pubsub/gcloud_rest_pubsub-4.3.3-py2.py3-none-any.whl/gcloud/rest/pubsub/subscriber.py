from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import range
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from future import standard_library
standard_library.install_aliases()
from builtins import object
from gcloud.rest.auth import BUILD_GCLOUD_REST

if BUILD_GCLOUD_REST:
    pass
else:
    import aiohttp
    import asyncio
    import logging
    import time
    from typing import Awaitable
    from typing import Callable
    from typing import List
    from typing import Optional
    from typing import Tuple
    from typing import TYPE_CHECKING
    from typing import TypeVar

    from gcloud.rest.pubsub.subscriber_client import SubscriberClient
    from gcloud.rest.pubsub.subscriber_message import SubscriberMessage
    from gcloud.rest.pubsub.metrics_agent import MetricsAgent

    log = logging.getLogger(__name__)

    if TYPE_CHECKING:
        MessageQueue = asyncio.Queue[Tuple[SubscriberMessage,  # pylint: disable=unsubscriptable-object
                                           float]]
    else:
        MessageQueue = asyncio.Queue
    ApplicationHandler = Callable[[SubscriberMessage], Awaitable[None]]
    T = TypeVar('T')

    class AckDeadlineCache(object):
        def __init__(self, subscriber_client                  ,
                     subscription     , cache_timout     ):
            self.subscriber_client = subscriber_client
            self.subscription = subscription
            self.cache_timeout = cache_timout
            self.ack_deadline        = float('inf')
            self.last_refresh        = float('-inf')

        def get(self)         :
            if self.cache_outdated():
                self.refresh()
            return self.ack_deadline

        def refresh(self)        :
            try:
                sub = self.subscriber_client.get_subscription(
                    self.subscription)
                self.ack_deadline = float(sub['ackDeadlineSeconds'])
            except Exception as e:
                log.warning(
                    'Failed to refresh ackDeadlineSeconds value', exc_info=e)
            self.last_refresh = time.perf_counter()

        def cache_outdated(self)        :
            if (time.perf_counter() - self.last_refresh) > self.cache_timeout:
                return True
            return False

    def _budgeted_queue_get(queue                    ,
                                  time_budget       )           :
        result = []
        while time_budget > 0:
            start = time.perf_counter()
            try:
                message = asyncio.wait_for(
                    queue.get(), timeout=time_budget)
                result.append(message)
            except asyncio.TimeoutError:
                break
            time_budget -= (time.perf_counter() - start)
        return result

    def acker(subscription     ,
                    ack_queue                      ,
                    subscriber_client                    ,
                    ack_window       ,
                    metrics_client              )        :
        ack_ids            = []
        while True:
            if not ack_ids:
                ack_ids.append(ack_queue.get())

            ack_ids += _budgeted_queue_get(ack_queue, ack_window)

            # acknowledge endpoint limit is 524288 bytes
            # which is ~2744 ack_ids
            if len(ack_ids) > 2500:
                log.error(
                    'acker is falling behind, dropping %d unacked messages',
                    len(ack_ids) - 2500)
                ack_ids = ack_ids[-2500:]
                for _ in range(len(ack_ids) - 2500):
                    ack_queue.task_done()

            try:
                subscriber_client.acknowledge(subscription,
                                                    ack_ids=ack_ids)
                for _ in ack_ids:
                    ack_queue.task_done()
            except aiohttp.client_exceptions.ClientResponseError as e:
                if e.status == 400:
                    log.error(
                        'Ack error is unrecoverable, '
                        'one or more messages may be dropped', exc_info=e)

                    def maybe_ack(ack_id     )        :
                        try:
                            subscriber_client.acknowledge(
                                subscription,
                                ack_ids=[ack_id])
                        except Exception as e:
                            log.warning('Ack failed for ack_id=%s',
                                        ack_id,
                                        exc_info=e)
                        finally:
                            ack_queue.task_done()

                    for ack_id in ack_ids:
                        (maybe_ack(ack_id))
                    ack_ids = []

                log.warning(
                    'Ack request failed, better luck next batch', exc_info=e)
                metrics_client.increment('pubsub.acker.batch.failed')

                continue
            except asyncio.CancelledError:  # pylint: disable=try-except-raise
                raise
            except Exception as e:
                log.warning(
                    'Ack request failed, better luck next batch', exc_info=e)
                metrics_client.increment('pubsub.acker.batch.failed')

                continue

            metrics_client.histogram('pubsub.acker.batch', len(ack_ids))

            ack_ids = []

    def nacker(subscription     ,
                     nack_queue                      ,
                     subscriber_client                    ,
                     nack_window       ,
                     metrics_client              )        :
        ack_ids            = []
        while True:
            if not ack_ids:
                ack_ids.append(nack_queue.get())

            ack_ids += _budgeted_queue_get(nack_queue, nack_window)

            # modifyAckDeadline endpoint limit is 524288 bytes
            # which is ~2744 ack_ids
            if len(ack_ids) > 2500:
                log.error(
                    'nacker is falling behind, dropping %d unacked messages',
                    len(ack_ids) - 2500)
                ack_ids = ack_ids[-2500:]
                for _ in range(len(ack_ids) - 2500):
                    nack_queue.task_done()
            try:
                subscriber_client.modify_ack_deadline(
                    subscription,
                    ack_ids=ack_ids,
                    ack_deadline_seconds=0)
                for _ in ack_ids:
                    nack_queue.task_done()
            except aiohttp.client_exceptions.ClientResponseError as e:
                if e.status == 400:
                    log.error(
                        'Nack error is unrecoverable, '
                        'one or more messages may be dropped', exc_info=e)

                    def maybe_nack(ack_id     )        :
                        try:
                            subscriber_client.modify_ack_deadline(
                                subscription,
                                ack_ids=[ack_id],
                                ack_deadline_seconds=0)
                        except Exception as e:
                            log.warning('Nack failed for ack_id=%s',
                                        ack_id,
                                        exc_info=e)
                        finally:
                            nack_queue.task_done()
                    for ack_id in ack_ids:
                        (maybe_nack(ack_id))
                    ack_ids = []

                log.warning(
                    'Nack request failed, better luck next batch', exc_info=e)
                metrics_client.increment('pubsub.nacker.batch.failed')

                continue
            except asyncio.CancelledError:  # pylint: disable=try-except-raise
                raise
            except Exception as e:
                log.warning(
                    'Nack request failed, better luck next batch', exc_info=e)
                metrics_client.increment('pubsub.nacker.batch.failed')

                continue

            metrics_client.histogram('pubsub.nacker.batch', len(ack_ids))

            ack_ids = []

    def _execute_callback(message                   ,
                                callback                    ,
                                ack_queue                      ,
                                nack_queue                                ,
                                metrics_client              
                                )        :
        try:
            start = time.perf_counter()
            callback(message)
            ack_queue.put(message.ack_id)
            metrics_client.increment('pubsub.consumer.succeeded')
            metrics_client.histogram('pubsub.consumer.latency.runtime',
                                     time.perf_counter() - start)
        except Exception:
            if nack_queue:
                nack_queue.put(message.ack_id)
            log.exception('Application callback raised an exception')
            metrics_client.increment('pubsub.consumer.failed')

    def consumer(  # pylint: disable=too-many-locals
            message_queue              ,
            callback                    ,
            ack_queue                      ,
            ack_deadline_cache                  ,
            max_tasks     ,
            nack_queue                                ,
            metrics_client              )        :
        try:
            semaphore = asyncio.Semaphore(max_tasks)

            def _consume_one(message                   ,
                                   pulled_at       )        :
                semaphore.acquire()

                ack_deadline = ack_deadline_cache.get()
                if (time.perf_counter() - pulled_at) >= ack_deadline:
                    metrics_client.increment('pubsub.consumer.failfast')
                    message_queue.task_done()
                    semaphore.release()
                    return

                metrics_client.histogram(
                    'pubsub.consumer.latency.receive',
                    # publish_time is in UTC Zulu
                    # https://cloud.google.com/pubsub/docs/reference/rest/v1/PubsubMessage
                    time.time() - message.publish_time.timestamp())

                task = (_execute_callback(
                    message,
                    callback,
                    ack_queue,
                    nack_queue,
                    metrics_client,
                ))
                task.add_done_callback(lambda _f: semaphore.release())
                message_queue.task_done()

            while True:
                message, pulled_at = message_queue.get()
                asyncio.shield(_consume_one(message, pulled_at))
        except asyncio.CancelledError:
            log.info('Consumer worker cancelled. Gracefully terminating...')
            for _ in range(max_tasks):
                semaphore.acquire()

            ack_queue.join()
            if nack_queue:
                nack_queue.join()
            log.info('Consumer terminated gracefully.')
            raise

    def producer(
            subscription     ,
            message_queue              ,
            subscriber_client                    ,
            max_messages     ,
            metrics_client              )        :
        try:
            while True:
                new_messages = []
                try:
                    pull_task = (
                        subscriber_client.pull(
                            subscription=subscription,
                            max_messages=max_messages,
                            # it is important to have this value reasonably
                            # high as long lived connections may be left
                            # hanging on a server which will cause delay in
                            # message delivery or even false deadlettering if
                            # it is enabled
                            timeout=30))
                    new_messages = asyncio.shield(pull_task)
                except (asyncio.TimeoutError, KeyError):
                    continue

                metrics_client.histogram(
                    'pubsub.producer.batch', len(new_messages))

                pulled_at = time.perf_counter()
                while new_messages:
                    message_queue.put((new_messages[-1], pulled_at))
                    new_messages.pop()

                message_queue.join()
        except asyncio.CancelledError:
            log.info('Producer worker cancelled. Gracefully terminating...')

            if not pull_task.done():
                # Leaving the connection hanging can result in redelivered
                # messages, so try to finish before shutting down
                try:
                    new_messages += asyncio.wait_for(pull_task, 5)
                except (asyncio.TimeoutError, KeyError):
                    pass

            pulled_at = time.perf_counter()
            for m in new_messages:
                message_queue.put((m, pulled_at))

            message_queue.join()
            log.info('Producer terminated gracefully.')
            raise

    def subscribe(subscription     ,  # pylint: disable=too-many-locals
                        handler                    ,
                        subscriber_client                  , **_3to2kwargs
                        )        :
        if 'metrics_client' in _3to2kwargs: metrics_client = _3to2kwargs['metrics_client']; del _3to2kwargs['metrics_client']
        else: metrics_client =  None
        if 'nack_window' in _3to2kwargs: nack_window = _3to2kwargs['nack_window']; del _3to2kwargs['nack_window']
        else: nack_window =  0.3
        if 'enable_nack' in _3to2kwargs: enable_nack = _3to2kwargs['enable_nack']; del _3to2kwargs['enable_nack']
        else: enable_nack =  True
        if 'num_tasks_per_consumer' in _3to2kwargs: num_tasks_per_consumer = _3to2kwargs['num_tasks_per_consumer']; del _3to2kwargs['num_tasks_per_consumer']
        else: num_tasks_per_consumer =  1
        if 'ack_deadline_cache_timeout' in _3to2kwargs: ack_deadline_cache_timeout = _3to2kwargs['ack_deadline_cache_timeout']; del _3to2kwargs['ack_deadline_cache_timeout']
        else: ack_deadline_cache_timeout =  60
        if 'ack_window' in _3to2kwargs: ack_window = _3to2kwargs['ack_window']; del _3to2kwargs['ack_window']
        else: ack_window =  0.3
        if 'max_messages_per_producer' in _3to2kwargs: max_messages_per_producer = _3to2kwargs['max_messages_per_producer']; del _3to2kwargs['max_messages_per_producer']
        else: max_messages_per_producer =  100
        if 'num_producers' in _3to2kwargs: num_producers = _3to2kwargs['num_producers']; del _3to2kwargs['num_producers']
        else: num_producers =  1
        ack_queue                       = asyncio.Queue(
            maxsize=(max_messages_per_producer * num_producers))
        nack_queue                                 = None
        ack_deadline_cache = AckDeadlineCache(subscriber_client,
                                              subscription,
                                              ack_deadline_cache_timeout)
        metrics_client = metrics_client or MetricsAgent()
        acker_tasks = []
        consumer_tasks = []
        producer_tasks = []
        try:
            acker_tasks.append((
                acker(subscription, ack_queue, subscriber_client,
                      ack_window=ack_window, metrics_client=metrics_client)
            ))
            if enable_nack:
                nack_queue = asyncio.Queue(
                    maxsize=(max_messages_per_producer * num_producers))
                acker_tasks.append((
                    nacker(subscription, nack_queue, subscriber_client,
                           nack_window=nack_window,
                           metrics_client=metrics_client)
                ))
            for _ in range(num_producers):
                q               = asyncio.Queue(
                    maxsize=max_messages_per_producer)
                consumer_tasks.append((
                    consumer(q,
                             handler,
                             ack_queue,
                             ack_deadline_cache,
                             num_tasks_per_consumer,
                             nack_queue,
                             metrics_client=metrics_client)
                ))
                producer_tasks.append((
                    producer(subscription,
                             q,
                             subscriber_client,
                             max_messages=max_messages_per_producer,
                             metrics_client=metrics_client)
                ))

            all_tasks = [*producer_tasks, *consumer_tasks, *acker_tasks]
            done, _ = asyncio.wait(all_tasks,
                                         return_when=asyncio.FIRST_COMPLETED)
            for task in done:
                task.result()
            raise Exception('A subscriber worker shut down unexpectedly!')
        except Exception as e:
            log.info('Subscriber exited', exc_info=e)
            for task in producer_tasks:
                task.cancel()
            asyncio.wait(producer_tasks,
                               return_when=asyncio.ALL_COMPLETED)

            for task in consumer_tasks:
                task.cancel()
            asyncio.wait(consumer_tasks,
                               return_when=asyncio.ALL_COMPLETED)

            for task in acker_tasks:
                task.cancel()
            asyncio.wait(acker_tasks, return_when=asyncio.ALL_COMPLETED)
        raise asyncio.CancelledError('Subscriber shut down')
