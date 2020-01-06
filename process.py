import sys
import csv
from utils import *
import classifiers
from matplotlib import pyplot as plt
import numpy as np

INPUT_PATH = "../Results/Classifier Benchmarking/"
OUTPUT_PATH = "Graphs/"
WINDOW = 0.1
RTT = 0.125
START_TIME = 6
END_TIME = 10
MOVING_AVERAGE_BOX = 40

# Change/Add the destination IPs to newer IPs as required. This IP is of the machine where receiver runs
RECEIVER_IP = ("34.87.0.255", "3.135.64.30")

def loadData(input_name):
  input_csv = csv.reader(open(INPUT_PATH + input_name, 'r'))

  throughput = []
  throughput_time = []

  size = []
  time = []
  for a in input_csv:
      destination = a[2]
      if (destination in RECEIVER_IP):
          time.append(float(a[0]))
          size.append(float(a[1]))
  start_time = 0
  start_sum = 0
  i_fp = 0
  i_bp = 0
  for val in time:
      if val-start_time > WINDOW:
          throughput.append(start_sum/(val-start_time))
          throughput_time.append(val)
          start_sum -= size[i_fp]
          i_fp += 1
          start_time = time[i_fp]
      
      start_sum += size[i_bp]
      i_bp += 1

  throughput = [float(8*i/1000000) for i in throughput]
  start_idx = 0
  end_idx = 0
  for i in range(len(throughput_time)):
    if (throughput_time[i]>=START_TIME):
      start_idx = i
      break
  for i in range(len(throughput_time)-1, start_idx, -1):
    if (throughput_time[i-1]<=END_TIME):
      end_idx = i
      break
  return (np.asarray(throughput_time[start_idx:end_idx]), np.asarray(throughput[start_idx:end_idx]))

def plotSingle(file_name):
  time, throughput = loadData(file_name)
  plt.plot(time, throughput)
  plt.show()

def processSingle(file_name):
  time, throughput = loadData(file_name)
  found = -2
  if classifiers.isVivace(time, throughput, RTT):
    found = classifiers.CC_Algo.PCC_Vivace if found == -2 else classifiers.CC_Algo.Unknown
  if classifiers.isBBR(time, throughput, RTT):
    found = classifiers.CC_Algo.BBR if found == -2 else classifiers.CC_Algo.Unknown
  if classifiers.isCopa(time, throughput, RTT):
    found = classifiers.CC_Algo.Copa if found == -2 else classifiers.CC_Algo.Unknown
  if found == -2:
    found = classifiers.CC_Algo.Unknown
  return found

# Param $1 -> Number of files going to be processed. Note that the files should be named in sender${index}.csv
def processMultiple(data):
  file_count = sys.argv[1]
  bbr_count = 0
  vivace_count = 0
  copa_count = 0
  unknown_count = set()

  for i in range(1, int(file_count)+1):
    result = processSingle(data+"sender"+str(i)+".csv")
    if (result == classifiers.CC_Algo.BBR):
      bbr_count+=1
    if (result == classifiers.CC_Algo.PCC_Vivace):
      vivace_count+=1
    if (result == classifiers.CC_Algo.Copa):
      copa_count+=1
    if (result == classifiers.CC_Algo.Unknown):
      unknown_count.add(i)
  
  return np.array([bbr_count, vivace_count, copa_count, unknown_count])

def main():

  #plotSingle("vivace_data/sender1.csv")
  counts = processMultiple("vivace_data/")

  print("BBR count: " + str(counts[0]))
  print("Vivace count: " + str(counts[1]))
  print("Copa count: " + str(counts[2]))
  print("Unknowns: " + str(counts[3]))

if __name__ == "__main__":
    main()
