from . import deferred_define
from . import Widget, QWidget
from . import QMainWindow, QDockWidget
from . import QHBoxLayout, SquareLayout
from . import WidgetController
from . import QSize, QSizeF, QPoint
from . import QPicture, QPixmap
from . import QPrinter, QPainter


@deferred_define
def set_central_widget(self: Widget, widget, del_pre_widget=True):
    if isinstance(widget, WidgetController):
        widget = widget.w
    if not isinstance(widget, QWidget):
        raise TypeError('Only Support Widget or WidgetController')
    widget.setVisible(True)  # ensure widget is visible

    if hasattr(self, 'center_widget'):
        self.layout().removeWidget(self.center_widget)
        self.center_widget.setVisible(False)  # hide pre widget, and widget can reuse
        if del_pre_widget:
            self.center_widget.deleteLater()

    if isinstance(self, QMainWindow):
        self.setCentralWidget(widget)
    elif isinstance(self, QDockWidget):
        self.setWidget(widget)
    elif hasattr(self, 'center_widget'):
        self.layout().addWidget(widget)
    else:
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(widget)
        self.setLayout(layout)
    self.center_widget = widget


@deferred_define
def set_square_widget(self: Widget, widget: Widget, spacing=0):
    if isinstance(widget, WidgetController):
        widget = widget.w
    if not isinstance(widget, QWidget):
        raise TypeError('Only Support Widget or WidgetController')

    layout = SquareLayout()
    layout.setSpacing(spacing)
    layout.addWidget(widget)
    self.setLayout(layout)
    self.center_widget = widget


@deferred_define
def set_layout_spacing(self: Widget, spacing):
    layout = self.layout()
    assert isinstance(layout, SquareLayout)
    layout.setSpacing(spacing)
    layout.update()


@deferred_define
def export_to_pdf(self: Widget, filename: str, export_size=QSize(1060, 730)):
    assert isinstance(export_size, QSize)
    w, h = self.size
    if w > h:
        self.resize(export_size.width(), export_size.height())
    else:
        self.resize(export_size.height(), export_size.width())

    p = QPicture()
    painter = QPainter(p)
    self.render(painter, QPoint(0, 0))
    painter.end()

    printer = QPrinter()
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setOutputFileName(filename)
    if w > h:
        printer.setOrientation(QPrinter.Landscape)
    if export_size.width() != 1060 or export_size.height() != 730:
        printer.setPageSize(QPrinter.Custom)
        printer.setPaperSize(QSizeF(self.size[1] * 0.8 + 20, self.size[0] * 0.8 + 20), QPrinter.Point)

    painter = QPainter()
    ok = painter.begin(printer)
    if ok:
        painter.drawPicture(0, 0, p)
        ok = painter.end()
    self.resize(w, h)
    return ok


@deferred_define
def export_to_bitmap(self: Widget, filename: str, export_size=QSize(1060, 730)):
    if filename.endswith('pdf'):
        return export_to_pdf(self, filename)
    assert isinstance(export_size, QSize)
    w, h = self.size
    if w > h:
        self.resize(export_size.width(), export_size.height())
    else:
        self.resize(export_size.height(), export_size.width())

    p = QPixmap(*self.size)
    painter = QPainter(p)
    self.render(painter, QPoint(0, 0))
    painter.end()
    ok = p.save(filename)

    self.resize(w, h)
    return ok
