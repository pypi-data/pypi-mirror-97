#!/usr/bin/env python3
from matplotlib.backends.backend_qt5agg import\
        FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtPrintSupport
from prasopes.datasets import ThermoRawDataset
import matplotlib
import numpy as np
import prasopes.datatools as dt
import prasopes.graphtools as gt
import prasopes.filetools as ft
import prasopes.config as cf
import prasopes.reactivitytools as rt
import prasopes.drltools as drl
import prasopes.imagetools as imgt
import os.path
import logging
matplotlib.use("Qt5Agg")


logger = logging.getLogger('drlLogger')


class StretchWidget(QtWidgets.QWidget):
    """horizontal stretch class"""
    def __init__(self):
        super(StretchWidget, self).__init__()
        self._main = QtWidgets.QWidget()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Preferred)


def update_profile(pt, row, dataset):
    """parent table profile spectrum updating procedure"""
    logger.debug("updating parent table row {} profile".format(row))
    # Dont do anything to graph when the spectrum is not populated
    if not dataset:
        return
    spectrum = pt.cellWidget(row, 3).figure.get_axes()[0]
    spectrum.clear()
    limits = []
    spectra = dataset.get_spectra(-np.inf, np.inf)
    for i, spectxy in enumerate(spectra):
        massargs = drl.get_subargs(pt, row, spectxy[0], 1, 2)
        spectrum.plot(spectxy[0], spectxy[1], ':', color='gray')
        spectrum.plot(spectxy[0][massargs], spectxy[1][massargs],
                      color=gt.colors[i % len(gt.colors)]/255)
        limits.append((spectxy[0][massargs[[0, -1]]],
                       max(spectxy[1][massargs])))
    widest = np.argmax([abs(lim[0][1]-lim[0][0]) for lim in limits])
    xmin, xmax = limits[widest][0]
    xexlim = 0.20 if type(dataset) == ThermoRawDataset else 0.02
    xex = max((xmax-xmin)*0.25, xexlim)
    spectrum.set_xlim(xmin-xex, xmax+xex)
    ymax = max(*[lim[1] for lim in limits], 1)
    spectrum.set_ylim(ymax*-0.1, ymax*1.2)
    spectrum.figure.canvas.draw()


def update_drlspectrum(ds, drls, drlspectrum):
    """Generic DRL spectrum updating procedure"""
    logger.info("updating DRL spectrum")
    # Do not do anything when the data set is not populated.
    if not ds:
        return

    names, times, intensities = drl.get_daughterset(ds, drls)
    drlspectrum.clear()
    gt.pop_plot([], [], drlspectrum, drls['graphlabels'])
    drlspectrum.axvline(0, 0, 0.9, color="#FF000088", linestyle=":")

    if drls['cutoff'].value() != 0:
        drlspectrum.axvline(drls['cutoff'].value(), 0, 0.9,
                            color="#0000FF88", linestyle=":")

    i = 0
    for row in range(drls['dt'].rowCount()):
        if drls['dt'].cellWidget(row, 0).checkState() == 2:
            drls['dt'].blockSignals(True)
            drls['dt'].item(row, 0).setBackground(QtGui.QBrush(
                QtGui.QColor(*gt.colors[row % len(gt.colors)], alpha=50)))
            drls['dt'].blockSignals(False)
            label = " {}".format(drls['pt'].item(row, 0).text())
            intensity = intensities[i]
            if drls['rel'].checkState() == 2:
                # Do not divide by 0
                intensity = np.divide(intensity, np.clip(np.sum(
                    intensities, 0), np.finfo(np.float32).eps, None),
                    dtype=np.float64)
            drlspectrum.plot(times, intensity, label=label,
                             color=(gt.colors[row % len(gt.colors)] / 255))
            i += 1
        else:
            drls['dt'].item(row, 0).setBackground(QtGui.QBrush())

    if len(names) != 0:
        gmax = np.amax(intensities)
        if drls['rel'].checkState() == 2:
            gmax = 1
        drlspectrum.set_ylim(top=gmax*1.1, bottom=gmax*-0.01)
        drlspectrum.legend(loc=2)
    drlspectrum.figure.canvas.draw()


