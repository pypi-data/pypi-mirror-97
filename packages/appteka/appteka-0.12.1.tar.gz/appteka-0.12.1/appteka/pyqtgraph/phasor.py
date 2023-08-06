# appteka - helpers collection

# Copyright (C) 2018-2021 Aleksandr Popov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.

# You should have received a copy of the Lesser GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Implementation of the phasor diagram."""

from math import degrees
import cmath
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore


GRID_DEFAULT_CIRCLES_NUM = 6

ARROW_SIZE_PX = 5


class PhasorDiagram(pg.PlotWidget):
    """Widget for plotting phasor diagram.

    Parameters
    ----------
    parent: object
        Parent object
    size: int
        Size of the widget
    end: str
        Can be 'circle' or 'arrow'
    """
    def __init__(self, parent=None, size=500, end='circle'):
        super().__init__(parent)
        self.setAspectLocked(True)
        self.addLine(x=0, pen=0.2)
        self.addLine(y=0, pen=0.2)
        self.showAxis('bottom', False)
        self.showAxis('left', False)

        self.setFixedSize(size, size)

        self.__build_grid()
        self.__build_labels()

        self.set_range(1)

        self.setMouseEnabled(x=False, y=False)
        self.disableAutoRange()
        self.plotItem.setMenuEnabled(False)
        self.hideButtons()

        self.legend = None

        self.phasors = {}
        self.items = {}

        if end not in ['circle', 'arrow']:
            raise ValueError('Unknown end value: {}'.format(end))
        self.__end = end

    def set_range(self, value):
        """Set range of diagram."""
        self.__range = value
        self.__update_grid()
        self.__update_labels()

    def add_phasor(self, name, amp=0, phi=0, color=(255, 255, 255), width=1):
        """Add phasor to the diagram."""

        # add items to be painted
        if self.__end == 'circle':
            items = {
                'line': self.plot(pen=pg.mkPen(color, width=width)),
                'point': self.plot(pen=None, symbolBrush=color,
                                   symbolSize=width+3, symbolPen=None,
                                   name=name),
            }

        if self.__end == 'arrow':
            items = {
                'line': self.plot(pen=pg.mkPen(color, width=width)),
                'arr': pg.ArrowItem(
                    tailLen=0,
                    tailWidth=1,
                    pen=pg.mkPen(color, width=width),
                    headLen=ARROW_SIZE_PX,
                    brush=None,
                ),
            }
            self.addItem(items['arr'])

        self.items[name] = items

        # add coordinates
        self.update_phasor(name, amp, phi)

    def update_phasor(self, name, amp, phi):
        """Change phasor value."""

        self.phasors[name] = (amp, phi)
        self.__update()

    def remove_phasors(self):
        """Remove phasors and legend."""

        for key in self.items:
            for subkey in self.items[key]:
                self.removeItem(self.items[key][subkey])

        self.phasors = {}

        if self.legend is not None:
            self.legend.scene().removeItem(self.legend)
        self.legend = None

    def show_legend(self):
        """Show legend."""

        self.legend = self.plotItem.addLegend()
        for key in self.items:
            self.plotItem.legend.addItem(
                self.items[key]['line'], key)

    def __update(self):
        for key in self.phasors:
            phasor = self.phasors[key]
            compl = cmath.rect(*phasor)
            x = compl.real
            y = compl.imag

            items = self.items[key]

            items['line'].setData([0, x], [0, y])

            if self.__end == 'arrow':
                arr = items['arr']
                arr.setStyle(angle=180 - degrees(phasor[1]))
                arr.setPos(x, y)

            elif self.__end == 'circle':
                items['point'].setData([x], [y])

    def __build_grid(self):
        self.circles = []
        for _ in range(GRID_DEFAULT_CIRCLES_NUM):
            circle = pg.QtGui.QGraphicsEllipseItem()
            circle.setPen(pg.mkPen(0.2))
            self.circles.append(circle)
            self.addItem(circle)

    def __update_grid(self):
        for i in range(GRID_DEFAULT_CIRCLES_NUM):
            rad = (i + 1) * self.__range / GRID_DEFAULT_CIRCLES_NUM
            self.circles[i].setRect(-rad, -rad, rad*2, rad*2)

        self.setRange(QtCore.QRectF(-rad, rad, 2*rad, -2*rad))

    def __build_labels(self):
        self.labels = []
        for _ in range(2):
            label = pg.TextItem()
            self.labels.append(label)
            self.addItem(label)

    def __update_labels(self):
        self.labels[0].setText("{}".format(self.__range / 2))
        self.labels[0].setPos(0, self.__range / 2)
        self.labels[1].setText("{}".format(self.__range))
        self.labels[1].setPos(0, self.__range)
