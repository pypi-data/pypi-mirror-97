import unittest
from appteka.pyqt import testing
from appteka.pyqtgraph.waveform import MultiWaveform


class TestMultiWavefrom(unittest.TestCase):
    """MultiWavefrom."""
    def test_top_axis(self):
        """Switch on top axis."""
        app = testing.TestApp(self)

        w = MultiWaveform()

        w.add_plot('a', title='plot A')

        app(w, [
            "There is top axis",
        ])

    def test_scaling(self):
        """Scaling with keys CONTROL and SHIFT."""
        app = testing.TestApp(self)

        w = MultiWaveform()

        w.add_plot('a', title='plot A')
        w.update_data('a',
                      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                      [1, 2, 0, 3, 1, 2, 3, 4, 1, 3])

        w.add_plot('b', title='plot B')
        w.update_data('b',
                      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                      [2, 1, 1, 1, 4, 6, 2, 3, 4, 3])

        app(w, [
            "both axis scaling with mouse wheel",
            "x-scaling with CONTROL pressed",
            "y-scaling with SHIFT pressed",
        ])

    def test_set_title(self):
        """Change title of given plot."""
        app = testing.TestApp(self)

        w = MultiWaveform()
        w.add_plot('a', title='Title one')
        w.update_data('a', [0, 1, 2, 3], [1, 2, 1, 2])
        w.set_title(plot_key='a', value='Frequency: 50.123')

        app(w, ["Title is 'Frequency: 50.123'"])

    def test_color(self):
        app = testing.TestApp(self)

        w = MultiWaveform()
        w.add_plot('a')
        w.set_plots_color((255, 0, 0))
        w.update_data('a', [0, 1, 2, 3], [1, 2, 1, 2])

        app(w, ["Red plot"])
