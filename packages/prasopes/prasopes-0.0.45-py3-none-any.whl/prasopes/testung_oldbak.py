#!/usr/bin/env python3
import datasets_oldbak as datasets
import numpy as np
from matplotlib import pyplot as plt

print("hello")
mySett = datasets.BrukerTimsDataset('/home/yan/roithPhD/sw_modd/msresearch/opentims_spektra/210211_PEG600_TIMS_Detect_Calibrated.d')


massints = mySett.get_spectra()

print(mySett.dataset)
masses = np.concatenate([i[0] for i in massints])
intensities =np.concatenate([i[1] for i in massints])
sortmasses = np.sort(np.concatenate([i[0] for i in massints]))
masssteps = sortmasses[1:] - sortmasses[:-1]
binspos = np.where(masssteps > 0.001)[0]
bins = sortmasses[:-1][binspos] + (masssteps[binspos]/2)
binposs = np.digitize(masses, bins)
bindmasses = np.bincount(binposs, masses) / np.bincount(binposs)
bindints = np.bincount(binposs, intensities) / np.bincount(binposs)
#print(bindmasses)

for i,j in enumerate(massints):
        plt.plot(j[0], j[1], marker='o', markersize=0.5, linestyle='None')
plt.plot(bins, np.zeros(bins.shape), marker='o', markersize=2, linestyle='None')
plt.plot(bindmasses, bindints)
plt.show()

