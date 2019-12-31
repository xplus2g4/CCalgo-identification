import numpy as np
from scipy.signal import find_peaks, peak_widths
from matplotlib import pyplot as plt
from utils import smooth, plotGraph, getDerivative
from enum import Enum

class CC_Algo(Enum):
  BBR = 1
  Copa = 2
  PCC_Vivace = 3

def isBBR(throughput, time, RTT=0.105):
  peaks, properties = find_peaks(throughput, prominence=0.6)
  freq = np.average(np.diff(time[peaks]))

  # plt.plot(time, throughput)
  # plt.plot(time[peaks], throughput[peaks], "x")
  # plt.show()
  # print(abs(freq - 8 * RTT))

  return True if abs(freq - 8 * RTT) < 0.1 else False

def isCopa(throughput, time, RTT=0.105):
  peaks, properties = find_peaks(throughput, prominence=0.7)
  freq = np.average(np.diff(time[peaks]))

  # plt.plot(time, throughput)
  # plt.plot(time[peaks], throughput[peaks], "x")
  # plt.show()
  # print(abs(freq - 8 * RTT))

  return True if abs(freq - 5 * RTT) < 0.1 else False

def isVivace(throughput, time):
  pass