def update_corrfors(drls):
    """update corrections selection layout of the daughter table"""
    ionlist = drl.gettableitemlist(drls['pt'])
    for row in range(drls['dt'].rowCount()):
        for i in range(drls['cors'].value()):
            corfor = drls['dt'].cellWidget(row, 1+i*2)
            index = corfor.currentIndex()
            corfor.blockSignals(True)
            corfor.clear()
            corfor.addItem("")
            corfor.addItems(ionlist)
            corfor.setCurrentIndex(index)
            corfor.blockSignals(False)


def ptable_changed(row, column, ds, drls, drlspectrum):
    """routine called by change of the ptable spectra"""
    logger.debug("ptable changed routine called")
    update_corrfors(drls)
    drls['dt'].item(row, 0).setText(drl.gettableitemlist(drls['pt'])[row])
    if column in (1, 2):
        update_profile(drls['pt'], row, ds)


def dtable_changed(row, column, ds, drls, drlspectrum):
    """routine called by change of the dtable spectra"""
    logger.info("Change in the daughter ion table detected")
    if drls['dt'].cellWidget(row, 0).checkState() == 2:
        if (column == 0) or (column % 2 == 0 and drls['dt'].cellWidget(
                row, column-1).currentIndex() != 0):
            update_drlspectrum(ds, drls, drlspectrum)


def corr_changed(correction, ds, drls, drlspectrum):
    """routine called by change of correction for ion"""
    logger.info('''Change of the "correct to" detected''')
    for i in range(drls['dt'].rowCount()):
        for j in range(drls['dt'].columnCount()):
            if correction == drls['dt'].cellWidget(i, 1+j*2):
                row, column = i, 1 + j*2
                logger.debug('''Change of the "correct to" on '''
                             '''row {}, column {}'''.format(
                                 row + 1, column + 1))
    if (drls['dt'].cellWidget(row, 0).checkState() == 2
       and drl.floatize(drls['dt'], row, column+1, False) != 0):
        update_drlspectrum(ds, drls, drlspectrum)


def corcount_changed(ds, drls, drlspectrum):
    """routine called by change of the correction factors count"""
    logger.info('''change in the correction count detected''')
    diff = int(drls['cors'].value() -
               ((drls['dt'].columnCount() - 1) / 2))
    if diff == 0:
        return
    elif diff > 0:
        drls['dt'].blockSignals(True)
        drls['dt'].setColumnCount(1 + (drls['cors'].value() * 2))
        newcors = []
        for col in range(drls['dt'].columnCount() - (diff * 2),
                         drls['dt'].columnCount(), 2):
            for row in range(drls['dt'].rowCount()):
                drls['dt'].setCellWidget(row, col, QtWidgets.QComboBox())
                drls['dt'].cellWidget(row, col).setFrame(False)
                drls['dt'].cellWidget(row, col).setFocusPolicy(
                        QtCore.Qt.NoFocus)
                drls['dt'].setItem(row, col+1, QtWidgets.QTableWidgetItem())
                newcors.append(drls['dt'].cellWidget(row, col))
        list(map(lambda x: x.currentIndexChanged.connect(
            lambda: corr_changed(x, ds, drls, drlspectrum)), newcors))
        update_corrfors(drls)
        dcolums = ["Name"]
        for i in range(drls['cors'].value()):
            dcolums.append("corrected for ({})".format(i+1))
            dcolums.append("factor ({})".format(i+1))
        drls['dt'].setHorizontalHeaderLabels(dcolums)
        drls['dt'].blockSignals(False)
    else:
        drls['dt'].blockSignals(True)
        drls['dt'].setColumnCount(1 + (drls['cors'].value() * 2))
        drls['dt'].blockSignals(False)
        update_drlspectrum(ds, drls, drlspectrum)


