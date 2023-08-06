import unittest
from appteka.pyqt import testing
from appteka.pyqt.code_text_edit import CodeTextEdit


class TestCodeTextEdit(unittest.TestCase):
    """Tests for CodeTextEdit"""

    def test_text(self):
        app = testing.TestApp(self)

        e = CodeTextEdit()

        code = ''
        code += '{\n'
        code += '  "a": 1,\n'
        code += '  "b": 2\n'
        code += '}'
        e.set_text(code)

        app(e, [
            "Some text is printed",
            "Lines numbered",
            "Current line is highlighted",
            "Font is monospace",
        ])
