#!/usr/bin/env python3
from rawprasslib import load_raw
from opentimspy.opentims import OpenTIMS
try:
    from rawautoparams import load_params
    autoparams = True
except ImportError:
    autoparams = False
import numpy as np
import logging
import os.path
import pathlib
import prasopes.config as cf
import prasopes.datatools as dt


logger = logging.getLogger('dsLogger')


class Dataset():
    def __init__(self, rawfile):
        self.filename = rawfile
        self.chromatograms = []
        self.dataset = []
        self.headers = None
        self.params = None
        self.mintime = -np.inf
        self.maxtime = np.inf

    def get_chromargs(self, mint=None, maxt=None):
        logger.info("finding correct scans")
        mint = mint or self.mintime
        maxt = maxt or self.maxtime
        times = dt.argsubselect(np.concatenate(
             [subset[0] for subset in self.chromatograms]), mint, maxt)
        args = []
        for subset in self.chromatograms:
            goodtimes = np.where((times < len(subset[0])) & ~(times < 0))[0]
            args.append(times[goodtimes])
            times -= len(subset[0])
        return args

    def refresh(self):
        """implement per-case"""
        return None

    def get_chromatograms(self):
        """implement per-case"""
        raise NotImplementedError

    def get_peakchrom(self, masstart, massend):
        """implement per-case"""
        raise NotImplementedError

    def get_spectra(self, mint=None, maxt=None):
        mint = mint or self.mintime
        maxt = maxt or self.maxtime
        """implement per-case"""
        raise NotImplementedError


class ThermoRawDataset(Dataset):
    def __init__(self, rawfile):
        super().__init__(rawfile)
        self.machtype = []
        self.refresh()

    def refresh(self):
        self.dataset = load_raw(self.filename,
                                cf.settings().value("tmp_location"))
        self.chromatograms = self.get_chromatograms()
        self.mintime, self.maxtime = [self.chromatograms[i][0][i]
                                      for i in (0, -1)]
        if autoparams:
            try:
                self.params, rawheaders, self.machtype = load_params(
                    self.filename, cf.settings().value("tmp_location"))
                segments = [len(i[0]) for i in self.chromatograms]
                indicies = [sum(segments[:i+1])
                            for i, j in enumerate(segments)]
                self.headers = np.split(rawheaders, indicies)[:-1]
            except Exception:
                self.params, self.machtype, self.headers = None, None, None

    def get_chromatograms(self):
        if cf.settings().value("view/oddeven", type=bool):
            chroms = []
            for i in self.dataset:
                for j in (0, 1):
                    chroms.append([i[0][ax, :][j::2] for ax in (0, 1)])
        else:
            chroms = [i[0] for i in self.dataset]
        return chroms

    def get_spectra(self, mint=None, maxt=None):
        mint = mint or self.mintime
        maxt = maxt or self.maxtime
        args = self.get_chromargs(mint, maxt)
        spectra = []
        for i, subset in enumerate(self.dataset):
            if cf.settings().value("view/oddeven", type=bool):
                for j in (0, 1):
                    if len(subset[2][args[i*2+j][j::2]]):
                        yvalz = np.mean(subset[2][args[i*2+j][j::2]], axis=0)
                        spectra.append([subset[1], yvalz])
                    else:
                        spectra.append([[], []])
            else:
                if len(subset[2][args[i]]):
                    yvalz = np.mean(subset[2][args[i]], axis=0)
                    spectra.append([subset[1], yvalz])
                else:
                    spectra.append([[], []])
        return spectra

    def get_peakchrom(self, startmass, endmass):
        intensity = np.concatenate([np.divide(np.sum(subset[2].T[
            dt.argsubselect(subset[1], startmass, endmass)].T, axis=1),
            np.clip(subset[0][1], np.finfo(np.float32).eps, None))
            for subset in self.dataset])
        return intensity


