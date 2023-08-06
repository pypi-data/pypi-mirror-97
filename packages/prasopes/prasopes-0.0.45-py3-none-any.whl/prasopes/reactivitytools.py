#!/usr/bin/env python3
from matplotlib.backends.backend_qt5agg import\
        FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtCore
from PyQt5 import QtWidgets
import matplotlib
import numpy as np
import prasopes.datatools as dt
import prasopes.graphtools as gt
import prasopes.filetools as ft
import prasopes.config as cf
import prasopes.drltools as drl
import prasopes.imagetools as imgt
import os.path
import logging
matplotlib.use("Qt5Agg")


logger = logging.getLogger('reactivityLogger')
settings = cf.settings()


class reactivityParam(QtWidgets.QHBoxLayout):
    """Layout with annotated text/spin box connected to settings"""
    def __init__(self, parselect, tabber, type, valname, vallabel,
                 min=None, max=None, decimals=4):
        super().__init__()
        self.valname = valname
        self.addWidget(QtWidgets.QLabel(vallabel, alignment=130))

        def getconfval(name=self.valname, parselect=parselect, tabber=tabber):
            ind = -1 if tabber.currentIndex() else parselect.currentIndex()
            par = "reactivity/{}_par{}".format(name, ind)
            logger.debug("Getting "+par)
            return settings.value(par, type=type)

        def setconfval(x, name=self.valname,
                       parselect=parselect, tabber=tabber):
            ind = -1 if tabber.currentIndex() else parselect.currentIndex()
            par = "reactivity/{}_par{}".format(name, ind)
            logger.debug("Setting "+par)
            settings.setValue(par, x)
        if type in (int, float):
            if type == float:
                self.dial = QtWidgets.QDoubleSpinBox(
                    decimals=decimals, minimum=float(min or "-inf"),
                    maximum=float(max or "inf"))
            elif type == int:
                self.dial = QtWidgets.QSpinBox(
                    minimum=(min or 0), maximum=(max or 255))
            self.dial.setValue(getconfval())
            self.dial.valueChanged.connect(setconfval)
            parselect.currentIndexChanged.connect(
                lambda _: self.dial.setValue(getconfval()))
            tabber.currentChanged.connect(
                lambda _: self.dial.setValue(getconfval()))
        elif type == str:
            self.dial = QtWidgets.QLineEdit()
            self.dial.setText(getconfval())
            self.dial.textChanged.connect(setconfval)
            parselect.currentIndexChanged.connect(
                lambda _: self.dial.setText(getconfval()))
            tabber.currentChanged.connect(
                lambda _: self.dial.setText(getconfval()))
        else:
            raise ValueError("excepted 'float', 'str' or 'int' as type")
        self.addWidget(self.dial, stretch=1)


def paint_override(self, augCanvas, drls, grph, labels, parselect):
    pop_dial(augCanvas, drls, self.plot, labels, parselect)
    self.plot.set_xlim(grph.get_xlim())
    self.plot.set_ylim(grph.get_ylim())


def key_pressed(event, augCanvas, drls, grph, labels, parselect):
    if event.key() == QtCore.Qt.Key_C:
        if event.modifiers().__int__() == QtCore.Qt.ControlModifier:
            imggen = imgt.ImagePainter("zcespec")
            imggen.popfig = lambda: paint_override(
                    imggen, augCanvas, drls, grph, labels, parselect)
            imggen.clip()


def export_dial(augCanvas, drls, grph, labels, parselect):
    """exports the reactivity into the .dat file format"""
    if not augCanvas.ds or not augCanvas.ds.params:
        QtWidgets.QMessageBox.warning(
            None, "Export spectrum",
            "Nothing to export, cancelling request")
        return
    exp_f_name = ft.get_save_filename(
        "Export spectrum", "dat table (*.dat)", "dat", None)
    if exp_f_name != '':
        names = ["pressure", "rel._intensity"]
        units = ["mTorr", ""]
        description = os.path.basename(augCanvas.ds.filename) + " " +\
            " -- ".join([line._label for line in grph.get_lines()])
        expf = open(exp_f_name, 'w')
        expf.write(dt.specttostr(grph, " ", names, units, description))
        expf.close


def update_parselect(augCanvas, parselect):
    # Do not do anything when data set is not populated
    if not augCanvas.ds or not augCanvas.ds.params:
        return
    index = parselect.currentIndex()
    if index == -1:
        index = settings.value("reactivity/index", type=int)
    parlist = [": ".join([str(i), j]) for i, j in
               enumerate(augCanvas.ds.params[0])]
    parselect.clear()
    parselect.addItems(parlist)
    if index <= len(parlist):
        parselect.setCurrentIndex(index)


