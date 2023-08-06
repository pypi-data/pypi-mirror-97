from PyQt5 import QtWidgets
from PyQt5 import QtCore
from matplotlib.backends.backend_qt5agg import\
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import SpanSelector
import numpy as np
import prasopes.datatools as dt
import prasopes.config as cf
import matplotlib
matplotlib.use("Qt5Agg")


colors = np.array([[0, 0, 0], [255, 0, 0], [0, 255, 0], [0, 0, 255],
                   [0, 200, 255], [255, 200, 0], [255, 100, 0],
                   [200, 50, 0], [255, 0, 200], [0, 100, 0],
                   [0, 100, 255], [100, 100, 100]])


ann_bbox = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.5)


class AugFigureCanvas(FigureCanvas):
    """Figure canvas fitted with mass spectrum, chromatogram and more"""
    def __init__(self):
        self.figure = Figure(figsize=(5, 4), dpi=100, facecolor="None",
                             constrained_layout=True)
        super().__init__(self.figure)
        self.ds = None
        self.ms = dict(annotation=[], name="Spectrum", xlabel="m/z",
                       ylabel="ion count", xtics=20, predict=None, texts=[])
        self.chrom = dict(
            x=[0], y=[0], t_start=None, t_end=None, machtype=None,
            name="Chromatogram", xlabel="time(min)", ylabel="total ion count",
            timesarg=[])
        self.drlcache = [None, None]
        self.tofcache = [None, None]
        self.mobontofcache = [None, None]
        grid = self.figure.add_gridspec(2, 1)
        self.chromplot = self.figure.add_subplot(grid[0, 0],
                                                 facecolor=(1, 1, 1, 0.8))
        self.spectplot = self.figure.add_subplot(grid[1, 0],
                                                 facecolor=(1, 1, 1, 0.8))
        self.setStyleSheet("background-color:transparent;")
        self.setAutoFillBackground(False)
        self.paramstable = dt.table(["", "name", "value"], 100)
        pan_factory(self.chromplot)
        zoom_factory(self.chromplot, 0.9)
        pan_factory(self.spectplot, self.ms)
        zoom_factory(self.spectplot, 0.9, self.ms)
        textedit_factory(self.spectplot, self.ms)
        self.mass_selector = AugSpanSelector(self.spectplot, self.ms)
        self.time_selector = SpanSelector(
                self.chromplot, lambda x_min, x_max: pick_times(
                    x_min, x_max, self), 'horizontal', useblit=True,
                rectprops=dict(alpha=0.15, facecolor='purple'), button=3)
        self.figure.set_constrained_layout(False)

    def constrained_draw(self):
        self.figure.execute_constrained_layout()
        self.draw()


class AugSpanSelector(SpanSelector):
    def __init__(self, ax, data):
        super().__init__(
            ax, onselect=lambda x, y: None, direction='horizontal',
            minspan=0.01, useblit=True, rectprops=dict(
                alpha=0.15, facecolor='purple'),
            onmove_callback=None, span_stays=False, button=3)
        self.data = data

    def _press(self, event):
        """on button press event override"""
        if QtWidgets.QApplication.keyboardModifiers() ==\
                QtCore.Qt.ShiftModifier:
            self.direction = 'vertical'
            self.onselect = self.pick_intensities
        else:
            self.direction = 'horizontal'
            self.onselect = self.pick_masses
        self.new_axes(self.ax)
        super()._press(event)

    def _release(self, event):
        """on button release event"""
        if self.pressv is None:
            return
        elif self.direction == 'horizontal':
            super()._release(event)
        else:
            self.rect.set_visible(False)
            self.canvas.draw_idle()
            vmax = self._get_data(event)[1] or self.prev[1]
            span = vmax - self.ax.get_ylim()[0]
            if self.minspan is not None and span < self.minspan:
                return
            self.onselect(self.ax.get_ylim()[0], vmax)
            self.pressv = None
            return False

    def _set_span_xy(self, event):
        """Setting the span coordinates override"""
        if self.direction == 'horizontal':
            super()._set_span_xy(event)
        else:
            x, y = self._get_data(event)
            if y is None:
                return
            self.prev = x, y
            self.rect.set_y(self.ax.get_ylim()[0])
            self.rect.set_height(y)

    def pick_masses(self, vmin, vmax):
        """zoom the spectrum in x axis by mass range"""
        self.ax.set_xlim(vmin, vmax)
        autozoomy(self.ax)
        ann_spec(self.ax, self.data)

    def pick_intensities(self, vmin, vmax):
        """zoom the spectrum in y axis by top intensity from range"""
        self.ax.set_ylim(-vmax*0.01, vmax)
        ann_spec(self.ax, self.data)


