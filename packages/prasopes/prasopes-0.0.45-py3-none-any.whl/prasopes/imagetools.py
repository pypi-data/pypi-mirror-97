#!/usr/bin/env python3
from matplotlib.backends.backend_qt5agg import\
        FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from io import BytesIO
from PyQt5 import QtGui
from PyQt5 import QtPrintSupport
from PyQt5 import QtWidgets
import prasopes.config as cf


class ImagePainter:
    """base class for painting image into cache"""
    def __init__(self, configname, painttarget=None):
        self.painttartget = painttarget
        self.confname = configname
        self.conftype = ("print/{}_{{}}" if isinstance(
            painttarget, type(QtPrintSupport.QPrinter()))
            else "imggen/{}_{{}}").format(self.confname)
        self.plot = None

    def updatefig(self):
        """generates a figure with desired parameters"""
        xinch, yinch = [float(
            cf.settings().value(self.conftype.format(i), type=str).replace(
                ",", ".")) for i in ("xinch", "yinch")]
        dpi = int(cf.settings().value(self.conftype.format("dpi")))
        fig = Figure(figsize=(xinch, yinch), dpi=dpi, constrained_layout=True)
        FigureCanvas(fig)
        self.plot = fig.add_subplot(111)

    def popfig(self):
        """to be overriden specifically"""
        raise NotImplementedError

    def paint(self):
        self.updatefig()
        self.popfig()
        cache_file = BytesIO()
        self.plot.figure.savefig(cache_file)
        cache_file.seek(0)
        image = QtGui.QImage.fromData(cache_file.read())
        return image

    def clip(self):
        img = self.paint()
        QtWidgets.QApplication.clipboard().clear()
        [QtWidgets.QApplication.clipboard().setImage(img, i) for i in range(2)]