def remove_rows(ds, drls, drlspectrum, rows=None):
    logger.info("remowing rows")
    if not rows:
        rows = reversed(list(set(
            map(lambda x: x.row(), drls['pt'].selectedIndexes()))))
    cors = []
    for row in rows:
        drls['dt'].cellWidget(row, 0).setCheckState(0)
        drls['dt'].removeRow(row)
        drls['pt'].removeRow(row)
        for i in range(drls['dt'].rowCount()):
            for cornum in range(drls['cors'].value()):
                corfor = drls['dt'].cellWidget(i, 1+cornum*2)
                cors.append(corfor)
                corfor.disconnect()
                index = corfor.currentIndex()
                corfor.clear()
                corfor.addItem("")
                corfor.addItems(drl.gettableitemlist(drls['pt']))
                if index == row+1:
                    corfor.setCurrentIndex(0)
                    corr_changed(corfor, ds, drls, drlspectrum)
                elif index > row+1:
                    corfor.setCurrentIndex(index-1)
                else:
                    corfor.setCurrentIndex(index)
        list(map(lambda x: x.currentIndexChanged.connect(
            lambda: corr_changed(x, ds, drls, drlspectrum)), cors))


def add_line(ds, drls, drlspectrum):
    """add parent ion to the table"""
    logger.debug("adding line")
    newrow = drls['pt'].rowCount()

    drls['pt'].blockSignals(True)
    drls['dt'].blockSignals(True)

    drls['pt'].setRowCount(newrow + 1)
    for i in range(3):
        drls['pt'].setItem(newrow, i, QtWidgets.QTableWidgetItem())
        if newrow != 0:
            val = drl.floatize(drls['pt'], newrow-1, i)
            if i != 2:
                val = val+1
            drls['pt'].item(newrow, i).setText(str(val))

    ion_graph = Figure(figsize=(3, 1.5), dpi=100, facecolor="None")
    ion_graph.add_subplot(111, facecolor=(1, 1, 1, 0.8),
                          position=(-0.01, -0.01, 1.02, 1.02))
    graph_canvas = FigureCanvas(ion_graph)
    graph_canvas.setStyleSheet("background-color:transparent;")
    graph_canvas.setAutoFillBackground(False)
    drls['pt'].setCellWidget(newrow, 3, graph_canvas)

    drls['dt'].setRowCount(newrow + 1)
    checkbox = QtWidgets.QCheckBox()
    checkbox.setFocusProxy(drls['dt'])
    dname = QtWidgets.QTableWidgetItem()
    dname.setFlags(dname.flags() & ~QtCore.Qt.ItemIsEditable)
    dname.setTextAlignment(QtCore.Qt.AlignRight)
    drls['dt'].setItem(newrow, 0, dname)
    drls['dt'].setCellWidget(newrow, 0, checkbox)

    for i in range(drls['cors'].value()):
        col = 1+i*2
        drls['dt'].setCellWidget(newrow, col, QtWidgets.QComboBox())
        drls['dt'].cellWidget(newrow, col).setFocusPolicy(QtCore.Qt.NoFocus)
        drls['dt'].cellWidget(newrow, col).setFrame(False)
        drls['dt'].setItem(newrow, col+1, QtWidgets.QTableWidgetItem())

    drls['pt'].blockSignals(False)
    drls['dt'].blockSignals(False)

    cors = list(map(lambda x: drls['dt'].cellWidget(newrow, 1+x*2),
                    range(drls['cors'].value())))
    list(map(lambda x: x.currentIndexChanged.connect(
        lambda: corr_changed(x, ds, drls, drlspectrum)), cors))

    ptable_changed(newrow, 1, ds, drls, drlspectrum)
    select_all_btn_up(ds, drls, drlspectrum)

    checkbox.stateChanged.connect(lambda: update_drlspectrum(
        ds, drls, drlspectrum))
    checkbox.stateChanged.connect(lambda: select_all_btn_up(
        ds, drls, drlspectrum))


