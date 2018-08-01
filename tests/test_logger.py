from unittest import TestCase
from mock import MagicMock
import logging
from freezegun import freeze_time
from io import StringIO
import sys
from icloudpd.logger import setup_logger, iCloudPDLogger

class LoggerTestCase(TestCase):
    # Tests the formatter that is set up in setup_logger()
    @freeze_time("2018-01-01 00:00")
    def test_logger_output(self):
        logger = setup_logger()
        test_logger = logging.getLogger('icloudpd-test')
        string_io = StringIO()
        string_handler = logging.StreamHandler(stream=string_io)
        string_handler.setFormatter(logger.handlers[0].formatter)
        test_logger.addHandler(string_handler)
        test_logger.setLevel(logging.DEBUG)
        test_logger.info(u'Test info output')
        test_logger.debug(u'Test debug output')
        test_logger.error(u'Test error output')
        output = string_io.getvalue().strip()
        self.assertIn('2018-01-01', output)
        self.assertIn('INFO     Test info output', output)
        self.assertIn('DEBUG    Test debug output', output)
        self.assertIn('ERROR    Test error output', output)

    def test_logger_tqdm_fallback(self):
        logging.setLoggerClass(iCloudPDLogger)
        logger = logging.getLogger('icloudpd-test')
        logger.info = MagicMock()
        logger.set_tqdm_description('foo')
        logger.info.assert_called_once_with('foo')

        logger.log = MagicMock()
        logger.tqdm_write('foo')
        logger.log.assert_called_once_with(logging.INFO, 'foo')

        logger.set_tqdm(MagicMock())
        logger.tqdm.write = MagicMock()
        logger.tqdm.set_description = MagicMock()
        logger.set_tqdm_description('bar')
        logger.tqdm.set_description.assert_called_once_with('bar')
        logger.tqdm_write('bar')
        logger.tqdm.write.assert_called_once_with('bar')
