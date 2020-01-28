import numpy as np
from matplotlib import pyplot as plt

# Smoothening function. Just a moving average
def smooth(y, box_pts):
  box = np.ones(box_pts)/box_pts
  y_smooth = np.convolve(y, box, mode='same')
  return y_smooth

def getDerivative(time, throughput):
  np_time = np.array(time, dtype=float)
  derivative = np.array(throughput, dtype=float)
  derivative = np.gradient(derivative, np_time)
  return derivative

def plotGraph(time, curves, label, output_name,
  title="Throughput vs Time",
  xlabel="Time (Seconds)",
  ylabel="Throughput (Mbps)",
  xtick=0.5
  ):
  plt.title(title)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.xticks(np.arange(min(time), max(time)+0.1, xtick))
  for curve in curves:
    plt.plot(time, curve, 'b', label=label)
  plt.tight_layout()
  plt.legend()
  plt.savefig(output_name)
  plt.close()
