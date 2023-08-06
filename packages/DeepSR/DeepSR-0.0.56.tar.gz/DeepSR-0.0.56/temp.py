import sys
from sys import argv
from os import  makedirs, rename
from os.path import isfile, join, exists, splitext, abspath, basename, dirname, isdir
import numpy as np
from scipy.io import loadmat
import LossHistory



lss = LossHistory.LossHistory()