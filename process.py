import sys
import csv
from utils import *
import classifiers

INPUT_PATH = "./data/"
OUTPUT_PATH = "Graphs/"
WINDOW = 0.1
START_TIME = 5
END_TIME = 8
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

# Param $1 -> Filename of input data
def processSingle():
  file_name = sys.argv[1]
  time, throughput = loadData(file_name)
  classifiers.isBBR
  classifiers.isCopa(throughput, time)

# Param $1 -> Number of files going to be processed. Note that the files should be named in sender${index}.csv
def processMultiple():
  file_count = sys.argv[1]
  bbr_count = 0
  unknown = set()
  for i in range(1, int(file_count)+1):
    time, throughput = loadData("sender"+str(i)+".csv")
    if classifiers.isBBR(throughput, time):
      bbr_count+=1
    else:
      unknown.add(i)
  print(bbr_count)
  print(unknown)

def main():
  processMultiple()
  # curves = [smooth(data_sender[1],MOVING_AVERAGE_BOX)]
  # #curves = [data_sender[1]]
  # derivative = [getDerivative(data_sender[0], smooth(data_sender[1], MOVING_AVERAGE_BOX))]
  # #derivative = [getDerivative(data_sender[0], data_sender[1])]
  # plotGraph(data_sender[0], curves, "test", "test")
  # plotGraph(data_sender[0], derivative, "d", "d")

if __name__ == "__main__":
    main()
