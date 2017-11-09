# @guimatsumoto
# @jesussanchez
#
# First implementation of a word2vec algorithm, on a skip-gram model.
#

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import math
import os
import random
from tempfile import gettempdir
import zipfile

import numpy as np
import tensorflow as tf
from six.moves import urllib
from six.moves import xrange

url = 'http://mattmahoney.net/dc/'

def download_if_not_present(filename, expected_bytes):
        local_filename = os.path.join()