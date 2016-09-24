import st
import pretty
from .. import *


@ui_extension
class ComboBox(QComboBox, BaseInterface,
               pretty.WidgetStringInterface, pretty.WidgetIndexInterface, pretty.WidgetStringListInterface):
    class ComboBoxItem:
        def __init__(self, parent: 'ComboBox'):
            self.parent = parent

        @property
        def count(self):
            return self.parent.count()

        def add_strings(self, *text):
            self.parent.addItems(text)

    class StringItem(ComboBoxItem, pretty.WidgetStringItem):
        def get_value(self):
            return self.parent.currentText()

        def set_value(self, value=None):
            texts = self.parent.string_list.value
            assert isinstance(texts, list)

            if value is None:
                self.parent.index.value = 0
            elif value in texts:
                self.parent.index.value = texts.index(value)
            else:
                self.add_strings(value)
                self.parent.index.value = self.count - 1

        def set_changed_connection(self):
            # noinspection PyUnresolvedReferences
            self.parent.currentIndexChanged[str].connect(self.check_change)

    class IndexItem(ComboBoxItem, pretty.IndexItem):
        def get_value(self):
            return self.parent.currentIndex()

        def set_value(self, value):
            if value is None or value >= self.count:
                value = 0
            self.parent.setCurrentIndex(value)

        def set_changed_connection(self):
            # noinspection PyUnresolvedReferences
            self.parent.currentIndexChanged[int].connect(self.check_change)

    class StringsItem(ComboBoxItem, pretty.StringsItem):
        def get_value(self):
            return st.foreach(self.parent.itemText, range(self.count))

        def set_value(self, value):
            value = value or []

            self.parent.clear()
            self.parent.addItems(value)
            self.string_list.check_change()
