import urwid

from clianer.widgets.dataset_view import DatasetView
from clianer.widgets.filter_list import FilterList
from clianer.widgets.add_filter import AddFilterDialog, EditFilterDialog


PALETTE = [(None,  "light gray", "black"),
           ("heading", "white", "black"),
           ("line", "light gray", "black"),
           ("options", "light cyan", "black"),
           ("focus heading", "white", "dark red"),
           ("focus line", "white", "black"),
           ("focus options", "black", "light gray"),
           ("selected", "white", "dark blue")]

# FOCUS_MAP = {"heading": "focus heading",
#              "options": "focus options",
#              "line": "focus line"}


class ClianerFrame(urwid.WidgetWrap):
    def __init__(self, f1, f2):
        self.dialog = None
        self.filterList = FilterList()
        self.datasetView = DatasetView(f1, f2)

        self.body = urwid.Columns([(40, self.filterList), self.datasetView])
        self.header = urwid.Text("File")

        self.footer = urwid.Columns([
            urwid.AttrMap(urwid.Text("F3: Add Filter"), "options"),
            urwid.AttrMap(urwid.Text("Q: Quit"), "options")
        ])

        self.top = urwid.Frame(
            self.body, header=self.header, footer=self.footer)

        super().__init__(self.top)

    def keypress(self, size, key):
        if key == "q" or key == "Q":
            if self.dialog is None:
                raise urwid.ExitMainLoop()

        if key == "f3":
            if self.dialog is None:
                self.openAddFilterDialog()

        return super().keypress(size, key)

    def openAddFilterDialog(self, height=30, width=40):
        assert self.dialog is None
        self.dialog = "add_filter"
        widget = AddFilterDialog(self)

        height = 30
        width = 40

        self._w = urwid.Overlay(
            widget,
            self._w,
            align="center",
            width=width,
            valign="middle",
            height=height)
        urwid.connect_signal(self._w[1], "close", self.addFilterDialogClosed)

    def addFilterDialogClosed(self, widget, filter_name, filter_cfg):
        if self.dialog != "add_filter":
            raise Exception("Unexpected dialog")
        assert widget is not None

        self.dialog = None
        urwid.disconnect_signal(
            self._w[1], "close", self.addFilterDialogClosed)
        self._w = self._w[0]

        if filter_name is not None:
            assert filter_cfg is not None
            self.openEditFilterDialog(filter_name, filter_cfg)

    def openEditFilterDialog(self, filter_name, filter_cfg):
        assert self.dialog is None
        self.dialog = "edit_filter"

        widget = EditFilterDialog(self, filter_name, filter_cfg)
        self._w = urwid.Overlay(
            widget,
            self._w,
            align="center",
            width=80,
            valign="middle",
            height=40)

        urwid.connect_signal(self._w[1], "close", self.editFilterDialogClosed)

    def editFilterDialogClosed(self, widget, filter_name, filter_args):
        if self.dialog != "edit_filter":
            raise Exception("Unexpected dialog")
        assert widget is not None

        self.dialog = None
        urwid.disconnect_signal(self._w[1], "close", self.editFilterDialogClosed)
        self._w = self._w[0]

        if filter_args is not None:
            assert filter_name is not None
            self.filterList.add_filter(filter_name, filter_args)
