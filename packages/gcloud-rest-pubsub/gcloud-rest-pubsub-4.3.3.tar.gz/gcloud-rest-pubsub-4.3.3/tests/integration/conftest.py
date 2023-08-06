from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from future import standard_library
standard_library.install_aliases()
import os

import pytest


@pytest.fixture(scope='module')  # type: ignore
def creds()       :
    # TODO: bundle public creds into this repo
    return os.environ['GOOGLE_APPLICATION_CREDENTIALS']


@pytest.fixture(scope='module')  # type: ignore
def project()       :
    return 'dialpad-oss'


@pytest.fixture(scope='module')  # type: ignore
def subscription_name()       :
    return 'public_test'


@pytest.fixture(scope='module')  # type: ignore
def topic_name()       :
    return 'public_test'
