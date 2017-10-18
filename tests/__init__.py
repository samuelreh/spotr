import random
import sys
import time

from botocore.compat import six
from six import add_move, MovedModule

# The unittest module got a significant overhaul
# in 2.7, so if we're in 2.6 we can use the backported
# version unittest2.
if sys.version_info[:2] == (2, 6):
    import unittest2 as unittest
else:
    import unittest


add_move(MovedModule('mock', 'mock', 'unittest.mock'))

# In python 3, order matters when calling assertEqual to
# compare lists and dictionaries with lists. Therefore,
# assertItemsEqual needs to be used but it is renamed to
# assertCountEqual in python 3.
if six.PY2:
    unittest.TestCase.assertCountEqual = unittest.TestCase.assertItemsEqual


class BaseTestCase(unittest.TestCase):
    """
    A base test case which mocks out the low-level session to prevent
    any actual calls to Botocore.
    """

    def setUp(self):
        self.bc_session_patch = mock.patch('botocore.session.Session')
        self.bc_session_cls = self.bc_session_patch.start()

        loader = self.bc_session_cls.return_value.get_component.return_value
        loader.data_path = ''
        self.loader = loader

        # We also need to patch the global default session.
        # Otherwise it could be a cached real session came from previous
        # "functional" or "integration" tests.
        patch_global_session = mock.patch('boto3.DEFAULT_SESSION')
        patch_global_session.start()
        self.addCleanup(patch_global_session.stop)

    def tearDown(self):
        self.bc_session_patch.stop()
