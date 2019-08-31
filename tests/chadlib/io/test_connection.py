from unittest.mock  import MagicMock
from unittest       import TestCase

from chadlib.io     import Connection


class TestConnection(TestCase):

    def setUp(self):
        self.connection = Connection(MagicMock(), MagicMock(), MagicMock())

    def tearDown(self):
        self.connection.close()