class FixedScalarFormatter(matplotlib.ticker.ScalarFormatter):
    def __init__(self):
        super().__init__()
        self._powerlimits = (0, 0)

    def _set_format(self):
        """_set_format override"""
        self.format = "%.2f"


def zoom_factory(axis, base_scale, plot_data=None):
    """returns zooming functionality to axis"""
    def zoom_fun(event, pd, ax, scale):
        """zoom when scrolling"""
        if event.inaxes == axis:
            scale_factor = np.power(scale, event.step)
            if QtWidgets.QApplication.keyboardModifiers() !=\
                    QtCore.Qt.ShiftModifier:
                data = event.ydata
                new_top = data + (ax.get_ylim()[1] - data) \
                    * scale_factor
                ymin = -0.01
                if type(pd) is dict and "c_ymin" in pd:
                    ymin = pd['c_ymin']
                axis.set_ylim([new_top * ymin, new_top])
            else:
                data = event.xdata
                x_left = data - ax.get_xlim()[0]
                x_right = ax.get_xlim()[1] - data
                ax.set_xlim([data - x_left * scale_factor,
                            data + x_right * scale_factor])
            if type(pd) is dict and "annotation" in pd:
                ann_spec(event.inaxes, pd)
            ax.figure.canvas.draw()

    fig = axis.get_figure()
    fig.canvas.mpl_connect('scroll_event', lambda event: zoom_fun(
        event, plot_data, axis, base_scale))


def pan_factory(axis, plot=None):
    """pan spectrum when you press a button"""
    def pan_fun(event, ax, pd):
        # Release focus from other objects when clicking on graph.
        focusedWidget = QtWidgets.QApplication.focusWidget()
        if focusedWidget and event.inaxes == ax:
            focusedWidget.clearFocus()
        # re-scale to origin if doubleclicked
        if event.dblclick and event.inaxes == ax:
            ax.get_figure()
            ax.autoscale(True)
            ymin = -0.01
            if type(pd) is dict and "c_ymin" in pd:
                ymin = pd['c_ymin']
            ax.set_ylim(ax.get_ylim()[1]*ymin, ax.get_ylim()[1]*1.1)
            if type(pd) is dict and "annotation" in pd:
                ann_spec(ax, pd)
            ax.figure.canvas.draw()
        # otherwise pan
        elif event.button == 1 and event.inaxes == ax:
            ax.start_pan(event.x, event.y, event.button)
            id_drag = fig.canvas.mpl_connect(
                'motion_notify_event',
                lambda action: drag_fun(action, ax))
            id_release = fig.canvas.mpl_connect(
                'button_release_event',
                lambda action: drag_end(
                    action, id_drag, id_release, pd, ax))

    def drag_fun(event, ax):
        ax.drag_pan(1, 'x', event.x, event.y)
        ax.figure.canvas.draw()

    def drag_end(event, id_drag, id_release, pd, ax):
        if event.button == 1:
            fig.canvas.mpl_disconnect(id_drag)
            fig.canvas.mpl_disconnect(id_release)
            if type(pd) is dict and "annotation" in pd:
                ann_spec(ax, pd)
            ax.figure.canvas.draw()

    fig = axis.get_figure()
    fig.canvas.mpl_connect('button_press_event',
                           lambda action: pan_fun(action, axis, plot))


def textedit_factory(axis, plot_data):
    def annpicked(pickevent):
        if isinstance(pickevent.artist, matplotlib.text.Annotation) and\
                pickevent.mouseevent.button == 2:
            annotation = pickevent.artist
            textdial = QtWidgets.QInputDialog.getText(
                    None, "Enter new annotation", "",
                    text=annotation.get_text())
            if textdial[1]:
                annotation.set_text(textdial[0].replace('\\n', '\n'))
                if len(textdial[0]) == 0 and annotation in plot_data['texts']:
                    plot_data['texts'].remove(annotation)
                elif annotation in plot_data['annotation']:
                    annotation.set_bbox(ann_bbox)
                    plot_data['annotation'].remove(annotation)
                    plot_data['texts'].append(annotation)
                axis.figure.canvas.draw()

    axis.figure.canvas.mpl_connect('pick_event', annpicked)