def load_drltables(parent, dataset, drls, drlspectrum):
    filename = QtWidgets.QFileDialog.getOpenFileName(
            caption="Load DRL config tables",
            filter="comma-separated values (*.csv)",
            directory=cf.settings().value("open_folder"))[0]
    if filename != '':
        names = []
        masses = []
        peak_widths = []
        states = []
        corrections = []

        with open(filename, 'r') as cfile:
            rawdata = cfile.read().splitlines()
        for i in range(len(rawdata[0].split(","))-4):
            corrections.append([])
        for i in range(1, len(rawdata)):
            rawline = rawdata[i].split(",")
            n = len(rawline)
            if n < 4 or not n % 2 == 0 or (rawline[3] not in map(
                str, range(3))) or not (set(map(int, rawline[4:n:2]))
                                        & set(range(-1, n)) or (n == 4)):
                QtWidgets.QMessageBox.warning(
                    parent, "Load DRL config tables",
                    "Wrong or corrupted config file.\n"
                    "Error encountered on line {}.\n"
                    "Cancelling request.".format(i+1))
                return
            for j, k in enumerate((names, masses, peak_widths,
                                   states, *corrections)):
                if len(rawline) > j:
                    k.append(rawline[j])
        for row in reversed(range(drls['pt'].rowCount())):
            drls['dt'].removeRow(row)
            drls['pt'].removeRow(row)
        # first populate only the parent table
        for i in range(len(names)):
            add_line(dataset, drls, drlspectrum)
            drls['pt'].item(i, 0).setText(names[i])
            drls['pt'].item(i, 1).setText(masses[i])
            drls['pt'].item(i, 2).setText(peak_widths[i])
        # and after that the daughter table
        drls['cors'].setValue(int((len(corrections) / 2)))
        for i in range(len(names)):
            for j in range(int((len(rawline)-4)/2)):
                drls['dt'].cellWidget(i, 1+j*2).setCurrentIndex(
                    int(corrections[0+j*2][i]))
                drls['dt'].item(i, 2+j*2).setText(corrections[1+j*2][i])
            drls['dt'].cellWidget(i, 0).setCheckState(int(states[i]))


def save_drlconfig(drls, parent, exp_f_name=None):
    """safe DRL table layout so it can be summoned when needed"""
    if not exp_f_name:
        exp_f_name = ft.get_save_filename(
            "Save DRL table layout", "comma-separated values (*.csv)",
            "csv", parent)
    if exp_f_name != '':
        corlist = []
        for i in range(drls['cors'].value()):
            corlist.append("corrected_to_{}, factor_{} ".format(
                i+1, i+1))
        cortext = ", ".join(corlist)
        expf = open(exp_f_name, 'w')
        expf.write("#ion_name, m/z, peak_width, visible,"
                   "{}\n".format(cortext))
        for row in range(drls['pt'].rowCount()):
            vals = []
            for i in range(3):
                vals.append(drls['pt'].item(row, i).text())
            vals.append(drls['dt'].cellWidget(row, 0).checkState())
            for i in range(drls['cors'].value()):
                vals.append(drls['dt'].cellWidget(row, 1+i*2).currentIndex())
                vals.append(drls['dt'].item(row, 2+i*2).text())
            expf.write("{}\n".format((",".join(map(str, vals)))))
        expf.close()


