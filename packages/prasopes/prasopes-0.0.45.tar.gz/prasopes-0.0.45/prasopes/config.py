#!/usr/bin/env python3
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui


def settings():
    settings = QtCore.QSettings("Yansoft", "Prasopes")
    defvals = {("view/autozoomy", True),
               ("view/filebrowservisible", True),
               ("view/consolevisible", True),
               ("view/acqparvisible", True),
               ("view/intensities", False),
               ("view/digits", 2),
               ("view/oddeven", False),
               ("view/legend", True),
               ("print/msspec_xinch", 10),
               ("print/msspec_yinch", 4),
               ("print/msspec_dpi", 300),
               ("print/msspec_xtics", 5),
               ("print/zcespec_xinch", 5),
               ("print/zcespec_yinch", 2),
               ("print/zcespec_dpi", 300),
               ("print/reactspecspec_xinch", 3.5),
               ("print/reactspecspec_yinch", 2),
               ("print/reactspecspec_dpi", 300),
               ("imggen/msspec_xinch", 10),
               ("imggen/msspec_yinch", 4),
               ("imggen/msspec_dpi", 300),
               ("imggen/msspec_xtics", 5),
               ("imggen/msspec_onlymanann", False),
               ("imggen/zcespec_xinch", 5),
               ("imggen/zcespec_yinch", 2),
               ("imggen/zcespec_dpi", 300),
               ("imggen/drlspec_xinch", 10),
               ("imggen/drlspec_yinch", 4),
               ("imggen/drlspec_dpi", 300),
               ("imggen/path", True),
               ("imggen/reactspecspec_xinch", 3.5),
               ("imggen/reactspecspec_yinch", 2),
               ("imggen/reactspecspec_dpi", 300),
               ("reactivity/index", 0),
               ("reactivity/activetab", 0),
               ("recents", ""),
               ("timstof/ms_sampling", 500),
               ("timstof/ms_bins", 0.001),
               ("timstof/mob_sampling", 5000),
               ("timstof/mob_bins", 0.0001)}
    [settings.setValue(*i)
     for i in defvals if not settings.contains(i[0])]
    return settings


def pathsearch(text, value, config):
    filename = QtWidgets.QFileDialog.getExistingDirectory()
    if filename != '':
        text.setText(filename)
        config.setValue(value, filename)


def pathlineconf(label, value, config):
    """adds generic filepath config line"""
    textfield = QtWidgets.QLineEdit(str(config.value(value)))
    textfield.editingFinished.connect(lambda: config.setValue(
        value, textfield.text()))
    browse_button = QtWidgets.QPushButton("Browse..")
    browse_button.clicked.connect(lambda: pathsearch(
        textfield, value, config))
    layout = QtWidgets.QHBoxLayout()
    layout.addWidget(QtWidgets.QLabel(str(label)))
    layout.addWidget(textfield)
    layout.addWidget(browse_button)
    return layout


def posvarconf(label, value, config, num="int"):
    """adds generic positive integer config line"""
    textfield = QtWidgets.QLineEdit(str(config.value(value)))
    textfield.editingFinished.connect(lambda: config.setValue(
        value, textfield.text()))
    validator = QtGui.QIntValidator() if num == "int"\
        else QtGui.QDoubleValidator()
    validator.setBottom(0)
    textfield.setValidator(validator)
    layout = QtWidgets.QHBoxLayout()
    layout.addWidget(QtWidgets.QLabel("{}:".format(label)))
    layout.addStretch()
    layout.addWidget(textfield)
    return layout


def checkboxconf(label, value, config):
    checkbox = QtWidgets.QCheckBox(label)
    checkbox.setChecked(config.value(value, type=bool))
    checkbox.stateChanged.connect(lambda: config.setValue(
        value, checkbox.checkState()))
    return checkbox


def dial(parent):
    """constructs a dialog window"""
    dialog = QtWidgets.QDialog(
        parent, windowTitle='Settings')
    dialog.resize(600, -1)

    config = settings()

    tabs = QtWidgets.QTabWidget()

    pathtab = QtWidgets.QWidget()
    pathlayout = QtWidgets.QVBoxLayout(pathtab)
    pathlayout.addLayout(pathlineconf(
        "Acquisition temp folder", "tmp_location", config))
    pathlayout.addLayout(pathlineconf(
        "Default open folder", "open_folder", config))
    tabs.addTab(pathtab, "Paths")

    printtab = QtWidgets.QWidget()
    printlayout = QtWidgets.QVBoxLayout(printtab)
    printlayout.addLayout(posvarconf(
        "Figure width (inch)", "print/xinch", config, "nonint"))
    printlayout.addLayout(posvarconf(
        "Figure height (inch)", "print/yinch", config, "nonint"))
    printlayout.addLayout(posvarconf(
        "Figure dpi", "print/dpi", config))
    printlayout.addLayout(posvarconf(
        "Figure x axis major ticks count", "print/xtics", config))
    tabs.addTab(printtab, "Printing")

    imggentab = QtWidgets.QWidget()
    imggenlayout = QtWidgets.QVBoxLayout(imggentab)
    imggenlayout.addLayout(posvarconf(
        "Figure width (inch)", "imggen/msspec_xinch", config, "nonint"))
    imggenlayout.addLayout(posvarconf(
        "Figure height (inch)", "imggen/msspec_yinch", config, "nonint"))
    imggenlayout.addLayout(posvarconf(
        "Figure dpi", "imggen/msspec_dpi", config))
    imggenlayout.addLayout(posvarconf(
        "Figure x axis major ticks count", "imggen/msspec_xtics", config))
    imggenlayout.addWidget(checkboxconf(
        "Manual annotation only", "imggen/msspec_onlymanann", config))
    imggenlayout.addWidget(checkboxconf(
        "Isert path to exported image", "imggen/path", config))
    tabs.addTab(imggentab, "Image clip/export")

    timstoftab = QtWidgets.QWidget()
    timstoflayout = QtWidgets.QVBoxLayout(timstoftab)
    timstoflayout.addLayout(posvarconf(
        "Maximum number of samples - MS", "timstof/ms_sampling", config))
    timstoflayout.addLayout(posvarconf(
        "Bins - MS", "timstof/ms_bins", config, "nonint"))
    timstoflayout.addLayout(posvarconf(
        "Maximum number of samples - mobility", "timstof/mob_sampling",
        config))
    timstoflayout.addLayout(posvarconf(
        "Bins - mobility", "timstof/mob_bins", config, "nonint"))
    tabs.addTab(timstoftab, "TimsTOF")

    viewtab = QtWidgets.QWidget()
    viewlayout = QtWidgets.QVBoxLayout(viewtab)
    viewlayout.addLayout(posvarconf(
        "number of digits after decimal point", "view/digits", config))
    tabs.addTab(viewtab, "View Settings")


    close_button = QtWidgets.QPushButton("Close")
    close_button.clicked.connect(dialog.close)

    butt_layout = QtWidgets.QHBoxLayout()
    butt_layout.addWidget(close_button)
    butt_layout.addStretch(1)

    layout = QtWidgets.QVBoxLayout(dialog)
    layout.addWidget(QtWidgets.QLabel("Changes are saved automatically"))
    layout.addWidget(tabs)
    layout.addStretch(1)
    layout.addLayout(butt_layout)

    dialog.show()
