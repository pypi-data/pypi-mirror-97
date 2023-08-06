import unittest
from time import sleep
import os
from appteka.io import QueuedWriter


TMP_FILE_NAME = "tmp.txt"


def convert_func(sample):
    """Convert function."""
    return '{}: {}\n'.format(*sample)


class TestQueuedWriter(unittest.TestCase):
    def test_on_timer(self):
        writer = QueuedWriter(write_on='time')
        writer.set_convert_func(convert_func)
        buf = open(TMP_FILE_NAME, 'w')
        writer.set_buff(buf)
        writer.start_thread()

        i = 0
        while i < 150:
            sample = (i, i*2)
            writer.add_data(sample)
            sleep(0.01)
            i += 1

        writer.stop_thread()
        buf.close()
        os.remove(TMP_FILE_NAME)

    def test_on_data(self):
        writer = QueuedWriter(write_on='data')
        writer.set_convert_func(convert_func)
        buf = open(TMP_FILE_NAME, 'w')
        writer.set_buff(buf)
        writer.start_thread()

        i = 0
        while i < 150:
            sample = (i, i*2)
            writer.add_data(sample)
            sleep(0.01)
            i += 1

        writer.stop_thread()
        buf.close()
        os.remove(TMP_FILE_NAME)

    def test_wront_write_on(self):
        with self.assertRaises(RuntimeError):
            QueuedWriter(write_on='dollar fault')
