
import cv2 as cv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib outline
from matplotlib.animation import FuncAnimation
from pandas.core.indexes import interval

import serial
import threading
import re


a = 13
b = 25
c = [a,b,a*b]
plt.plot(c)







ser = serial.Serial('com6',115200)

%matplotlib auto

data = pd.read_csv(r'/home/lihuiliu/mnt/workspace/battery_log/report1.txt',\
  names=['origin_v','origin_i','v','i_low','i_high'],header=None,\
  dtype = str)

data_na = data.dropna(how='any').reset_index(drop=True)

data_int = pd.DataFrame(index=np.arange(len(data_na.index)),columns=['v','i_low','i_high'])
for i in data_na.index:
  data_int.loc[i] = [int(data_na.v[i],16),int(data_na.i_low[i],16),int(data_na.i_high[i],16)]

data_np = np.array(data_int)


def set_gpus(gpu_index):
    if type(gpu_index) == list:
        gpu_index = ','.join(str(_) for _ in gpu_index)
    if type(gpu_index) ==int:
        gpu_index = str(gpu_index)
    os.environ["CUDA_VISIBLE_DEVICES"] = gpu_index


fig, ax = plt.subplots()
x,y = [], []
line, = plt.plot([],[],'.-',color='green')
nums = 10000
#i = np.linspace(0,len(data_np),len(data_np)+1)
i = np.arange(0,len(data_np),1000)

def init():
  ax.set_xlim(0,100000)
  ax.set_ylim(-1,30)
  return line

def update(step):
  #x.append(step)
  x = np.arange(0,100000)
  #y.append(np.cos(step/3)+np.sin(step**2))
  y = ((data_np[0+step:100000+step,1]+data_np[0+step:100000+step,2]*256)/100)
  line.set_data(x,y)
  return line

ani = FuncAnimation(fig,update,frames=i,\
  init_func=init,interval=100)
#ani = FuncAnimation(fig,update,frames=np.linspace(0,13*np.pi,128),\
#  init_func=init,interval=20)

plt.show()







subplot(2,1,1);
plot(data(:,1)/10);
subplot(2,1,2);
plot((data(:,2)+data(:,3)*256)/100);
figure;
hold on;
plot(data(:,3)/10);
plot();