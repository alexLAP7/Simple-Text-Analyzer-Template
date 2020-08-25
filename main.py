from natasha import Segmenter, MorphVocab, Doc, NewsEmbedding, NewsMorphTagger
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import os
import sys


def process_russian_text(text, type_of_word_to_highlight='VERB'):
    segmenter = Segmenter()
    emb = NewsEmbedding()
    morph_tagger = NewsMorphTagger(emb)
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    return [token.text for token in doc.tokens if token.pos == type_of_word_to_highlight]


class AdvancedTextEditor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AdvancedTextEditor, self).__init__(parent)
        self.path_to_resources = os.path.join(
            os.getcwd(), 'resources', 'light')
        self.set_layout()

    def set_layout(self):
        self.qvboxLayout = QVBoxLayout(self)
        self.qvboxLayout.setSpacing(1)
        self.qvboxLayout.setAlignment(QtCore.Qt.AlignLeft)
        self.qvboxLayout.setContentsMargins(1, 1, 1, 1)
        self.setLayout(self.qvboxLayout)

        self.text_edit = QtWidgets.QTextEdit()
        self.toolbar = QToolBar()
        self.toolbar.setOrientation(QtCore.Qt.Horizontal)

        self.menu = QtWidgets.QMenuBar()
        self.set_menubar()
        self.set_toolbar()

    def set_menubar(self):
        self.menu_file = self.menu.addMenu("File")

        self.action_undo = self.menu_file.addAction("Open a text file")
        self.action_undo.setStatusTip("Open file action")
        self.action_undo.triggered.connect(self.open_text_file)

        self.menu_edit = self.menu.addMenu("Edit")

        self.action_undo = self.menu_edit.addAction("Undo")
        self.action_undo.setStatusTip("Undo action")
        self.action_undo.setShortcut("Ctrl+Z")
        self.action_undo.triggered.connect(self.text_edit.undo)

        self.action_redo = self.menu_edit.addAction("Redo")
        self.action_redo.setStatusTip("Redo action")
        self.action_redo.setShortcut("Ctrl+Shift+Z")
        self.action_redo.triggered.connect(self.text_edit.redo)

        self.menu_edit.addSeparator()

        self.action_copy = self.menu_edit.addAction("Copy")
        self.action_copy.setStatusTip("Copy action")
        self.action_copy.setShortcut("Ctrl+C")
        self.action_copy.triggered.connect(self.text_edit.copy)

        self.action_cut = self.menu_edit.addAction("Cut")
        self.action_cut.setStatusTip("Cut action")
        self.action_cut.setShortcut("Ctrl+X")
        self.action_cut.triggered.connect(self.text_edit.cut)

        self.action_paste = self.menu_edit.addAction("Paste")
        self.action_paste.setStatusTip("Paste action")
        self.action_paste.setShortcut("Ctrl+V")
        self.action_paste.triggered.connect(self.text_edit.paste)

        self.menu_analyzer = self.menu.addMenu("Analyzer")

        self.action_analyze_rus = self.menu_analyzer.addAction(
            "Analyze selected russian sentences and highlight the structure")
        self.action_analyze_rus.setStatusTip(
            "Highlight the structure")
        self.action_analyze_rus.triggered.connect(self.process_russian_text)

    def set_toolbar(self):
        self.undo = QtWidgets.QAction(QtGui.QIcon(os.path.join(
            self.path_to_resources, "undo.svg")), "Undo", self)
        self.undo.triggered.connect(self.text_edit.undo)

        self.redo = QtWidgets.QAction(QtGui.QIcon(os.path.join(
            self.path_to_resources, "redo.svg")), "Redo", self)
        self.redo.triggered.connect(self.text_edit.redo)

        self.bold = QtWidgets.QAction(QtGui.QIcon(os.path.join(
            self.path_to_resources, "bold-text.svg")), "Make text bold", self)
        self.bold.triggered.connect(self.set_css_font_bold)
        self.italic = QtWidgets.QAction(QtGui.QIcon(os.path.join(
            self.path_to_resources, "italics.svg")), "Make text italic", self)
        self.italic.triggered.connect(self.set_css_font_italic)
        self.underline = QtWidgets.QAction(QtGui.QIcon(os.path.join(
            self.path_to_resources, "underlined.svg")), "Make text underlined", self)
        self.underline.triggered.connect(self.set_css_font_underline)

        self.combobox_font_family = QtWidgets.QFontComboBox()
        self.combobox_font_family.currentFontChanged.connect(
            self.set_css_font_family)

        self.combobox_font_size = QtWidgets.QSpinBox()
        self.combobox_font_size.setSuffix(" pt")
        self.combobox_font_size.valueChanged.connect(
            lambda size: self.set_css_fontSize(size))
        self.combobox_font_size.setValue(14)

        self.font_color = QtWidgets.QAction("Change color", self)
        self.font_color.triggered.connect(self.set_css_font_color)

        self.font_background = QtWidgets.QAction(
            "Change background color", self)
        self.font_background.triggered.connect(
            self.set_css_font_background_color)

        self.align_left = QtWidgets.QAction("Text left alignment", self)
        self.align_left.triggered.connect(
            lambda: self.set_css_text_align("Left"))

        self.align_right = QtWidgets.QAction("Text right alignment", self)
        self.align_right.triggered.connect(
            lambda: self.set_css_text_align("Right"))

        self.align_center = QtWidgets.QAction("Text center alignment", self)
        self.align_center.triggered.connect(
            lambda: self.set_css_text_align("Center"))

        self.align_justify = QtWidgets.QAction("Text justify alignment", self)
        self.align_justify.triggered.connect(
            lambda: self.set_css_text_align("Justify"))

        self.toolbar.addAction(self.undo)
        self.toolbar.addAction(self.redo)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.bold)
        self.toolbar.addAction(self.italic)
        self.toolbar.addAction(self.underline)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.combobox_font_family)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.combobox_font_size)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.font_color)
        self.toolbar.addAction(self.font_background)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.align_left)
        self.toolbar.addAction(self.align_right)
        self.toolbar.addAction(self.align_center)
        self.toolbar.addAction(self.align_justify)

        self.qvboxLayout.addWidget(self.menu)
        self.qvboxLayout.addWidget(self.toolbar)
        self.qvboxLayout.addWidget(self.text_edit)

    def open_text_file(self):
        try:
            abs_path, _ = QFileDialog.getOpenFileName(self,
                                                      'Open File',
                                                      "*.txt",
                                                      "Text Files (*.txt)",
                                                      options=QFileDialog.DontUseNativeDialog)
            with open(abs_path) as f:
                self.text_edit.setPlainText(f.read())
        except:
            self.text_edit.insertPlainText(
                '\nCould not open that text file...\n\n\n')

    def set_css_font_family(self, font):
        self.text_edit.setCurrentFont(font)

    def set_css_fontSize(self, fontSize):
        self.text_edit.setFontPointSize(fontSize)

    def set_css_font_color(self):
        colorDialog = QtWidgets.QColorDialog()
        color = colorDialog.getColor()
        self.text_edit.setTextColor(color)

    def set_css_font_background_color(self):
        colorDialog = QtWidgets.QColorDialog()
        backgroundColor = colorDialog.getColor()
        self.text_edit.setTextBackgroundColor(backgroundColor)

    def set_css_font_bold(self):
        if self.text_edit.fontWeight() == QtGui.QFont.Bold:
            self.text_edit.setFontWeight(QtGui.QFont.Normal)
        else:
            self.text_edit.setFontWeight(QtGui.QFont.Bold)

    def set_css_font_italic(self):
        state = self.text_edit.fontItalic()
        self.text_edit.setFontItalic(not state)

    def set_css_font_underline(self):
        state = self.text_edit.fontUnderline()
        self.text_edit.setFontUnderline(not state)

    def set_css_text_align(self, alignType="Left"):
        if alignType == "Right":
            self.text_edit.setAlignment(QtCore.Qt.AlignRight)
        elif alignType == "Center":
            self.text_edit.setAlignment(QtCore.Qt.AlignCenter)
        elif alignType == "Justify":
            self.text_edit.setAlignment(QtCore.Qt.AlignJustify)
        elif alignType == "Left":
            self.text_edit.setAlignment(QtCore.Qt.AlignLeft)

    def process_russian_text(self):
        list_of_all_words = self.text_edit.toPlainText()

        # list_of_nouns = process_russian_text(list_of_all_words, type_of_word_to_highlight='NOUN')
        list_of_verbs = process_russian_text(
            list_of_all_words, type_of_word_to_highlight='VERB')
        list_of_parts = process_russian_text(
            list_of_all_words, type_of_word_to_highlight='PART')

        # self.highlight_list_of_words_by_color(list_of_nouns, QtGui.QBrush(QtGui.QColor("red")))
        self.highlight_list_of_words_by_color(
            list_of_verbs, QtGui.QBrush(QtGui.QColor("yellow")))
        self.highlight_list_of_words_by_color(
            list_of_parts, QtGui.QBrush(QtGui.QColor("light green")))

    def merge_format_on_word_selection(self, color):
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        qt_format = QtGui.QTextCharFormat()
        qt_format.setBackground(color)
        cursor.mergeCharFormat(qt_format)
        self.text_edit.mergeCurrentCharFormat(qt_format)

    def find_word_and_highlight_it(self, text, color):
        if not text:
            return
        self.text_edit.moveCursor(QtGui.QTextCursor.Start)
        while self.text_edit.find(text, QtGui.QTextDocument.FindWholeWords):
            self.merge_format_on_word_selection(color)

    def highlight_list_of_words_by_color(self, list_of_words_to_highlight, color):
        for word in list_of_words_to_highlight:
            self.find_word_and_highlight_it(word, color)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    advanced_text_editor = AdvancedTextEditor()
    advanced_text_editor.show()
    advanced_text_editor.resize(900, 400)
    sys.exit(app.exec_())
