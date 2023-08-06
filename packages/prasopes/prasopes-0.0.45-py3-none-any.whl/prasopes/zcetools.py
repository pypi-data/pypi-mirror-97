from matplotlib.backends.backend_qt5agg import\
        FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtPrintSupport
from prasopes.zcetools_help import helpstr
import numpy as np
import prasopes.graphtools as gt
import prasopes.filetools as ft
import prasopes.imagetools as imgt
import os.path
import logging


logger = logging.getLogger('zceLogger')


def pop_dial(zcespec, gradspect, data_set, coff_d, grad_d,
             textfield, parent):
    logger.debug("populating ZCE dialog")
    if data_set is None:
        QtWidgets.QMessageBox.warning(
            parent, "ZCE calculation",
            "No spectrum opened, nothing to display")
        return
    zcespec.clear()
    gradspect.clear()

    masses, coff_y = data_set.get_spectra()[0]
    coff_x = masses - 196
    grad_x = coff_x
    halfl = int(len(grad_x)/2)
    grad_y = -np.gradient(coff_y)\
        if np.sum(coff_y[:halfl]) > np.sum(coff_y[halfl:])\
        else np.gradient(coff_y)
    gradspect.axhline(0, color="#FF000088", linestyle=":")
    zcespec.axhline(0, color="#0000FF88", linestyle=":")
    gt.pop_plot(coff_x, coff_y, zcespec, coff_d)
    gt.pop_plot(grad_x, grad_y, gradspect, grad_d)
    gradspect.lines[-1].set_color("red")
    gradspect.set_ylim(bottom=gradspect.get_ylim()[1] * -0.1)
    zcespec.set_title("COFF", loc="center")

    maxarg = np.argmax(grad_y)
    grad_d['gmax'] = coff_x[maxarg]
    halfmax = np.max(grad_y) / 2
    peakargs = np.where(grad_y > halfmax)[0]
    start = [peakargs[0]-1, peakargs[0]]
    end = [peakargs[-1]+1, peakargs[-1]]
    grad_d['fwhm_y'] = [halfmax, halfmax]
    grad_d['fwhm_x'] = [
        np.interp(halfmax, grad_y[start], grad_x[start]),
        np.interp(halfmax, grad_y[end], grad_x[end])]
    grad_d['fwhm'] = grad_d['fwhm_x'][1] - grad_d['fwhm_x'][0]

    gradspect.plot(grad_d['fwhm_x'], grad_d['fwhm_y'], "#880088")
    textfield.setText(
        "ZCE = {:.2f}\nFWHM = {:.2f}\nCenter(HM) = {:.2f}".format(
            grad_d['gmax'], grad_d['fwhm'],
            np.mean(grad_d['fwhm_x'])))
    gradspect.annotate(' FWHM = {:.2f}'.format(grad_d['fwhm']),
                       xy=(grad_d['fwhm_x'][1], grad_d['fwhm_y'][1]))
    gradspect.annotate('{:.2f}'.format(grad_d['gmax']),
                       xy=(grad_x[maxarg], grad_y[maxarg]))
    zcespec.figure.canvas.draw()


def exp_zce(zce_spec, zcegrad_spec, data_set, parent):
    """export the ZCE graph into the .dat file format"""
    if data_set is None:
        QtWidgets.QMessageBox.warning(
            parent, "Export ZCE spectrum",
            "Nothing to export, cancelling request")
        return
    exp_f_name = ft.get_save_filename(
        "Export ZCE spectrum", "dat table (*.dat)", "dat", parent)
    if exp_f_name != '':
        expf = open(exp_f_name, 'w')
        expf.write("mass ion_count ion_count_gradient fwhm_x fwhm_y\n"
                   "m/z\n"
                   "{} zce={} fwhm={} hmcenter={}\n".format(
                       os.path.basename(data_set.filename),
                       zcegrad_spec['gmax'], zcegrad_spec['fwhm'],
                       np.mean(zcegrad_spec['fwhm_x'])))
        for i in range(len(zce_spec['x'])):
            fwhm = ["", ""]
            if i <= 1:
                fwhm = [zcegrad_spec['fwhm_x'][i],
                        zcegrad_spec['fwhm_y'][i]]
            expf.write("{} {} {} {} {}\n".format(
                zce_spec['x'][i], zce_spec['y'][i], zcegrad_spec['y'][i],
                fwhm[0], fwhm[1]))
        expf.close()


