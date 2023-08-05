import unittest
from PyQt5 import QtCore
from appteka.pyqt import testing
from appteka.pyqtgraph.waveform import Waveform


class TestWaveform(unittest.TestCase):
    """Test suite for Waveform widget."""
    def test_xlabel(self):
        app = testing.TestApp(self)

        w = Waveform(xlabel="Time [sec]")

        app(w, [
            "x label is 'Time [sec]'",
        ])

    def test_time_axis_false(self):
        app = testing.TestApp(self)

        w = Waveform(time_axis=False)
        w.update_data([0, 1, 2, 3], [1, 2, 1, 2])

        app(w, [
            "x values are usual numbers from 0 to 3",
        ])

    def test_time_axis_true(self):
        app = testing.TestApp(self)

        w = Waveform(None, time_axis=True)
        w.update_data([0, 1, 2, 3], [1, 2, 1, 2])

        app(w, [
            "x values are time values",
        ])

    def test_scaling(self):
        app = testing.TestApp(self)

        w = Waveform()
        w.update_data([0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                      [1, 2, 0, 3, 1, 2, 3, 4, 1, 3])

        app(w, [
            "both axis scaling with mouse wheel",
            "x-scaling with CONTROL pressed",
            "y-scaling with SHIFT pressed",
        ])


class TestWaveform_Animation(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0

    def test_it(self):
        app = testing.TestApp(self)

        w = Waveform()

        def rotate():
            ts = [self.counter+i for i in range(10)]
            xs = [t for t in ts]
            w.update_data(ts, xs)
            self.counter = self.counter + 1

        timer = QtCore.QTimer()
        timer.setInterval(500)
        timer.timeout.connect(rotate)
        self.counter = 0
        timer.start()

        app(w, [
            "x values grow",
            "y values grow",
        ])
