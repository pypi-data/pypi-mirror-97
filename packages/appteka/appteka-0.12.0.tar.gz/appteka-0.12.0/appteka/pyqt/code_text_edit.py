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

"""Here the text edit with line numbers and highlighting of current
line is implemented."""

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QSize, QRect, Qt

LINE_COLOR = QtGui.QColor(Qt.yellow).lighter(160)
FONT = "monospace"


class CodeTextEdit(QtWidgets.QPlainTextEdit):
    """Text field for editing the source code."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

        font = QtGui.QFont(FONT)
        font.setStyleHint(QtGui.QFont.Monospace)
        self.setFont(font)

    def set_text(self, text):
        """Set text."""
        self.document().setPlainText(text)

    def lineNumberAreaPaintEvent(self, event):
        painter = QtGui.QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(
            self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = "{}".format(block_number + 1)
                painter.setPen(Qt.black)
                painter.drawText(
                    0, top, self.lineNumberArea.width(),
                    self.fontMetrics().height(), Qt.AlignRight,
                    number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number = block_number + 1

    def lineNumberAreaWidth(self):
        count = max(1, self.blockCount())
        digits = 1
        while count >= 10:
            count = count / 10
            digits = digits + 1

        return 3 + self.fontMetrics().horizontalAdvance('9') * digits

    def resizeEvent(self, e):
        super().resizeEvent(e)

        rect = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(
            rect.left(), rect.top(),
            self.lineNumberAreaWidth(), rect.height()))

    def updateLineNumberAreaWidth(self, newBlockCount):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def highlightCurrentLine(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QtWidgets.QTextEdit.ExtraSelection()
            selection.format.setBackground(LINE_COLOR)
            selection.format.setProperty(
                QtGui.QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(
                0, rect.y(),
                self.lineNumberArea.width(),
                rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)


class LineNumberArea(QtWidgets.QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self):
        return QSize(self.code_editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.code_editor.lineNumberAreaPaintEvent(event)
