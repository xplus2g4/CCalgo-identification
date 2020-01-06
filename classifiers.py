import numpy as np
from scipy.signal import find_peaks, peak_widths
from matplotlib import pyplot as plt
from utils import smooth, plotGraph, getDerivative
from enum import Enum

class CC_Algo(Enum):
  BBR = 1
  Copa = 2
  PCC_Vivace = 3
  Unknown = -1

def isBBR(time, throughput, RTT):
  peaks, properties = find_peaks(throughput, distance=35, prominence=0.2)
  diffs = np.diff(time[peaks])

  # plt.plot(time, throughput)
  # plt.plot(time[peaks], throughput[peaks], "x")
  # plt.show()
  
  if (len(diffs) == 0 or np.var(diffs) > 0.02):
    return False
  
  freq = np.average(diffs)
  return True if isClose(freq, 8 * RTT) else False

def isCopa(time, throughput, RTT):
  peaks, properties = find_peaks(throughput, distance=20, prominence=0.2)
  diffs = np.diff(time[peaks])
  
  # plt.plot(time, throughput)
  # plt.plot(time[peaks], throughput[peaks], "x")
  # plt.show()

  if (len(diffs) == 0 or np.var(diffs) > 0.02):
    return False
  
  freq = np.average(diffs)
  return True if isClose(freq, 5 * RTT) else False

def isVivace(time, throughput, RTT):
  derivative = getDerivative(time, throughput)
  peaks, _ = find_peaks(abs(derivative), prominence=1, distance=25)

  # plt.plot(time, abs(derivative))
  # plt.plot(time[peaks], abs(derivative)[peaks], "x")
  # plt.show()

  return True if isClose(np.average(np.diff(time[peaks])), RTT*0.6) else False

def isClose(value1, value2, threshold=0.1):
  return True if abs(value1 - value2) < threshold else False
