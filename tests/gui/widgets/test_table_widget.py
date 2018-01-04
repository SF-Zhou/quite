import unittest
import quite


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.table_widget = quite.TableWidget()
        self.table_widget.set_just_show_mode()
        self.table_widget.set_headers(['字符串', '整形', '浮点型'])

    def test_table_widget_row(self):
        with quite.EventLoop(0.1):
            self.table_widget.show()
            excuted = [False]

            times = []
            @quite.connect_with(self.table_widget.string.changed)
            def test_changed(text):
                excuted[0] = True
                times.append(len(times))
                if len(times) == 0:
                    self.assertEqual(text, 'first 1 1.1')
                elif len(times) == 1:
                    self.assertEqual(text, 'second 2 2.2')

            self.table_widget.string_list.value = ['first 1 1.1', 'second 2 2.2']
            self.assertTrue(excuted[0])

    def test_table_widget_string_list(self):
        with quite.EventLoop(0.1):
            self.table_widget.show()
            executed = [False]
            string_list = ["first 1 1.1", "second 2 2.2", "third 3 3.3"]

            @quite.connect_with(self.table_widget.string_list.changed)
            def string_list_changed(string_list_now):
                self.assertEqual(string_list, string_list_now)
                executed[0] = True

            self.table_widget.string_list.value = string_list
            self.assertTrue(executed[0])

    def test_table_widget_set_text(self):
        with quite.EventLoop(0.1):
            self.table_widget.show()
            times = []

            @quite.connect_with(self.table_widget.string.changed)
            def text_changed(string):
                if len(times) == 0:
                    self.assertEqual(string, 'first 1 1.1')
                elif len(times) == 1:
                    self.assertEqual(string, 'second 2 2.2')
                elif len(times) == 2:
                    self.assertEqual(string, 'first 1 1.1')
                elif len(times) == 3:
                    self.assertEqual(string, '')
                times.append(len(times))

            self.table_widget.string.set_value('first 1 1.1')
            self.table_widget.string.set_value('second 2 2.2')
            self.table_widget.string.set_value('first 1 1.1')
            self.assertEqual(len(times), 3)
            self.assertEqual(self.table_widget.string_list.count, 2)
if __name__ == '__main__':
    unittest.main()