def export_drlspectrum(parent, ds, drls):
    if not ds:
        QtWidgets.QMessageBox.warning(
            None, "Export DRL dat aset",
            "No file opened. Nothing to export, canceling request")
        return
    names, times, intensities = drl.get_daughterset(ds, drls)
    if drls['cutoff'].value() == 0:
        subset = np.where(times > 0)[0]
    else:
        subset = np.where((times > 0) & (times < drls['cutoff'].value()))[0]
    times = times[subset]
    intensities = list(map(lambda x: x[subset], intensities))

    pnames, ptimes, pintensities = drl.get_parentset(ds, drls)
    if names == []:
        QtWidgets.QMessageBox.warning(
            None, "Export DRL data set",
            "No rows in the Corrected ions table selected. "
            "Nothing to export, canceling request")
        return
    fname = QtWidgets.QFileDialog.getSaveFileName(
            None, "Export DRL data", options=(
                QtWidgets.QFileDialog.DontConfirmOverwrite |
                QtWidgets.QFileDialog.HideNameFilterDetails),
            directory=ds.filename[0][:-4])[0]
    if fname == '':
        return
    exp_f_name = list(map(lambda x: "{}/{}-{}.csv".format(
        fname, os.path.basename(fname), x),
        ["raw", "corrected", "input"]))
    for name in exp_f_name:
        if os.path.isfile(name):
            quest = QtWidgets.QMessageBox.warning(
                parent, "Export DRL data",
                "File {} already exists in the filesystem.\n"
                "Do you want to overwrite it?"
                .format(os.path.basename(name)),
                QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if quest == QtWidgets.QMessageBox.No:
                return
    if not os.path.exists(fname):
        os.makedirs(fname)
    for i, table in enumerate([[pnames, pintensities],
                               [names, intensities]]):
        expf = open(exp_f_name[i], 'w')
        expf.write("times,{}\n".format((",".join(table[0]))))
        expf.write("timeshift = {}, cutoff = {}\n".format(
            drls['tshift'].value(), drls['cutoff'].value()))
        for j in range(len(times)):
            dataset = list()
            dataset.append(times[j])
            for intensity in table[1]:
                dataset.append(intensity[j])
            expf.write("{}\n".format((",".join(map(str, dataset)))))
        expf.close()
    save_drlconfig(drls, parent, exp_f_name[2])


def print_graph(ds, drls):
    printfig = Figure(figsize=(5, 2), dpi=100)
    printplot = printfig.add_subplot(111)
    printcanvas = FigureCanvas(printfig)
    gt.pop_plot([], [], printplot, drls['graphlabels'])
    update_drlspectrum(ds, drls, printplot)
    widget = QtWidgets.QDialog(None, windowTitle='Print preview')
    layout = QtWidgets.QVBoxLayout(widget)
    layout.addWidget(printcanvas)
    widget.resize(600, 400)
    widget.show()
    dialog = QtPrintSupport.QPrintDialog()
    if dialog.exec_() == QtWidgets.QDialog.Accepted:
        printcanvas.render(dialog.printer())
    widget.close()


def clip_range(drls):
    """copy selected part of the table"""
    logger.debug("copying selected table cells to clipboard")
    activeObject = QtWidgets.QApplication.focusWidget()
    if activeObject in (drls['pt'], drls['dt']):
        table = activeObject
        if len(table.selectedRanges()) == 0:
            return
        if len(table.selectedRanges()) > 1:
            QtWidgets.QMessageBox.warning(
                None, "Operation not supported",
                "Operation not supported for multiple ranges,\n"
                "cancelling request")
            return
        sr = table.selectedRanges()[0]
        rows = []
        for row in range(sr.topRow(), sr.bottomRow() + 1):
            line = []
            for col in range(sr.leftColumn(), sr.rightColumn() + 1):
                if isinstance(table.cellWidget(row, col),
                              QtWidgets.QComboBox):
                    line.append(
                        table.cellWidget(row, col).currentText())
                elif isinstance(table.item(row, col),
                                QtWidgets.QTableWidgetItem):
                    line.append(table.item(row, col).text())
            rows.append(("\t").join(line))
        QtWidgets.QApplication.clipboard().clear()
        QtWidgets.QApplication.clipboard().setText(("\n").join(rows))


def paste_clip(ds, drls, drlspectrum):
    logger.debug("pasting data from clipboard")
    activeObject = QtWidgets.QApplication.focusWidget()
    if activeObject in (drls['pt'], drls['dt'])\
            and activeObject.selectedRanges() != []:
        table = activeObject
        if len(table.selectedRanges()) > 1:
            QtWidgets.QMessageBox.warning(
                None, "Operation not supported",
                "Operation not supported for multiple ranges,\n"
                "cancelling request")
            return
        cliptext = QtWidgets.QApplication.clipboard().text()
        rows = cliptext.split("\n")
        startrow = table.selectedRanges()[0].topRow()
        startcol = table.selectedRanges()[0].leftColumn()
        for i, row in enumerate(rows, start=startrow):
            cols = row.split("\t")
            for j, col in enumerate(cols, start=startcol):
                if table == drls['pt'] and j < 3:
                    if i >= (table.rowCount()):
                        add_line(ds, drls, drlspectrum)
                    table.item(i, j).setText(col)
                if table == drls['dt'] and j != 0 and j % 2 == 0\
                        and i < table.rowCount():
                    table.item(i, j).setText(col)


def paint_override(self, ds, drls, drlspectrum):
    update_drlspectrum(ds, drls, self.plot)
    self.plot.set_xlim(drlspectrum.get_xlim())
    self.plot.set_ylim(drlspectrum.get_ylim())
    self.plot.figure.canvas.draw()


def key_pressed(event, ds, drls, drlspectrum):
    if event.key() == QtCore.Qt.Key_Delete:
        rows = reversed(list(map(
            lambda x: x.row(), drls['pt'].selectionModel().selectedRows())))
        remove_rows(ds, drls, drlspectrum, rows)
    if event.key() == QtCore.Qt.Key_F5:
        update_drlspectrum(ds, drls, drlspectrum)
        for row in range(drls['pt'].rowCount()):
            update_profile(drls['pt'], row, ds)
    if event.key() == QtCore.Qt.Key_C\
            and event.modifiers().__int__() == QtCore.Qt.ControlModifier:
        if drls['dt'].underMouse() or drls['pt'].underMouse():
            clip_range(drls)
        else:
            imggen = imgt.ImagePainter("drlspec")
            imggen.popfig = lambda: paint_override(
                    imggen, ds, drls, drlspectrum)
            imggen.clip()
    if event.key() == QtCore.Qt.Key_V\
            and event.modifiers().__int__() == QtCore.Qt.ControlModifier:
        paste_clip(ds, drls, drlspectrum)


def select_all_btn_up(ds, drls, drlspectrum, state=None):
    logger.info('''Change of the select-all button detected''')
    if state in (0, 2):
        for row in range(drls['dt'].rowCount()):
            drls['dt'].cellWidget(row, 0).blockSignals(True)
            drls['dt'].cellWidget(row, 0).setCheckState(state)
            drls['dt'].cellWidget(row, 0).blockSignals(False)
        update_drlspectrum(ds, drls, drlspectrum)
    elif state == 1:
        drls['checkAll'].setCheckState(2)
    else:
        drls['checkAll'].blockSignals(True)
        btns = [drls['dt'].cellWidget(row, 0).checkState()
                for row in range(drls['dt'].rowCount())]
        if all(btns):
            drls['checkAll'].setCheckState(2)
        elif any(btns):
            drls['checkAll'].setCheckState(1)
        else:
            drls['checkAll'].setCheckState(0)
        drls['checkAll'].blockSignals(False)


def main_window(parent, augCanvas, update_signal):
    """constructs a dialog window"""
    ds = augCanvas.ds
    cache = augCanvas.drlcache

    def onclose(widget, event, buffer, drls,
                canvas, update_fnc, update_ptrows):
        buffer[0], buffer[1] = drls, canvas
        update_signal.signal.disconnect(update_fnc)
        update_signal.signal.disconnect(update_ptrows)
        QtWidgets.QMainWindow.closeEvent(widget, event)

    def update_fnc():
        logger.info('''udate routine called''')
        update_drlspectrum(ds, drls, chromplot)

    def update_ptrows():
        for row in range(drls['pt'].rowCount()):
            ptable_changed(row, 1, ds, drls, chromplot)

    if cache == [None, None]:
        # pt = parenttable
        # dt = daughtertable
        drls = dict(pt=None, dt=None, tshift=None, cutoff=None, cors=None,
                    rel=None, checkAll=None)
        drls['tshift'] = QtWidgets.QDoubleSpinBox(
            minimum=-100, maximum=1440, decimals=3)
        drls['cutoff'] = QtWidgets.QDoubleSpinBox(
            minimum=0, maximum=1440, decimals=3)
        drls['rel'] = QtWidgets.QCheckBox("Steady state approximation")
        drls['checkAll'] = QtWidgets.QCheckBox("Select all")
        drls['cors'] = QtWidgets.QSpinBox(minimum=0)
        drls['cors'].setValue(3)
        drls['graphlabels'] = dict(line=None, name="", xlabel="time(min)",
                                   ylabel="relative intensity")

        dial_graph = Figure(figsize=(5, 2), dpi=100, facecolor="None")
        chromplot = dial_graph.add_subplot(111, facecolor=(1, 1, 1, 0.8))
        graph_canvas = FigureCanvas(dial_graph)
        graph_canvas.setStyleSheet("background-color:transparent;")
        graph_canvas.setAutoFillBackground(False)
        gt.pan_factory(chromplot)
        gt.zoom_factory(chromplot, 1.15)
        gt.pop_plot([], [], chromplot, drls['graphlabels'])

        dcolums = ["Name"]
        for i in range(drls['cors'].value()):
            dcolums.append("corrected for ({})".format(i+1))
            dcolums.append("factor ({})".format(i+1))
        drls['dt'] = dt.table(dcolums)
        drls['pt'] = dt.table(["Name", "Mass (m/z)", "Peak width",
                               "Profile"])
        # TODO: DIRTY, DIRTY, DIRTY !!! Do it nicer when I'll know how
        [drls['dt'].horizontalHeader().setSectionResizeMode(
             n, QtWidgets.QHeaderView.Interactive) for n in range(
                    drls['dt'].columnCount())]
        add_line(ds, drls, chromplot)
    else:
        drls = cache[0]
        graph_canvas = cache[1]
        chromplot = graph_canvas.figure.axes[0]

    window = QtWidgets.QMainWindow(
        parent, windowTitle='Delayed reactant labeling')
    main_widget = QtWidgets.QWidget(window)
    window.setCentralWidget(main_widget)

    window.closeEvent = lambda event: onclose(
        window, event, cache, drls, graph_canvas, update_fnc, update_ptrows)

    time_title = QtWidgets.QLabel("Time shift (min):")
    cutoff_title = QtWidgets.QLabel("Cut off (min):")

    drl_load = QtWidgets.QPushButton("&Load")
    drl_save = QtWidgets.QPushButton("&Save")
    drl_export = QtWidgets.QPushButton("&Export")
    drl_reactivity = QtWidgets.QPushButton("&Reactivity")
    drl_print = QtWidgets.QPushButton("&Print")
    close = QtWidgets.QPushButton("&Close")
    close.clicked.connect(window.close)

    btn_add = QtWidgets.QPushButton("&Add")
    btn_rem = QtWidgets.QPushButton("Remove")

    window.keyPressEvent = lambda event: key_pressed(
        event, ds, drls, chromplot)

    btn_add.clicked.connect(lambda: add_line(
        ds, drls, chromplot))
    btn_rem.clicked.connect(lambda: remove_rows(
        ds, drls, chromplot))
    drl_load.clicked.connect(lambda: load_drltables(
        main_widget, ds, drls, chromplot))
    drl_save.clicked.connect(lambda: save_drlconfig(
        drls, main_widget))
    drl_print.clicked.connect(lambda: print_graph(ds, drls))
    drl_export.clicked.connect(lambda: export_drlspectrum(
        main_widget, ds, drls))
    drl_reactivity.clicked.connect(lambda: rt.main_window(
        parent, augCanvas, update_signal, drls))

    drls['pt'].itemChanged.connect(lambda item: ptable_changed(
        item.row(), item.column(), ds, drls, chromplot))
    drls['dt'].itemChanged.connect(lambda item: dtable_changed(
        item.row(), item.column(), ds, drls, chromplot))
    drls['tshift'].valueChanged.connect(update_fnc)
    drls['cutoff'].valueChanged.connect(update_fnc)
    drls['cors'].valueChanged.connect(lambda: corcount_changed(
        ds, drls, chromplot))
    drls['rel'].stateChanged.connect(update_fnc)
    drls['checkAll'].stateChanged.connect(
        lambda state: select_all_btn_up(ds, drls, chromplot, state))
    update_signal.signal.connect(update_fnc)
    update_signal.signal.connect(update_ptrows)

    actionBar = QtWidgets.QToolBar(window)
    window.addToolBar(QtCore.Qt.BottomToolBarArea, actionBar)
    actionBar.setAllowedAreas(QtCore.Qt.BottomToolBarArea)
    actionBar.setFloatable(False)
    actionBar.setMovable(False)
    actionBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
    actionBar.addWidget(drl_load)
    actionBar.addWidget(drl_save)
    actionBar.addWidget(drl_print)
    actionBar.addWidget(StretchWidget())
    actionBar.addWidget(drl_reactivity)
    actionBar.addWidget(StretchWidget())
    actionBar.addWidget(drl_export)
    actionBar.addWidget(close)

    dtdock = QtWidgets.QDockWidget()
    dtdock.setWidget(QtWidgets.QWidget())
    dtdock_layout = QtWidgets.QVBoxLayout(dtdock.widget())
    dtdock.setWindowTitle("Corrected ions table")
    dt_butlayout = QtWidgets.QHBoxLayout()
    dt_butlayout.addWidget(drls['checkAll'])
    dt_butlayout.addWidget(StretchWidget())
    dt_butlayout.addWidget(QtWidgets.QLabel("Number of corrections:"))
    dt_butlayout.addWidget(drls['cors'])
    dt_butlayout.addWidget(StretchWidget())
    dtdock_layout.addLayout(dt_butlayout)
    dtdock_layout.addWidget(drls['dt'])
    window.addDockWidget(QtCore.Qt.BottomDockWidgetArea, dtdock)

    ptdock = QtWidgets.QDockWidget()
    ptdock.setWidget(QtWidgets.QWidget())
    ptdock_layout = QtWidgets.QVBoxLayout(ptdock.widget())
    ptdock.setWindowTitle("Raw ions table")
    ptdock_layout.addWidget(drls['pt'])
    pt_butlayout = QtWidgets.QHBoxLayout()
    pt_butlayout.addWidget(btn_add)
    pt_butlayout.addWidget(btn_rem)
    pt_butlayout.addStretch(0)
    ptdock_layout.addLayout(pt_butlayout)
    window.addDockWidget(QtCore.Qt.RightDockWidgetArea, ptdock)

    main_layout = QtWidgets.QVBoxLayout(main_widget)
    graphparams_layout = QtWidgets.QHBoxLayout()
    main_layout.addWidget(graph_canvas, stretch=1)
    main_layout.addLayout(graphparams_layout)
    graphparams_layout.addWidget(time_title)
    graphparams_layout.addWidget(drls['tshift'])
    graphparams_layout.addStretch(1)
    graphparams_layout.addWidget(cutoff_title)
    graphparams_layout.addWidget(drls['cutoff'])
    graphparams_layout.addStretch(1)
    graphparams_layout.addWidget(drls['rel'])
    graphparams_layout.addStretch(1)

    window.show()
