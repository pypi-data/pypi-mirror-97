#!/usr/bin/env python3

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from code import InteractiveConsole
from io import StringIO
from os import path
import contextlib
import prasopes.config as cf


class AugDock(QtWidgets.QDockWidget):
    """construct dock with vboxlayout and action to show/hide"""
    def __init__(self, name, actionname, cfval):
        config = cf.settings()
        super().__init__(name)
        self.setWidget(QtWidgets.QWidget())
        self.layout = QtWidgets.QVBoxLayout(self.widget())
        self.action = QtWidgets.QAction(
                actionname, None, checkable=True,
                checked=config.value(cfval, type=bool))
        self.action.triggered.connect(
            lambda: self.show() if self.action.isChecked()
            else self.hide())
        self.closeEvent = lambda event: self.closeOverride(event)
        if not config.value(cfval, type=bool):
            self.hide()

    def closeOverride(self, event):
        self.action.setChecked(False)
        self.hide()
        event.ignore()


class AugLineEdit(QtWidgets.QLineEdit):
    """QLineEdit with history"""
    def __init__(self):
        super().__init__()
        self.history = []
        self.historypos = 0
        self.returnPressed.connect(lambda: self.history.append(self.text())
                                   if self.text() != "" else None)

    def keyPressEvent(self, event):
        """super().keyPressEvent override"""
        if event.key() in (QtCore.Qt.Key_Up, QtCore.Qt.Key_Down):
            self.historypos = min(len(self.history), self.historypos+1) if\
                event.key() == QtCore.Qt.Key_Up else max(0, self.historypos-1)
            self.setText(self.history[-self.historypos])\
                if self.historypos > 0 else self.setText("")
        else:
            self.historypos = 0
            super().keyPressEvent(event)


def consoleDockWidget(localvars, actionname, cfval):
    def consoleExecfunc(inp, outp, loc):
        stream = StringIO()
        console = InteractiveConsole(locals=loc)
        text = inp.text()
        inp.setText("")
        with contextlib.redirect_stdout(stream),\
                contextlib.redirect_stderr(stream):
            outp.append(">>>"+text)
            console.runcode(text)
            outtext = stream.getvalue()
            if outtext == "" and text != "":
                with contextlib.redirect_stderr(StringIO()):
                    # Brief sanitization
                    console.runcode("""print(eval('{}'.format(str('""" +
                                    text + """'))))""")
                outtext = stream.getvalue()
            if outtext != "":
                outp.append(outtext[:-1])
    dock = AugDock("console", actionname, cfval)
    coutput = QtWidgets.QTextEdit()
    coutput.setReadOnly(True)
    cinput = AugLineEdit()
    cinput.returnPressed.connect(lambda: consoleExecfunc(
        cinput, coutput, localvars))
    [dock.layout.addWidget(i) for i in (coutput, cinput)]
    return dock


def treeDockWidget(actionname, cfval, update, loadfnc, parent,
                   augCanvas, config, loadthread):
    config = cf.settings()
    fileModel = QtWidgets.QFileSystemModel()
    fileModel.setRootPath('')
    activeDir = fileModel.index(config.value("open_folder"))
    treeview = QtWidgets.QTreeView()
    treeview.setModel(fileModel)
    treeview.setCurrentIndex(activeDir)
    treeview.expand(activeDir)
    dirview = QtWidgets.QListView()
    dirview.setModel(fileModel)

    sortorder = QtWidgets.QComboBox()
    sortorder.addItems(("name", "time"))
    sortorder.currentIndexChanged.connect(
        lambda index: fileModel.sort(index and 3, 1))

    orderlayout = QtWidgets.QHBoxLayout()
    orderlayout.addStretch(1)
    for i in (QtWidgets.QLabel("Sort by:"), sortorder):
        orderlayout.addWidget(i)
    dock = AugDock("Folder View", actionname, cfval)
    dock.layout.addLayout(orderlayout)
    [dock.layout.addWidget(i) for i in (treeview, dirview)]

    def scrolltoonce():
        fileModel.layoutChanged.disconnect(scrolltoonce)
        treeview.scrollTo(fileModel.index(config.value("open_folder")), 1)

    def clickload(index):
        loadfnc(parent, augCanvas, update, config, loadthread,
                filename=fileModel.filePath(index))

    fileModel.directoryLoaded.connect(
            lambda: treeview.resizeColumnToContents(0))
    update.signal.connect(lambda: treeview.setCurrentIndex(fileModel.index(
                                  augCanvas.ds.filename)))
    update.signal.connect(lambda: dirview.setRootIndex(fileModel.index(
            path.dirname(path.realpath(augCanvas.ds.filename)))))
    fileModel.layoutChanged.connect(scrolltoonce)

    for i in [treeview.doubleClicked, dirview.doubleClicked, dirview.clicked]:
        i.connect(clickload)
    return dock
