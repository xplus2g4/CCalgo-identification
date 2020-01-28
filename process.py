import sys
import csv
from utils import *
import classifiers
from matplotlib import pyplot as plt
import numpy as np
from os import rename, listdir
from os.path import isfile, join

INPUT_PATH = "../Results_2/SG-Ohio"
WINDOW = 0.1
START_TIME = 5
END_TIME = 10
MOVING_AVERAGE_BOX = 40

# Change/Add the destination IPs to newer IPs as required. This IP is of the machine where receiver runs
RECEIVER_IP = ("34.87.0.255", "3.135.64.30", "18.136.106.11")

# Load data, return {rtt, throughput, time}
def loadData(sender_name):
  sender_csv = csv.reader(open(sender_name, 'r'))

  rtt = 0.001 * int(sender_name.split('sender')[1].split('-')[1])
  sender_throughput=[]
  sender_time=[]

  size=[]
  time=[]
  for row in sender_csv:
    destination = row[3]
    if (destination in RECEIVER_IP):
      time.append(float(row[1]))
      size.append(float(row[2]))

  start_time = 0
  start_sum = 0
  i_fp = 0
  i_bp = 0
  for val in time:
    if val-start_time > WINDOW:
      sender_throughput.append(start_sum/(val-start_time))
      sender_time.append(val)
      start_sum -= size[i_fp]
      i_fp += 1
      start_time = time[i_fp]
    start_sum += size[i_bp]
    i_bp += 1

  sender_throughput = [float(8*i/1000000) for i in sender_throughput]
  start_idx = 0
  end_idx = 0
  for i in range(len(time)):
    if (time[i]>=START_TIME):
      start_idx = i
      break
  for i in range(len(time)-1, start_idx, -1):
    if (time[i-1]<=END_TIME):
      end_idx = i
      break
  
  return {
    'time': np.asarray(sender_time[start_idx:end_idx]), 
    'throughput': np.asarray(sender_throughput[start_idx:end_idx]),
    'rtt': rtt
  }

def plotSingle(file_name):
  data = loadData(file_name)
  time, throughput = data['time'], data['throughput']

  #plt.title("Throughput of PCC-Vivace over time")
  plt.xlabel("Time (Seconds)")
  plt.ylabel("Throughput (Mbps)")
  plt.xticks(np.arange(START_TIME, END_TIME+1, 0.2))
  plt.plot(time, throughput, 'b')
  plt.tight_layout()
  # plt.show()
  # plt.legend()
  plt.savefig("Copa_steady")
  plt.close()

def processSingle(file_name):
  data = loadData(file_name)
  rtt, time, throughput = data['rtt'], data['time'], data['throughput']

  found = -2
  if classifiers.isVivace(time, throughput, rtt):
    found = classifiers.CC_Algo.PCC_Vivace if found == -2 else classifiers.CC_Algo.Unknown
  if classifiers.isCopa(time, throughput, rtt):
    found = classifiers.CC_Algo.Copa if found == -2 else classifiers.CC_Algo.Unknown
  if classifiers.isBBR(time, throughput, rtt):
    found = classifiers.CC_Algo.BBR if found == -2 else classifiers.CC_Algo.Unknown
  if found == -2:
    found = classifiers.CC_Algo.Unknown
  return found

# Param $1 -> Number of files going to be processed. Note that the files should be named in sender${index}.csv
def processMultiple(algo):
  FINAL_INPUT_PATH = join(INPUT_PATH, algo)
  sender_files = [f for f in listdir(FINAL_INPUT_PATH) if isfile(join(FINAL_INPUT_PATH, f)) and f[0]=='s']

  bbr_count = 0
  vivace_count = 0
  copa_count = 0
  unknown_count = set()

  for sender_file in sender_files:
    result = processSingle(join(FINAL_INPUT_PATH, sender_file))
    if (result == classifiers.CC_Algo.BBR):
      bbr_count+=1
    if (result == classifiers.CC_Algo.PCC_Vivace):
      vivace_count+=1
    if (result == classifiers.CC_Algo.Copa):
      copa_count+=1
    if (result == classifiers.CC_Algo.Unknown):
      unknown_count.add(sender_file.split('.')[0])
  
  return np.array([bbr_count, vivace_count, copa_count, unknown_count])

def change_name(shift, algo):
  FINAL_INPUT_PATH = join(INPUT_PATH, algo)
  sender_files = [f for f in listdir(FINAL_INPUT_PATH) if isfile(join(FINAL_INPUT_PATH, f)) and f[0]=='s']
  for old_name in sender_files:
    split_name = old_name.split('-')
    idx = int(split_name[2].split('.')[0])
    # if idx >= 80:
    #   continue
    split_name[2] = str(idx+shift)+'.csv'
    new_name_path = join(FINAL_INPUT_PATH, split_name[0]+'-'+split_name[1]+'-'+split_name[2])
    old_name_path = join(FINAL_INPUT_PATH, old_name)
    rename(old_name_path, new_name_path)

def main():

  # plotSingle("copa/sender1.csv")

  counts = processMultiple("bbr")
  print("BBR count: " + str(counts[0]))
  print("Vivace count: " + str(counts[1]))
  print("Copa count: " + str(counts[2]))
  print("Unknowns: " + str(counts[3]))
  
  #change_name(algo='bbr', shift=50)

if __name__ == "__main__":
    main()
