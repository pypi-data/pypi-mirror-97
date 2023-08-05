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

"""The tool for visual testing of widgets."""

import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from appteka.pyqt import gui


class TestApp:
    """An application for displaying a widget that has been set to a
    certain state and asking questions that express the requirements
    of the test case.

    Parameters
    ----------
    context: unittest.TestCase
        The class in that the test case should being ran.
    """

    __app = None

    def __init__(self, context):
        if not TestApp.__app:
            TestApp.__app = QtWidgets.QApplication(sys.argv)

        self.answer = False
        self.dialog = _Dialog(self)
        self.context = context

    def __call__(self, widget, assertions):
        self.dialog.set_widget(widget)
        self.dialog.set_assertions(assertions)

        self.dialog.show()
        TestApp.__app.exec()

        self.context.assertTrue(self.answer)


class _Dialog(QtWidgets.QDialog):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app
        self.__make_gui()

    def __make_gui(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        self.widget_layout = gui.add_sublayout(main_layout, "h")

        self.assert_layout = gui.add_sublayout(main_layout, "h")
        self.label_assert = gui.add_label("", self.assert_layout)
        self.label_assert.setWordWrap(True)

        self.button_layout = gui.add_sublayout(main_layout, "h")
        self.button_no = gui.add_button("No", self.__on_button_no,
                                        self.button_layout)
        self.button_yes = gui.add_button("Yes", self.__on_button_yes,
                                         self.button_layout)
        self.button_yes.setFocus(Qt.ActiveWindowFocusReason)

    def set_widget(self, widget):
        """Set widget to be shown."""
        self.widget_layout.addWidget(widget)

    def set_assertions(self, assertions):
        """Set assertions to be printed in dialog."""
        lines = ""
        for asr in assertions:
            lines += "- {}\n".format(asr)
        self.label_assert.setText(lines)

    def __on_button_no(self):
        self.app.answer = False
        self.reject()

    def __on_button_yes(self):
        self.app.answer = True
        self.accept()
