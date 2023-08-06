import logging
import unittest


enabled = False


class LoggedTests(unittest.TestCase):
    def setUp(self):
        self._logger = logging.getLogger(__name__)
        if enabled:
            logging.basicConfig(level=logging.DEBUG)
            print()
            self._logger.info(
                "--- Testing %s.%s ---",
                self.__class__.__name__,
                self._testMethodName)
