import numpy as np
from scipy.signal import find_peaks, peak_widths, butter, lfilter, freqz
from matplotlib import pyplot as plt
from utils import smooth, plotGraph, getDerivative
from enum import Enum

class CC_Algo(Enum):
  BBR = 1
  Copa = 2
  PCC_Vivace = 3
  Unknown = -1

def isBBR(time, throughput, RTT):
  #RTT+=0.01
  samples_per_RTT = int(len(time)/(time[-1]-time[0])) * RTT
  throughput = smooth(throughput, 10)[3:-3]
  time=time[3:-3]
  peaks, properties = find_peaks(throughput, width=samples_per_RTT, prominence=0.15)
  diffs = np.diff(time[peaks])
  
  if (len(diffs) == 0 or np.var(diffs) > 0.025):
    # print(np.var(diffs))
    # plt.plot(time, throughput)
    # plt.plot(time[peaks], throughput[peaks], "x")
    # plt.show()
    return False
  
  freq = np.average(diffs)

  # if not isClose(freq, 8 * RTT, RTT*1.3):
  #   print(freq, 8*RTT)
  #   plt.plot(time, throughput)
  #   plt.plot(time[peaks], throughput[peaks], "x")
  #   plt.show()
  #print(freq)
  return True if isClose(freq, 8 * RTT, threshold=RTT*1.3) else False

def isCopa(time, throughput, RTT):
  RTT+=0.01
  samples_per_RTT = int(len(time)/(time[-1]-time[0])) * RTT
  throughput = smooth(throughput, int(samples_per_RTT))[5:-5]
  time=time[5:-5]
  peaks, properties = find_peaks(throughput, distance=3 * samples_per_RTT, width=samples_per_RTT, prominence=0.1)
  diffs = np.diff(time[peaks])

  # # print(np.var(diffs))
  # plt.plot(time, throughput)
  # plt.plot(time[peaks], throughput[peaks], "x")
  # plt.show()

  if (len(diffs) == 0 or np.var(diffs) > 0.085):
    # print(np.var(diffs))
    # plt.plot(time, throughput)
    # plt.plot(time[peaks], throughput[peaks], "x")
    # plt.show()
    return False

  freq = np.average(diffs)
  # if isClose(freq, 5 * RTT, threshold=RTT*1.1):
  #   print(freq, 5*RTT)
  #   plt.plot(time, throughput)
  #   plt.plot(time[peaks], throughput[peaks], "x")
  #   plt.show()
  return True if isClose(freq, 5 * RTT, threshold=RTT*1.1) else False

def isVivace(time, throughput, RTT):
  samples_per_RTT = int(len(time)/(time[-1]-time[0])) * RTT
  derivative = getDerivative(time, throughput)
  peaks, _ = find_peaks(derivative, prominence=1, distance=0.5*samples_per_RTT)
  diffs = np.diff(time[peaks])

  if (len(diffs) == 0 or np.var(diffs) > 0.0005):
    # fig, axs = plt.subplots(2)
    # axs[0].plot(time, throughput)
    # axs[1].plot(time, derivative)
    # axs[1].plot(time[peaks], derivative[peaks], "x")
    # plt.show()
    return False

  freq = np.average(diffs)

  # if not isClose(freq, RTT*0.9, 0.5*RTT):
  #   print(freq, RTT*0.9)
  #   fig, axs = plt.subplots(2)
  #   axs[0].plot(time, throughput)
  #   axs[1].plot(time, derivative)
  #   axs[1].plot(time[peaks], derivative[peaks], "x")
  #   plt.show()

  return True if isClose(freq, RTT*0.9, 0.5*RTT) else False

def isClose(value1, value2, threshold=0.1):
  return True if abs(value1 - value2) < threshold else False
