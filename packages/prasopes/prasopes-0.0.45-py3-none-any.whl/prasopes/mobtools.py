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
import os.path
import logging
matplotlib.use("Qt5Agg")


logger = logging.getLogger('tofLogger')
settings = cf.settings()



def ionstable_changed(row, col, dsfunc, table):
    if col in (1, 2, 3, 4):
        update_profile(table, row, dsfunc)
    table.blockSignals(True)
    table.item(row, 0).setBackground(QtGui.QBrush(
        QtGui.QColor(*gt.colors[row % len(gt.colors)], alpha=50)))
    table.blockSignals(False)


def pop_dial(dialspect, ionstable, labels, getfnc):
    dialspect.clear()
    gt.pop_plot([], [], dialspect, labels)
    for row in range(ionstable.rowCount()):
        name = ionstable.item(row, 0).text()
        startm = drl.floatize(ionstable, row, 3)\
            - (drl.floatize(ionstable, row, 4) / 2)
        endm = drl.floatize(ionstable, row, 3)\
            + (drl.floatize(ionstable, row, 4) / 2)
        [tstart, tend] = [drl.floatize(ionstable, row, i) for i in (1, 2)]
        spectrum = getfnc(startm, endm, tstart, tend)
        dialspect.plot(spectrum[0], spectrum[1], label=name,
                       color=(gt.colors[row % len(gt.colors)] / 255))
    if ionstable.rowCount():
        dialspect.autoscale(True)
        dialspect.legend(loc=2)
    gt.ann_spec(dialspect, labels)
    dialspect.figure.canvas.draw()
    return


def add_row(dsfunc, dialspect, ionstable):
    """add parent ion to the table"""
    logger.debug("adding line")
    newrow = ionstable.rowCount()

    ionstable.blockSignals(True)

    ionstable.setRowCount(newrow + 1)
    for i in range(5):
        ionstable.setItem(newrow, i, QtWidgets.QTableWidgetItem())
        if newrow != 0:
            val = drl.floatize(ionstable, newrow-1, i)
            if i not in (1, 2, 4):
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
    ionstable_changed(newrow, 1, dsfunc, ionstable)
    return


def remove_rows(ionstable, rows=None):
    logger.info("remowing rows")
    if not rows:
        rows = reversed(list(set(
            map(lambda x: x.row(), ionstable.selectedIndexes()))))
    [ionstable.removeRow(row) for row in rows]
    return


def update_profile(table, row, dsfunc):
    """parent table profile spectrum updating procedure"""
    logger.debug("updating parent table row {} profile".format(row))
    # Dont do anything to graph when the spectrum is not populated
    """if not dataset or isinstance(dataset, ds.ThermoRawDataset):
        return"""
    spectrum = table.cellWidget(row, 5).figure.get_axes()[0]
    spectrum.clear()
    limits = []
    spectra = dsfunc(*[drl.floatize(table, row, i) for i in (1, 2)])
    for i, spectxy in enumerate(spectra):
        massargs = drl.get_subargs(table, row, spectxy[0], 3, 4)
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
