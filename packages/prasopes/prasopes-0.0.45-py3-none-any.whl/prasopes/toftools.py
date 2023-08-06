#!/usr/bin/env python3
from matplotlib.backends.backend_qt5agg import\
        FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtCore
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
import os.path
import logging
matplotlib.use("Qt5Agg")


logger = logging.getLogger('tofLogger')
settings = cf.settings()


def get_massargs(tab, row, masses):
    startm = drl.floatize(tab, row, 3) - (drl.floatize(tab, row, 4) / 2)
    endm = drl.floatize(tab, row, 3) + (drl.floatize(tab, row, 4) / 2)
    massargs = dt.argsubselect(masses, startm, endm)
    return massargs


def update_profile(table, row, dataset):
    """parent table profile spectrum updating procedure"""
    logger.debug("updating parent table row {} profile".format(row))
    # Dont do anything to graph when the spectrum is not populated
    if not dataset or isinstance(dataset, ds.ThermoRawDataset):
        return
    spectrum = table.cellWidget(row, 5).figure.get_axes()[0]
    spectrum.clear()
    limits = []
    spectra = dataset.get_spectra(*[drl.floatize(table, row, i) for i in (1,2)])
    for i,spectxy in enumerate(spectra):
        massargs = get_massargs(table, row, spectxy[0])
        spectrum.plot(spectxy[0], spectxy[1], ':', color='gray')
        spectrum.plot(spectxy[0][massargs], spectxy[1][massargs],
                      color=gt.colors[i % len(gt.colors)]/255)
        limits.append((spectxy[0][massargs[[0, -1]]],
                       max(spectxy[1][massargs])))
    widest = np.argmax([abs(lim[0][1]-lim[0][0]) for lim in limits])
    xmin, xmax = limits[widest][0]
    xex = max((xmax-xmin)*0.25, 0.02)
    spectrum.set_xlim(xmin-xex, xmax+xex)
    ymax = max(*[lim[1] for lim in limits], 1)
    spectrum.set_ylim(ymax*-0.1, ymax*1.2)
    spectrum.figure.canvas.draw()


def ionstable_changed(row, col, ds, table):
    if col in (1,2,3,4):
        update_profile(table, row, ds)
    table.blockSignals(True)
    table.item(row, 0).setBackground(QtGui.QBrush(
        QtGui.QColor(*gt.colors[row % len(gt.colors)], alpha=50)))
    table.blockSignals(False)


def pop_dial(augCanvas, dialspect, ionstable, labels):
    ds = augCanvas.ds
    dialspect.clear()
    gt.pop_plot([], [], dialspect, labels)
    for row in range(ionstable.rowCount()):
            name = ionstable.item(row, 0).text()
            startm = drl.floatize(ionstable, row, 3)\
                     - (drl.floatize(ionstable, row, 4) / 2)
            endm = drl.floatize(ionstable, row, 3)\
                     + (drl.floatize(ionstable, row, 4) / 2)
            [tstart, tend] = [drl.floatize(ionstable, row, i) for i in (1,2)]
            spectrum = ds.get_mobilogram(startm, endm, tstart, tend)
            dialspect.plot(spectrum[0], spectrum[1], label=name,
                             color=(gt.colors[row % len(gt.colors)] / 255))
    if ionstable.rowCount():
        dialspect.autoscale(True)
        dialspect.legend(loc=2)
    dialspect.figure.canvas.draw()
    return


def add_row(ds, dialspect, ionstable):
    """add parent ion to the table"""
    logger.debug("adding line")
    newrow = ionstable.rowCount()

    ionstable.blockSignals(True)

    ionstable.setRowCount(newrow + 1)
    for i in range(5):
        ionstable.setItem(newrow, i, QtWidgets.QTableWidgetItem())
        if newrow != 0:
            val = drl.floatize(ionstable, newrow-1, i)
            if i not in (1,2,4):
                val = val+1
            ionstable.item(newrow, i).setText(str(val))

    ion_graph = Figure(figsize=(3, 1.5), dpi=100, facecolor="None")
    ion_graph.add_subplot(111, facecolor=(1, 1, 1, 0.8),
                          position=(-0.01, -0.01, 1.02, 1.02))
    graph_canvas = FigureCanvas(ion_graph)
    graph_canvas.setStyleSheet("background-color:transparent;")
    graph_canvas.setAutoFillBackground(False)
    ionstable.setCellWidget(newrow, 5, graph_canvas)

    ionstable.blockSignals(False)
    ionstable_changed(newrow, 1, ds, ionstable)
    return


def remove_rows(ionstable, rows=None):
    logger.info("remowing rows")
    if not rows:
        rows = reversed(list(set(
            map(lambda x: x.row(), ionstable.selectedIndexes()))))
    [ionstable.removeRow(row) for row in rows]
    return


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
        names = ["time", "intensity"]
        units = ["sec??", ""]
        description = os.path.basename(augCanvas.ds.filename) + " " +\
                " -- ".join([line._label for line in grph.get_lines()])
        expf = open(exp_f_name, 'w')
        expf.write(dt.specttostr(grph, " ", names, units, description))
        expf.close


def main_window(parent, augCanvas, update_signal):
    reactlabels = dict(name="", xlabel="$time (??seconds??)\ \\it→$",
                       ylabel="$Intensity\ \\it→$")
    cache = augCanvas.tofcache

    def onclose(widget, event, ionstable, canvas, cache, update_fnc):
        logger.debug("custom close routine called")
        cache[0], cache[1] = ionstable, canvas
        update_signal.signal.disconnect(update_fnc)
        QtWidgets.QDialog.closeEvent(widget, event)

    def update_fnc():
        pop_dial(augCanvas, dialspect, ionstable, reactlabels)

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

    ionstable.itemChanged.connect(lambda item: ionstable_changed(
        item.row(), item.column(), augCanvas.ds, ionstable))

    updatebtn = QtWidgets.QPushButton("Update")
    updatebtn.clicked.connect(lambda: update_fnc())

    addbtn = QtWidgets.QPushButton("Add")
    addbtn.clicked.connect(lambda: add_row(
        augCanvas.ds, dialspect, ionstable))
    rmbtn = QtWidgets.QPushButton("Remove")
    rmbtn.clicked.connect(lambda: remove_rows(ionstable))

    expbtn = QtWidgets.QPushButton("Export")
    expbtn.clicked.connect(lambda: export_dial(
        augCanvas, dialspect))

    buttlayout = QtWidgets.QHBoxLayout()
    buttlayout.addWidget(updatebtn)
    buttlayout.addStretch()
    buttlayout.addWidget(addbtn)
    buttlayout.addWidget(rmbtn)
    buttlayout.addStretch()
    buttlayout.addWidget(expbtn)

    dial_layout = QtWidgets.QVBoxLayout(dial_widget)
    dial_layout.addWidget(graph_canvas, stretch=1)
    dial_layout.addWidget(ionstable)
    dial_layout.addLayout(buttlayout)
    dial_widget.setFocus()
    dial_widget.show()
    update_fnc()
