#!/usr/bin/env python3
from matplotlib.backends.backend_qt5agg import\
        FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import matplotlib
import numpy as np
import prasopes.datasets as ds
import prasopes.datatools as dt
import prasopes.graphtools as gt
import prasopes.filetools as ft
import prasopes.config as cf
import prasopes.drltools as drl
import prasopes.imagetools as imgt
import prasopes.msonmobtools_gui as mmtg
import prasopes.mobtools as mt
import os.path
import logging
matplotlib.use("Qt5Agg")


logger = logging.getLogger('tofLogger')
settings = cf.settings()


def export_dial(augCanvas, grph):
    """exports the reactivity into the .dat file format"""
    if not augCanvas.ds or isinstance(augCanvas.ds, ds.ThermoRawDataset):
        QtWidgets.QMessageBox.warning(
            None, "Export spectrum",
            "Nothing to export, cancelling request")
        return
    exp_f_name = ft.get_save_filename(
        "Export spectrum", "dat table (*.dat)", "dat", None)
    if exp_f_name != '':
        names = ["1/K_0", "intensity"]
        units = ["Vs/cm^2", ""]
        description = os.path.basename(augCanvas.ds.filename) + " " +\
            " -- ".join([line._label for line in grph.get_lines()])
        expf = open(exp_f_name, 'w')
        expf.write(dt.specttostr(grph, " ", names, units, description))
        expf.close


def main_window(parent, augCanvas, update_signal):
    if not augCanvas.ds or isinstance(augCanvas.ds, ds.ThermoRawDataset):
        QtWidgets.QMessageBox.warning(
            parent, "MOB GUI",
            "No spectrum opened, or file format is not supported,"
            "nothing to display")
        return
    reactlabels = dict(name="", xlabel="$1/K_0 (Vs/cm^2)\ \\it→$",
                       ylabel="$Intensity\ \\it→$", annotation=[], texts=[],
                       ancx=5, ancy=3)
    cache = augCanvas.tofcache

    def onclose(widget, event, ionstable, canvas, cache, update_fnc):
        logger.debug("custom close routine called")
        cache[0], cache[1] = ionstable, canvas
        update_signal.signal.disconnect(update_fnc)
        QtWidgets.QDialog.closeEvent(widget, event)

    def update_fnc():
        if not augCanvas.ds or isinstance(augCanvas.ds, ds.ThermoRawDataset):
            QtWidgets.QMessageBox.warning(
                parent, "MOB GUI",
                "No spectrum opened, or file format is not supported,"
                "nothing to display")
            return
        else:
            mt.pop_dial(dialspect, ionstable, reactlabels,
                        augCanvas.ds.get_mobilogram)

    dial_widget = QtWidgets.QDialog(
            parent, windowTitle='Mobilogram')
    dial_widget.closeEvent = lambda event: onclose(
        dial_widget, event, ionstable, graph_canvas, cache, update_fnc)
    update_signal.signal.connect(update_fnc)

    if cache == [None, None]:
        dial_graph = Figure(figsize=(5, 2), dpi=100, facecolor="None",
                            constrained_layout=True)
        dialspect = dial_graph.add_subplot(111, facecolor=(1, 1, 1, 0.8))
        graph_canvas = FigureCanvas(dial_graph)
        graph_canvas.setStyleSheet("background-color:transparent;")
        graph_canvas.setAutoFillBackground(False)

        gt.zoom_factory(dialspect, 1.15, reactlabels)
        gt.pan_factory(dialspect, reactlabels)

        ionstable = dt.table(["Name", "Start time (min)", "End time (min)",
                              "Mass (m/z)", "Peak width", "Profile"])
    else:
        ionstable = cache[0]
        graph_canvas = cache[1]
        dialspect = graph_canvas.figure.axes[0]

    ionstable.itemChanged.connect(lambda item: mt.ionstable_changed(
        item.row(), item.column(), augCanvas.ds.get_spectra, ionstable))

    updatebtn = QtWidgets.QPushButton("Update")
    updatebtn.clicked.connect(lambda: update_fnc())

    addbtn = QtWidgets.QPushButton("Add")
    addbtn.clicked.connect(lambda: mt.add_row(
        augCanvas.ds.get_spectra, dialspect, ionstable))
    rmbtn = QtWidgets.QPushButton("Remove")
    rmbtn.clicked.connect(lambda: mt.remove_rows(ionstable))

    mobbtn = QtWidgets.QPushButton("mobMZ")
    mobbtn.clicked.connect(lambda: mmtg.main_window(
        parent, augCanvas, update_signal))
    expbtn = QtWidgets.QPushButton("Export")
    expbtn.clicked.connect(lambda: export_dial(
        augCanvas, dialspect))

    buttlayout = QtWidgets.QHBoxLayout()
    buttlayout.addWidget(updatebtn)
    buttlayout.addStretch()
    buttlayout.addWidget(addbtn)
    buttlayout.addWidget(rmbtn)
    buttlayout.addStretch()
    buttlayout.addWidget(mobbtn)
    buttlayout.addWidget(expbtn)

    dial_layout = QtWidgets.QVBoxLayout(dial_widget)
    dial_layout.addWidget(graph_canvas, stretch=1)
    dial_layout.addWidget(ionstable)
    dial_layout.addLayout(buttlayout)
    dial_widget.setFocus()
    dial_widget.show()
    update_fnc()