def help_msg(pw):
    QtWidgets.QMessageBox.information(
            pw, "TSQ zce tool help", "{}".format(helpstr))


def paint_override(self, ds, coff, coffgrad):
    overlay = self.plot.twinx()
    textfield = QtWidgets.QLabel()
    pop_dial(self.plot, overlay, ds, coff, coffgrad, textfield, None)


def print_graph(ds, coff, coffgrad):
    def printimage(printdevice, img):
        printer.setResolution(600)
        painter = QtGui.QPainter(printdevice)
        painter.drawImage(0, 0, img)
        painter.end()
    # TODO: substitute the QPrintPreviewDialog with QPrintPreviewWidget
    printPreview = QtPrintSupport.QPrintPreviewDialog()
    printer = printPreview.printer()
    printer.setPageSize(printer.A5)
    printer.setDuplex(printer.DuplexNone)
    imggen = imgt.ImagePainter("msspec", printer)
    imggen.popfig = lambda: paint_override(imggen, ds, coff, coffgrad)
    image = imggen.paint()
    printPreview.paintRequested.connect(lambda: printimage(printer, image))
    printPreview.exec()


def key_pressed(event, ds, coff, coffgrad):
    if event.key() == QtCore.Qt.Key_C:
        if event.modifiers().__int__() == QtCore.Qt.ControlModifier:
            painter = imgt.ImagePainter("zcespec")
            painter.popfig = lambda: paint_override(
                painter, ds, coff, coffgrad)
            painter.clip()


def dialog(parent, augCanvas, update_signal):
    coff = dict(name="", xlabel="Voltage (V)", ylabel="ion count")
    coffgrad = dict(c_ymin=-0.1, name="", xlabel="",
                    ylabel="ion count gradient", gmax=None, fwhm_x=None,
                    fwhm_y=None, fwhm=None)

    def onclose(widget, event, update_fnc):
        logger.debug("ZCE window custom close routine called")
        update_signal.signal.disconnect(update_fnc)
        QtWidgets.QDialog.closeEvent(widget, event)

    def update_fnc():
        pop_dial(coffspect, coffspect_grad, augCanvas.ds, coff, coffgrad,
                 textfield, parent)

    dial_widget = QtWidgets.QDialog(
            parent, windowTitle='TSQ zero collision energy calculator')
    dial_widget.closeEvent = lambda event: onclose(
        dial_widget, event, update_fnc)
    update_signal.signal.connect(update_fnc)

    dial_graph = Figure(figsize=(5, 2), dpi=100, facecolor="None")
    coffspect = dial_graph.add_subplot(111, facecolor=(1, 1, 1, 0.8))
    coffspect_grad = coffspect.twinx()
    graph_canvas = FigureCanvas(dial_graph)
    graph_canvas.setStyleSheet("background-color:transparent;")
    graph_canvas.setAutoFillBackground(False)

    gt.zoom_factory(coffspect_grad, 1.15, coffgrad)
    gt.pan_factory(coffspect_grad, coffgrad)

    zce_export = QtWidgets.QPushButton("Export ZCE")
    zce_export.clicked.connect(lambda: exp_zce(
        coff, coffgrad, augCanvas.ds, parent))
    zce_print = QtWidgets.QPushButton("Print ZCE")
    zce_print.clicked.connect(lambda: print_graph(
        augCanvas.ds, coff, coffgrad))
    zce_help = QtWidgets.QPushButton("Help")
    zce_help.clicked.connect(lambda: help_msg(parent))
    close_button = QtWidgets.QPushButton("Close")
    close_button.clicked.connect(dial_widget.close)

    dial_widget.keyPressEvent = lambda event: key_pressed(
            event, augCanvas.ds, coff, coffgrad)

    butt_layout = QtWidgets.QHBoxLayout()
    butt_layout.addWidget(zce_help)
    butt_layout.addStretch(1)
    textfield = QtWidgets.QLabel(coffgrad['gmax'])
    butt_layout.addWidget(textfield)
    butt_layout.addStretch(1)
    butt_layout.addWidget(zce_print)
    butt_layout.addWidget(zce_export)
    butt_layout.addWidget(close_button)

    dial_layout = QtWidgets.QVBoxLayout(dial_widget)
    dial_layout.addWidget(graph_canvas)
    dial_layout.addLayout(butt_layout)
    dial_widget.setFocus()
    dial_widget.show()
    pop_dial(coffspect, coffspect_grad, augCanvas.ds, coff, coffgrad,
             textfield, parent)
