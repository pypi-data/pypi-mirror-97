#!/usr/bin/env python3
from matplotlib.backends.backend_qt5agg import\
        FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from io import BytesIO
from PyQt5 import QtGui
from PyQt5 import QtPrintSupport
from PyQt5 import QtWidgets
from pathlib import Path
import copy
import prasopes.graphtools as gt
import prasopes.config as cf


def paint_image(mass_spec, spect, fn=None, painttarget=None):
    """generates QImage from mass spectrum"""
    configtype = "print/{}" if isinstance(
            painttarget, type(QtPrintSupport.QPrinter())) else "imggen/{}"
    xinch, yinch = [float(cf.settings().value(configtype.format(i), type=str)\
                          .replace(",", ".")) for i in ("xinch", "yinch")]
    dpi, xtics = [int(cf.settings().value(configtype.format(i))) for i
                  in ("dpi", "xtics")]
    paintfig = Figure(figsize=(xinch, yinch), dpi=dpi, constrained_layout=True)
    FigureCanvas(paintfig)
    printplot = paintfig.add_subplot(111)
    printplot.set_xlim(spect.get_xlim())
    printplot.set_ylim(spect.get_ylim())
    data = [line.get_data() for line in spect.lines]
    texts = copy.copy(mass_spec)
    if len(mass_spec['headers']) != 0:
        legend = spect.get_legend().get_texts()
        [gt.pop_plot(*line, printplot, texts, i, legend[i].get_text(),
                     not (cf.settings().value(
                         configtype.format("onlymanann"), type=bool)))
            for i, line in enumerate(data)]
        legend = 1
        if legend == True:
            printplot.legend(loc=2)
    else:
        [gt.pop_plot(*line, printplot, texts, i)
            for i, line in enumerate(data)]
    printplot.locator_params(nbins=xtics, axis='x')
    if fn not in (None, [None]):
        printplot.set_title(Path(*Path(fn).resolve().parts[-2:]),
                            loc="right")
    cache_file = BytesIO()
    paintfig.savefig(cache_file)
    paintfig.savefig("{}.png".format(fn[:-4]), format="png")
    cache_file.seek(0)
    image = QtGui.QImage.fromData(cache_file.read())
    return image


def clip_spect_img(mass_spec, spect, fn):
    image = paint_image(mass_spec, spect, fn=fn)
    QtWidgets.QApplication.clipboard().clear()
    [QtWidgets.QApplication.clipboard().setImage(image, i) for i in range(2)]