def tab_changed(fnc, index):
    settings.setValue("reactivity/activetab", index)
    fnc()


def pop_dial(augCanvas, drls, graph, labels, parselect):
    logger.debug("populating reactivity dialog")
    # Do not do anything when data set is not populated
    if not augCanvas.ds or not augCanvas.ds.params or not augCanvas.ds.headers:
        return

    def getconfval(name, type, parselect=parselect):
        parind = -1 if settings.value("reactivity/activetab")\
                else parselect.currentIndex()
        par = "reactivity/{}_par{}".format(name, parind)
        logger.debug("Getting "+par)
        return settings.value(par, type=type)
    graph.clear()
    labels['xlabel'] = getconfval("xlabel", str)
    gt.pop_plot([], [], graph, labels)
    names, times, intensities = drl.get_daughterset(augCanvas.ds, drls)
    colorargs = [row for row in range(drls['dt'].rowCount())
                 if drls['dt'].cellWidget(row, 0).checkState() == 2]
    params = augCanvas.ds.params[1]
    headers = np.concatenate(augCanvas.ds.headers, axis=0)
    parlen = len(params)
    if len(names) < 2:
        return
    try:
        float(params[0][parselect.currentIndex()])
    except ValueError:
        QtWidgets.QMessageBox.warning(
                None, "Unsupported parameter",
                "This parameter is not supported for mathematical evaluation\n"
                "or no parameters were loaded. Please change the parameter")
        return

    pressures = []
    lastpos = 0
    coef1 = getconfval("coef_a", float)
    coef2 = getconfval("coef_b", float)
    alpha = getconfval("transparency", float)
    transcolors = [np.append(i, alpha) for i in gt.colors]
    if not settings.value("reactivity/activetab"):
        for time in times:
            toavg = []
            for i in range(lastpos, parlen):
                if float(params[i][0]) == time:
                    toavg.append((float(
                        params[i][parselect.currentIndex()])-coef1)*coef2)
                    lastpos = i
                elif float(params[i][0]) > time and i > 0:
                    # i>0 condition to handle invalid first scan.
                    # (was observed in-wild on TSQ once)
                    break
            if len(toavg) != 0:
                pressures.append([time, np.average(toavg)])
        if len(pressures) == 0:
            QtWidgets.QMessageBox.critical(
                None, "No times loaded",
                "Did not located any valid parameters.\n"
                "It is either start of the acquisition,\n"
                "or the timestamps has been corrupted.")
            return
        nptpressures = np.asarray(pressures).T[0]
        goodtimes = np.where([t in nptpressures for t in times])
    for i in range(1, len(intensities)):
        label = drls['pt'].item(colorargs[i], 0).text()
        relint = np.divide(intensities[i], np.clip(np.sum(
            intensities, 0), np.finfo(np.float32).eps, None),
            dtype=np.float64)
        if not settings.value("reactivity/activetab"):
            graph.plot(np.asarray(pressures).T[1], relint[goodtimes],
                       label=label, color=(transcolors[
                           colorargs[i] % len(transcolors)] / 255), marker=".",
                       markersize=getconfval("markersize", float),
                       linestyle="None")
        else:
            transheads = headers.T
            hdrindex = min(getconfval("headerindex", int), len(headers.T)-1)
            graph.plot(transheads[hdrindex], relint,
                       label=label, color=(transcolors[
                           colorargs[i] % len(transcolors)] / 255), marker=".",
                       markersize=getconfval("markersize", float),
                       linestyle="None")

    if getconfval("showlabel", int):
        legend = graph.legend(loc=getconfval("labelloc", int))
        [lh._legmarker.set_alpha(1) for lh in legend.legendHandles]
    graph.text(0, 0.975, getconfval("figann", str), va="top",
               transform=graph.figure.transFigure, in_layout=False)

    graph.autoscale(True)
    graph.figure.canvas.draw()


