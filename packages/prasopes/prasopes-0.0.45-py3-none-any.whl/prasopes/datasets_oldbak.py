#!/usr/bin/env python3
from rawprasslib import load_raw
from opentimspy.opentims import OpenTIMS
import pathlib
import opentims_bruker_bridge
import numpy as np
import prasopes.config as cf


class Dataset():
    def __init__(self, rawfile):
        self.filename = rawfile
        self.chromatograms = []
        self.dataset = []
        self.timemin = -np.inf
        self.timemax = np.inf
        self.type = None

    def refresh(self):
        """implement per-case"""
        return None

    def get_chromatogram(self):
        """implement per-case"""
        return

    def get_spectra(self):
        """implement per-case"""
        return


class ThermoRawDataset(Dataset):
    def __init__(self, rawfile):
        super().__init__(self, rawfile)
        self.type = "thermo"
        self.refresh()
        self.chromatograms = []

    def refresh(self):
        self.dataset = load_raw(selt.filename, 
                                cf.settings().value("tmp_location"))
        self.chromatograms = self.get_chromatogram()
        self.timemin = self.chromatograms[0][0]
        self.timemax = self.chromatograms[-1][-1]

    def get_chtomatograms(self):
        if cf.settings().value("view/oddeven", type=bool):
            chroms = []
            for i in self.dataset:
                for j in (0,1):
                    chroms.append([i[0][ax, :][j::2] for ax in (0,1)])
        else:
            chroms = [i[0] for i in self.dataset]
        return chroms

    def get_spectra(self):
        times = dt.argsubselect(np.concatenate(
             [subset[0][0] for subset in self.dataset]),
             self.timemin, self.timemax)
        args = []
        for subset in augCanvas.ds:
            goodtimes = np.where((times < len(subset[0][0]))
                             & ~(times < 0))[0]
            args.append(times[goodtimes])
            times =- len(subset[0][0])
            spectra = []
            for i,subset in enumerate(self.dataset):
                if cf.settings().value("view/oddeven", type=bool):
                    for j in (0,1):
                        yvalz = np.mean(subset[2][args[i][j::2]], axis=0)
                        spectra.append(subset[1], yvalz)
                else:
                    yvalz = np.mean(subset[2][args[i]], axis=0)
                    spectra.append(subset[1], yvalz)
        return spectra


class BrukerTimsDataset(Dataset):
    def __init__(self, rawfile):
        super().__init__(rawfile)
        self.type = "bruker"
        self.steps = []
        self.refresh()

    def refresh(self):
        self.dataset = OpenTIMS(pathlib.Path(self.filename))
        self.chromatograms = self.get_chromatogram()
        self.timemin = self.chromatograms[0][0][0]
        self.timemax = self.chromatograms[-1][0][-1] 

    def get_chromatogram(self):
        keys = ('retention_time', 'intensity')
        times = self.dataset.retention_times / 60
        intensities = [np.sum(i['intensity']) for i in self.dataset.query_iter(
                       self.dataset.ms1_frames, columns=('intensity',))]
        return [[times,intensities]]

    def get_spectra(self):
        massints = [[i['mz'], i['intensity']] for i in 
                    self.dataset.rt_query_iter(self.timemin*60, self.timemax*60,
                                               columns=('mz', 'intensity'))]
        sortmasses = [np.argsort(i[0]) for i in massints]
        sortmassints = [[massints[i][0][sortmasses[i]],
                        massints[i][1][sortmasses[i]]]
                        for i in range(len(sortmasses))]
        return sortmassints