def plot_subtime(augCanvas):
    """plot averaged spectrum of subselected part of the chromatogram"""
    slims = [augCanvas.spectplot.get_xlim(), augCanvas.spectplot.get_ylim()]
    chlims = [augCanvas.chromplot.get_xlim(), augCanvas.chromplot.get_ylim()]
    augCanvas.ms['annotation'].clear()
    augCanvas.spectplot.clear()
    augCanvas.chromplot.clear()

    chromargs = augCanvas.ds.get_chromargs()
    populate(augCanvas)

    for i, args in enumerate(chromargs):
        if len(args):
            dots_x, dots_y = [augCanvas.ds.chromatograms[i][j][args]
                              for j in (0, 1)]
            augCanvas.chromplot.plot(dots_x, dots_y, '.', color=(
                                     colors[i % len(colors)]/255))

    augCanvas.spectplot.set_xlim(slims[0])
    if not cf.settings().value("view/autozoomy", type=bool):
        augCanvas.spectplot.set_ylim(slims[1])
    if augCanvas.ds.headers:
        for ax in (augCanvas.spectplot, augCanvas.chromplot):
            ax.legend(loc=2)
            ax.get_legend().set_in_layout(False)
            ax.get_legend().set_visible(
                    cf.settings().value("view/legend", type=bool))
    else:
        autozoomy(augCanvas.spectplot)
    ann_spec(augCanvas.spectplot, augCanvas.ms)
    augCanvas.chromplot.set_xlim(chlims[0])
    augCanvas.chromplot.set_ylim(chlims[1])
    augCanvas.draw()
    update_paramstable(augCanvas)


def pick_times(x_min, x_max, augCanvas):
    """subselect part of the chromatogram and plot it"""
    augCanvas.ds.mintime = x_min
    augCanvas.ds.maxtime = x_max
    plot_subtime(augCanvas)


def shift_times(event, augCanvas):
    """shifts times when arrow is pressed"""
    if event.key() == QtCore.Qt.Key_Left:
        move = -1
    elif event.key() == QtCore.Qt.Key_Right:
        move = +1
    else:
        return
    if not np.array_equal(augCanvas.chrom['timesarg'], []):
        x_min, x_max = augCanvas.chrom['t_start'], augCanvas.chrom['t_end']
        alltimes = np.concatenate([subset['chrom_dat'][0] for subset
                                   in augCanvas.ds])
        times = dt.argsubselect(alltimes, x_min, x_max) + move
        goodtimes = np.where((times < len(alltimes)) & ~(times < 0))[0]
        if not np.array_equal(goodtimes, []):
            x_min, x_max = alltimes[times[goodtimes[[0, -1]]]]
            pick_times(x_min, x_max, augCanvas)


def autozoomy(ms_spec):
    if cf.settings().value("view/autozoomy", type=bool) and not (
            np.array_equal(ms_spec.lines[0].get_xdata(), [0]) and
            len(ms_spec.lines) == 1):
        ms_spec.autoscale(True, 'y')
        gap = 0.01
        ymax = np.max([np.max(line.get_data()[1][dt.argsubselect(
            line.get_data()[0], *ms_spec.get_xlim())])*1.1
            for line in ms_spec.lines])
        ms_spec.set_ylim(-ymax*gap, ymax)
        ms_spec.figure.canvas.draw()