def main_window(parent, augCanvas, update_signal, drls):
    """constructs a dialog window"""
    reactlabels = dict(name="", xlabel="pressure (mT)",
                       ylabel="$Intensity$ $\\it→$")

    def onclose(widget, event, update_fnc):
        logger.debug("ZCE window custom close routine called")
        update_signal.signal.disconnect(update_fnc)
        QtWidgets.QDialog.closeEvent(widget, event)

    def update_fnc():
        pop_dial(augCanvas, drls, dialspect, reactlabels, parselect)

    dial_widget = QtWidgets.QDialog(
            parent, windowTitle='TSQ reactivity interpreter')
    dial_widget.closeEvent = lambda event: onclose(
        dial_widget, event, update_fnc)
    update_signal.signal.connect(update_fnc)
    dial_graph = Figure(figsize=(5, 2), dpi=100, facecolor="None",
                        constrained_layout=True)
    dialspect = dial_graph.add_subplot(111, facecolor=(1, 1, 1, 0.8))
    graph_canvas = FigureCanvas(dial_graph)
    graph_canvas.setStyleSheet("background-color:transparent;")
    graph_canvas.setAutoFillBackground(False)

    gt.zoom_factory(dialspect, 1.15, reactlabels)
    gt.pan_factory(dialspect, reactlabels)

    tabberlabel = QtWidgets.QLabel("Operate on:")
    tabber = QtWidgets.QTabWidget()

    parselect_widget = QtWidgets.QWidget()
    parselect_layout = QtWidgets.QVBoxLayout(parselect_widget)
    parselect = QtWidgets.QComboBox()
    update_parselect(augCanvas, parselect)
    parselect.currentIndexChanged.connect(lambda x: settings.setValue(
        "reactivity/index", x))
    parselect_layout.addWidget(parselect)

    headerselect = QtWidgets.QWidget()
    hdrselect_layout = QtWidgets.QVBoxLayout(headerselect)
    hdrtext = QtWidgets.QLabel(
        "Please select the index of header variable you want to operate on. "
        "If the index number will be higher than the highest active index, "
        "last parameter will be used")
    hdrtext.setWordWrap(True)
    hdrindex = reactivityParam(
            parselect, tabber, int, "headerindex", "Index (0-n): ", 0)
    hdrselect_layout.addWidget(hdrtext)
    hdrselect_layout.addLayout(hdrindex)

    formula = QtWidgets.QLabel(
        "Formula for the x-axis: (Parameter - a) * b")
    xannlayout = reactivityParam(parselect, tabber, str,
                                 "xlabel", "x axis label:")
    xannlayout.addStretch()
    figann = reactivityParam(parselect, tabber, str,
                             "figann", "Figure annotation:")
    translayout = reactivityParam(parselect, tabber, int, "transparency",
                                  "Transparency (0-255): ", 0, 255)
    translayout.addStretch()
    labelloclayout = reactivityParam(
        parselect, tabber, int, "labelloc", "Label location (0-10): ", 0, 10)
    layouts = [xannlayout, figann, translayout, labelloclayout]
    layouts.append(reactivityParam(
        parselect, tabber, int, "showlabel", "Show Label? (0-1): ", 0, 1))
    layouts.append(reactivityParam(
        parselect, tabber, float, "markersize", "dot size: ", 0))
    layouts.append(reactivityParam(parselect, tabber, float, "coef_a", "a: "))
    layouts.append(reactivityParam(parselect, tabber, float, "coef_b", "b: "))

    pushbtn = QtWidgets.QPushButton("Update")
    pushbtn.clicked.connect(lambda: update_fnc())

    expbtn = QtWidgets.QPushButton("Export")
    expbtn.clicked.connect(lambda: export_dial(
        augCanvas, drls, dialspect, reactlabels, parselect))

    buttlayout = QtWidgets.QHBoxLayout()
    buttlayout.addWidget(pushbtn)
    buttlayout.addStretch()
    buttlayout.addWidget(expbtn)
    layouts.append(buttlayout)

    dial_widget.keyPressEvent = lambda event: key_pressed(
            event, augCanvas, drls, dialspect, reactlabels, parselect)

    tabber.addTab(parselect_widget, "Parameter")
    tabber.addTab(headerselect, "Header")
    tabber.setCurrentIndex(settings.value("reactivity/activetab", type=int))
    tabber.currentChanged.connect(
            lambda index: tab_changed(lambda: update_fnc(), index))

    dial_layout = QtWidgets.QVBoxLayout(dial_widget)
    dial_layout.addWidget(graph_canvas, stretch=1)
    dial_layout.addWidget(tabberlabel)
    dial_layout.addWidget(tabber)
    dial_layout.addWidget(formula)
    [dial_layout.addLayout(i) for i in layouts]
    dial_widget.setFocus()
    dial_widget.show()
    update_fnc()
