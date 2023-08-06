#!/usr/bin/env python3
import datasets
from matplotlib import pyplot as plt

print("hello")
mySett = datasets.ThermoRawDataset('/home/yan/skola/PhD_II/sw_modd/msresearch/bench_batch/LTQ.raw')

print(type(mySett))
