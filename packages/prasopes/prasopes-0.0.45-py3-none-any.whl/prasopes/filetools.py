from PyQt5 import QtWidgets
import prasopes.config as cf
import prasopes.datatools as dt
import os.path


def get_save_filename(caption, fnfilter, suffix, parent):
    """fix Qt5 "feature" - it does add sufix when exporting
    and thus also cant check for file with the selected suffix"""
    filename = QtWidgets.QFileDialog.getSaveFileName(
            caption=caption, filter=fnfilter,
            directory=cf.settings().value("open_folder"),
            options=QtWidgets.QFileDialog.DontConfirmOverwrite)[0]
    if suffix[0] != ".":
        suffix = ".{}".format(suffix)
    if filename[-len(suffix):] != suffix and filename != "":
        filename = "".join((filename, suffix))
    if os.path.isfile(filename):
        quest = QtWidgets.QMessageBox.warning(
           parent, caption,
           "File {} already exists in the filesystem.\n"
           "Do you want to overwrite it?"
           .format(os.path.basename(filename)),
           QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if quest == QtWidgets.QMessageBox.No:
            filename = ''
    return filename


def export_dial(augCanvas, main_window):
    """exports the chromatogram into the .dat file format"""
    if not augCanvas.ds:
        QtWidgets.QMessageBox.warning(
            main_window, "Export spectrum",
            "Nothing to export, cancelling request")
        return
    exp_f_name = get_save_filename(
        "Export spectrum", "dat table (*.dat)", "dat", main_window)
    if exp_f_name != '':
        description = ("{}_{:.4}-{:.4}_minutes_of_the_aquisition".format(
                   os.path.basename(augCanvas.ds.filename),
                   augCanvas.chrom['t_start'], augCanvas.chrom['t_end']))
        expf = open(exp_f_name, 'w')
        expf.write(dt.specttostr(augCanvas.spectplot, description=description))
        expf.close
