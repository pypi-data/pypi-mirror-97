import unittest
import math
from PyQt5 import QtCore
from appteka.pyqt import testing
from appteka.pyqtgraph import phasor


class TestPhasor(unittest.TestCase):
    def test_just_visible(self):
        app = testing.TestApp(self)
        app(phasor.PhasorDiagram(), [
            "Widget seems to be OK",
        ])

    def test_range_is_two(self):
        app = testing.TestApp(self)
        d = phasor.PhasorDiagram()
        d.set_range(2)

        app(d, [
            "Grid is OK",
            "The max circle in grid has radius of 2",
        ])

    def test_change_range(self):
        app = testing.TestApp(self)
        d = phasor.PhasorDiagram()
        d.set_range(2)
        d.set_range(4)
        app(d, [
            "Grid is OK",
            "The max circle in grid has radius of 4",
        ])

    def test_add_phasor(self):
        app = testing.TestApp(self)
        d = phasor.PhasorDiagram()
        d.set_range(100)
        d.add_phasor('ph-1', 80, 1)

        app(d, [
            "There is a phasor in first quadrant",
            "The color of phasor is white",
        ])

    def test_update_phasor(self):
        app = testing.TestApp(self)
        d = phasor.PhasorDiagram()
        d.set_range(100)
        d.add_phasor('ph-1', 80, 1)
        d.update_phasor('ph-1', 80, 2)

        app(d, [
            "There is a phasor in second quadrant",
            "Phasor in single",
        ])

    def test_phasor_color(self):
        app = testing.TestApp(self)
        d = phasor.PhasorDiagram()
        d.set_range(100)
        d.add_phasor('ph-1', 80, 1, (255, 0, 0))

        app(d, [
            "There is a red phasor in first quadrant",
        ])

    def test_phasor_end_circle(self):
        app = testing.TestApp(self)
        color = (255, 0, 0)
        d = phasor.PhasorDiagram()
        d.set_range(100)
        d.add_phasor('ph-1', 80, 0 + math.pi/10, color)
        d.add_phasor('ph-2', 80, math.pi/2 + math.pi/10, color)
        d.add_phasor('ph-3', 80, math.pi + math.pi/10, color)
        d.add_phasor('ph-4', 80, 3 * math.pi / 2 + math.pi/10, color)
        app(d, ["Ends of the phasors are circles"])

    def test_phasor_end_arrow(self):
        app = testing.TestApp(self)
        color = (0, 255, 0)
        d = phasor.PhasorDiagram(end='arrow')
        d.set_range(100)
        d.add_phasor('ph-1', 80, 0 + math.pi/10, color)
        d.add_phasor('ph-2', 80, math.pi/2 + math.pi/10, color)
        d.add_phasor('ph-3', 80, math.pi + math.pi/10, color)
        d.add_phasor('ph-4', 80, 3 * math.pi / 2 + math.pi/10, color)
        app(d, ["Ends of the phasors are arrows"])

    def test_phasor_end_unknown(self):
        testing.TestApp(self)
        raised = False
        try:
            phasor.PhasorDiagram(end='wrong')
        except ValueError:
            raised = True

        self.assertTrue(raised)

    def test_phasor_end_arrow_clear(self):
        app = testing.TestApp(self)
        d = phasor.PhasorDiagram(end='arrow')
        d.set_range(100)
        d.add_phasor('ph-1', 80, 0, (0, 255, 0))
        d.remove_phasors()
        app(d, ["Only grid"])

    def test_three_phasors(self):
        app = testing.TestApp(self)
        d = phasor.PhasorDiagram(end='arrow')
        d.set_range(100)
        d.add_phasor('ph-1', 80, 0, (255, 0, 0))
        d.add_phasor('ph-2', 80, 2 * 3.1415 / 3, (0, 255, 0))
        d.add_phasor('ph-3', 80, -2 * 3.1415 / 3, (0, 0, 255))

        app(d, [
            "There are 3 phasors: red, green and blue",
            "About 120 degrees between phasors",
        ])

    def test_three_phasors_rotated(self):
        app = testing.TestApp(self)

        d = phasor.PhasorDiagram()
        d.set_range(100)
        d.add_phasor('ph-1', 80, 0, (255, 0, 0))
        d.add_phasor('ph-2', 80, 2 * 3.1415 / 3, (0, 255, 0))
        d.add_phasor('ph-3', 80, -2 * 3.1415 / 3, (0, 0, 255))
        d.update_phasor('ph-1', 80, 1)
        d.update_phasor('ph-2', 80, 1 + 2 * 3.1415 / 3)
        d.update_phasor('ph-3', 80, 1 - 2 * 3.1415 / 3)

        app(d, [
            "There are 3 phasors: red, green and blue",
            "About 120 degrees between phasors",
            "Red phasor has angle about 1 radian",
        ])

    def test_range_to_phasor(self):
        app = testing.TestApp(self)

        d = phasor.PhasorDiagram()
        d.add_phasor('ph-1', color=(255, 255, 0))
        d.update_phasor('ph-1', 1, 1)
        d.update_phasor('ph-1', 100, 1)
        d.set_range(100)

        app(d, ["Grid corresponds to phasor"])

    def test_legend(self):
        app = testing.TestApp(self)

        d = phasor.PhasorDiagram()
        d.add_phasor('ph-1', 80, 0, (255, 0, 0))
        d.add_phasor('ph-2', 80, 2 * 3.1415 / 3, (0, 255, 0))
        d.add_phasor('ph-3', 80, -2 * 3.1415 / 3, (0, 0, 255))
        d.show_legend()
        d.set_range(80)

        app(d, [
            "Legend is correct",
        ])

    def test_width_of_phasors(self):
        app = testing.TestApp(self)

        # Given phasor diagram
        d = phasor.PhasorDiagram()

        # When add two phasors
        # And widths of phasors are set to be significantly differ
        d.add_phasor('ph-1', color=(255, 255, 255), width=1)
        d.add_phasor('ph-2', color=(255, 255, 255), width=4)
        d.update_phasor('ph-1', 100, 1)
        d.update_phasor('ph-2', 100, 2)
        d.set_range(100)

        # Then widths of phasors are differ
        app(d, [
            "widths of phasors are differ",
        ])


class TestPhasor_Animation(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0

    def test_three_phasors_animation(self):
        app = testing.TestApp(self)

        d = phasor.PhasorDiagram(end='arrow')
        d.add_phasor('ph-1', color=(255, 0, 0))
        d.add_phasor('ph-2', color=(0, 255, 0))
        d.add_phasor('ph-3', color=(0, 0, 255))
        d.show_legend()

        def rotate():
            a = 2 * 3.1415 / 3
            sh = self.counter / 200
            ash = self.counter / 10
            d.update_phasor('ph-1', ash + 10, sh)
            d.update_phasor('ph-2', 10, sh + a)
            d.update_phasor('ph-3', 10, sh - a)
            d.set_range(ash + 10)
            self.counter = self.counter + 1

        timer = QtCore.QTimer()
        timer.setInterval(10)
        timer.timeout.connect(rotate)
        self.counter = 0
        timer.start()

        app(d, [
            "Phasors smoothly rotating",
            "Amplitude of red phasor grows",
        ])