def ann_spec(ms_spec, msdata, ann_limit=0.01, coef_x=15, coef_y=20):
    """annotate spectrum

    First define the array, in which the annotation should occur.
    Then remove values which are invalid as local maximas. Local maximas are
    then reduced to a representation of the important ones by the sub_peaks
    function"""

    cx = msdata['ancx'] if 'ancx' in msdata.keys() else 15
    cy = msdata['ancy'] if 'ancy' in msdata.keys() else 20

    def sub_peaks(peakz, hardpeaks, xrange, yrange, coef_x=cx, coef_y=cy):
        """Returns reasonable subselection of local maximas"""
        hardxy = np.array([i.xy for i in hardpeaks], dtype=[
            ('x', np.float32), ('y', np.float32)])
        sort_peaks = np.flipud(np.sort(np.array(peakz), order='y')).copy()
        red_x = xrange / coef_x
        red_y = yrange / coef_y
        big_peaks = np.array([], dtype=[('x', np.float32), ('y', np.float32)])
        for peak in np.nditer(sort_peaks, flags=["zerosize_ok"]):
            if not (np.any((abs(peak['y'] - big_peaks['y']) < red_y)
                           & (abs(peak['x'] - big_peaks['x']) < red_x)) or
                    np.any((abs(peak['y'] - hardxy['y']) < red_y)
                           & (abs(peak['x'] - hardxy['x']) < red_x))):
                big_peaks = np.append(big_peaks, peak)
        return big_peaks

    peaks = []
    for line in ms_spec.lines:
        xdata, ydata = line.get_data()
        # Thanks to:
        # https://gist.github.com/ben741/d8c70b608d96d9f7ed231086b237ba6b
        minlim = ms_spec.get_ylim()[1] * ann_limit
        lims = [*ms_spec.get_xlim(), *ms_spec.get_ylim()]
        maxargs = np.where((xdata[1:-1] > lims[0]) & (xdata[1:-1] < lims[1]) &
                           (ydata[1:-1] > minlim) & (ydata[1:-1] < lims[3]) &
                           (ydata[1:-1] > ydata[0:-2]) &
                           (ydata[1:-1] > ydata[2:]))[0] + 1
        peakline = np.empty([len(maxargs)], dtype=[('x', np.float32),
                                                   ('y', np.float32)])
        peakline['x'], peakline['y'] = xdata[maxargs], ydata[maxargs]
        peaks.append(peakline)

    # delete objects from the spectra
    for intensity in msdata['annotation']:
        intensity.remove()
    # remove them from tracking
    msdata['annotation'].clear()

    if not len(peaks):
        return
    peaks = np.concatenate(peaks)

    s_peaks = sub_peaks(peaks, msdata['texts'],
                        np.diff(ms_spec.get_xlim()),
                        np.diff(ms_spec.get_ylim()))

    dispints = cf.settings().value("view/intensities", type=bool)
    for peak in s_peaks:
        digits = cf.settings().value("view/digits", type=int)
        annotation = '{0:.{2}f}\n{1: .{2}e}'.format(peak[0], peak[1], digits)\
                if dispints else '{0:.{1}f}'.format(peak[0], digits)
        peaktext = ms_spec.annotate(
            annotation, xy=(peak['x'], peak['y']), textcoords='data',
            picker=True, in_layout=False)
        msdata['annotation'].append(peaktext)


def pop_plot(xdata, ydata, plot, plot_data, colornum=0,
             legend=None, annotate=True):
    """Define and populate plot"""
    if len(xdata):
        plot.plot(xdata, ydata, linewidth=1, color=(
            colors[colornum % len(colors)]/255), label=legend)
    plot.set_title(plot_data['name'], loc="right")
    plot.set_xlabel(plot_data['xlabel'])
    plot.set_ylabel(plot_data['ylabel'])
    plot.set_ylim(plot.get_ylim()[1] * -0.01,
                  plot.get_ylim()[1] * 1.1)
    plot.yaxis.set_major_formatter(FixedScalarFormatter())
    # put hardcoded annotation if there is some
    if "texts" in plot_data and not any(
            data in plot.get_children() for data in plot_data['texts']):
        plot_data['texts'] = [plot.annotate(
            a.get_text(), a.xy, picker=True, bbox=ann_bbox, in_layout=False)
            for a in plot_data['texts']]
    if "annotation" in plot_data and annotate:
        ann_spec(plot, plot_data)
    if "xtics" in plot_data:
        plot.locator_params(nbins=plot_data["xtics"], axis='x')
        plot.minorticks_on()
        plot.tick_params(axis='y', which='minor', left=False)


def legendize(rawlegend, augCanvas):
    # sanity check
    if len(rawlegend) == 0:
        return None
    marks = ["-", "+"]
    quads = ["q3", "q1"]

    def translate(wut):
        if augCanvas.ds.machtype == 47:
            if wut[1] in (0, 1):
                text = "{}{}ms; m/z = {:.1f}-{:.1f}".format(
                        marks[int(wut[0])], quads[int(wut[1])], *wut[4:])
            else:
                text = "{}ms^{} {:.2f}@{:.1f}V; m/z = {:.1f}-{:.1f}".format(
                        marks[int(wut[0])], *wut[1:])
        elif augCanvas.ds.machtype in (57, 63):
            if int(wut[1]) == 1:
                text = "{}ms; m/z = {:.1f}-{:.1f}".format(
                        marks[int(wut[0])], *wut[2:])
            else:
                text = ("{}ms^{:.0f};" + "".join([" {:.2f}/{:.1f}@{:.1f}V" for
                                                  _ in range(int(wut[1])-1)]) +
                        "; m/z = {:.1f}-{:.1f}").format(
                                marks[int(wut[0])], *wut[1:])
        else:
            text = "unknown header type"
        return text
    uniqindexs = np.unique(np.array(rawlegend), return_index=True)\
        if np.array(rawlegend).dtype == np.dtype('O') else\
        np.unique(np.array(rawlegend), axis=0, return_index=True)
    strdata = [translate(i) for i in rawlegend[np.sort(uniqindexs[1])]]
    strtext = " and\n".join(strdata) + "; t = {:.2f}-{:.2f} min".format(
                    augCanvas.ds.mintime, augCanvas.ds.maxtime)
    return strtext