class BrukerTimsDataset(Dataset):
    def __init__(self, rawfile):
        super().__init__(rawfile)
        self.refresh()

    def refresh(self):
        logger.info("refreshing timsTOF dataset")
        if(os.path.isdir(self.filename)):
            self.dataset = OpenTIMS(pathlib.Path(self.filename))
        else:
            self.dataset = OpenTIMS(
                    pathlib.Path(os.path.dirname(self.filename)))
        self.chromatograms = self.get_chromatograms()
        self.mintime, self.maxtime = [self.chromatograms[i][0][i]
                                      for i in (0, -1)]

    def sampletimes(self, mint, maxt, timescap):
        frames = dt.argsubselect(self.dataset.retention_times,
                                 mint*60, maxt*60) + 1
        framessel = frames if timescap >= len(frames) else np.linspace(
                frames[0], frames[-1], timescap).astype('int')
        return framessel

    def binit(self, x, y, minstep, length):
        sortx = np.sort(x)
        stepsx = sortx[1:] - sortx[:-1]
        binspos = np.where(stepsx > minstep)[0]
        bins = sortx[:-1][binspos] + (stepsx[binspos]/2)
        binpos = np.digitize(x, bins)
        bindx = np.bincount(binpos, x) / np.bincount(binpos)
        bindy = np.bincount(binpos, y) / length
        return bindx, bindy

    def get_chromatograms(self):
        logger.info("getting timsTOF chromatogram")
        times = self.dataset.retention_times / 60
        # Thx to Michał Startek, slight deviation, but much faster
        intensities = (self.dataset.frames['SummedIntensities'] *
                       self.dataset.frames['AccumulationTime']) / 100.0
        return [[times, intensities]]

    def get_spectra(self, mint=None, maxt=None):
        logger.info("getting timsTOF spectra")
        mint = mint or self.mintime
        maxt = maxt or self.maxtime
        framessel = self.sampletimes(mint, maxt, cf.settings().value(
                                         "timstof/ms_sampling", type=int))
        massints = self.dataset.query(framessel, columns=('mz', 'intensity'))
        masses, ints = self.binit(
            massints['mz'], massints['intensity'],
            cf.settings().value("timstof/ms_bins", type=float), len(framessel))
        return [[masses, ints]]

    def get_mobspectra(self, mint=None, maxt=None):
        logger.info("getting timsTOF spectra")
        mint = mint or self.mintime
        maxt = maxt or self.maxtime
        framessel = self.sampletimes(mint, maxt, cf.settings().value(
                                         "timstof/ms_sampling", type=int))
        massints = self.dataset.query(framessel, columns=('inv_ion_mobility', 'intensity'))
        masses, ints = self.binit(
            massints['inv_ion_mobility'], massints['intensity'],
            cf.settings().value("timstof/mob_bins", type=float), len(framessel))
        return [[masses, ints]]

    def get_peakchrom(self, startm, endm):
        logger.info("getting peak ion chromatogram")
        intensity = np.divide([
            np.sum(i['intensity'][dt.argsubselect(i['mz'], startm, endm)])
            for i in self.dataset.query_iter(
                np.arange(self.dataset.max_frame)+1, columns=('intensity', 'mz'))],
            np.clip(self.chromatograms[0][1], np.finfo(np.float32).eps, None))
        return intensity

    def get_subspace(self, xax, subselect, start, end, bins,
                     mint=None, maxt=None):
        mint = mint or self.mintime
        maxt = maxt or self.maxtime
        logger.info(("getting timsTOF for {:.3f}-{:.3f} minutes, subselecting"
                     " {}: {}-{}").format(mint, maxt, subselect, start, end))
        framessel = self.sampletimes(mint, maxt, cf.settings().value(
                                         "timstof/mob_sampling", type=int))
        massintstof = self.dataset.query(
                framessel, columns=(subselect, 'intensity', xax))
        goodargs = dt.argsubselect(massintstof[subselect], start, end)
        mobs, ints = self.binit(
            massintstof[xax][goodargs], massintstof['intensity'][goodargs],
            cf.settings().value("timstof/{}".format(bins), type=float),
            len(framessel))
        return mobs, ints
        maxt = maxt or self.maxtime

    def get_mobilogram(self, startm, endm, mint=None, maxt=None):
        x, y = self. get_subspace('inv_ion_mobility', 'mz',
                                  startm, endm, 'mob_bins', mint, maxt)
        return x, y

    def get_ms_onmob(self, startm, endm, mint=None, maxt=None):
        x, y = self.get_subspace('mz', 'inv_ion_mobility',
                                 startm, endm, 'ms_bins', mint, maxt)
        return x, y