def populate(augCanvas):
    """populate the GUI plots with desired dataset"""
    if np.array_equal(augCanvas.ds, []):
        return
    [i.clear() for i in (augCanvas.ms['annotation'],
     augCanvas.chromplot, augCanvas.spectplot)]

    if augCanvas.ms['predict']:
        # TODO: Fix the broken code
        predict = augCanvas.ms['predict']
        maxm = np.argmax(predict[1]) + predict[0]
        maxseek = dt.argsubselect(linex, maxm-.5, maxm+.5)
        maxpos = maxseek[np.argmax(liney[maxseek])]
        crudeints = predict[1] * augCanvas.ms['y'][maxpos]
        crudemasses = (np.arange(len(predict[1])) + linex[maxpos])
        pmasses, pints = [], []
        [pmasses.extend([np.nan, i, i]) for i in crudemasses]
        [pints.extend([np.nan, 0, i]) for i in crudeints]
        augCanvas.spectplot.plot(pmasses, pints, linewidth=1)

    chromxy = augCanvas.ds.chromatograms
    msxy = augCanvas.ds.get_spectra()
    for i in range(len(msxy)):
        if augCanvas.ds.headers and\
                len(augCanvas.ds.headers) == len(augCanvas.ds.chromatograms):
            legend = legendize(augCanvas.ds.headers[i], augCanvas)
        else:
            legend = None
        pop_plot(msxy[i][0], msxy[i][1], augCanvas.spectplot,
                 augCanvas.ms, i, legend)
        pop_plot(chromxy[i][0], chromxy[i][1], augCanvas.chromplot,
                 augCanvas.chrom, i, legend)
    for ax in (augCanvas.spectplot, augCanvas.chromplot):
        if augCanvas.ds.headers:
            ax.legend(loc=2)
            ax.get_legend().set_in_layout(False)
            ax.get_legend().set_visible(
                    cf.settings().value("view/legend", type=bool))
        ax.autoscale(True)
        ax.set_ylim(ax.get_ylim()[1]*-0.01, ax.get_ylim()[1]*1.1)
    augCanvas.constrained_draw()
    return


def update_paramstable(augCanvas):
    if not augCanvas.ds.params:
        augCanvas.paramstable.setRowCount(0)
        return
    elif len(augCanvas.ds.params[0]) == augCanvas.paramstable.rowCount():
        states = [augCanvas.paramstable.cellWidget(row, 0).checkState()
                  for row in range(augCanvas.paramstable.rowCount())]
    else:
        states = False
        augCanvas.paramstable.setRowCount(len(augCanvas.ds.params[0]))
    for row, paramname in enumerate(augCanvas.ds.params[0]):
        [augCanvas.paramstable.setItem(row, col, QtWidgets.QTableWidgetItem())
         for col in range(1, 3)]
        augCanvas.paramstable.setCellWidget(row, 0, QtWidgets.QCheckBox())
        if states:
            augCanvas.paramstable.cellWidget(row, 0).setCheckState(states[row])
        augCanvas.paramstable.item(row, 1).setText(paramname)
        vals = [param[row] for param in augCanvas.ds.params[1]
                if (param[0] >= augCanvas.ds.mintime and
                param[0] <= augCanvas.ds.maxtime)]
        if len(vals) == 0:
            text = ""
        elif all([type(val) in [np.float32, np.float64] for val in vals]):
            aver = np.average(vals)
            minim = min(vals)
            maxim = max(vals)
            text = "{:.2f} (from {:.2f} to {:.2f})".format(aver, minim, maxim)
        else:
            values = [str(i) for i in np.unique(np.array(vals), axis=0)]
            text = " or ".join(values)
        augCanvas.paramstable.item(row, 2).setText(text)
