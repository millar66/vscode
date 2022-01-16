 import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib auto
#%matplotlib inline
from matplotlib.animation import FuncAnimation
from pandas.core.indexes import interval
# from tkinter import *
# import tkinter.filedialog
# root = Tk()
# def xz():
#     filename = tkinter.filedialog.askopenfilename()
#     if filename != '':
#         lb.config(text = "您选择的文件是："+filename);
#     else:
#         lb.config(text = "您没有选择任何文件");
#     return filename

# lb = Label(root,text = '')
# lb.pack()
# btn = Button(root,text="弹出选择文件对话框",command=xz)
# btn.pack()
# root.mainloop()
import tkinter as tk
from tkinter import filedialog

root=tk.Tk()
root.withdraw()
#FolderPath=filedialog.askdirectory()  #看情况自己使用
FilePath=filedialog.askopenfilenames()
#print('FolderPath:',FilderPath)
#print('FilePath:',FilePath)
datafile = []
for i in np.arange(len(FilePath)):
  datafile.append(pd.read_csv(FilePath[i],\
    names=['origin_v','origin_i','v','i_low','i_high'],header=None,\
    dtype = str))
data = pd.concat(datafile)

data_na = data.fillna('0')
data_np = np.array(data_na)
data_int = data_np.copy()
data_times = []
for i in np.arange(len(data_np)):
  for j in [2,3,4]:
    data_int[i][j] = int(data_np[i][j],16)
charge_index = np.where(data_int=='eeee')
charge = []
charge.append(data_int[charge_index[0]+1])
charge_int = charge.copy()
for i in np.arange(len(charge[0])):
  charge_int[0][i][1] = int(charge[0][i][1],16)
start_data = np.where(data_int=='aaaa')
end_data = np.where(data_int=='5555')
delete_index = []
data_data = np.delete(data_int,np.hstack((charge_index[0],charge_index[0]+1,\
                  charge_index[0]+2,start_data[0],end_data[0])),0)
current = (data_data[:,3]+data_data[:,4]*256)/100
charge_list = charge_int[0][:,1]+charge_int[0][:,2]*256
charge_ones_times = charge_list.copy()
for i in np.arange(len(charge_list)-1):
  charge_ones_times[i] = charge_list[i+1]-charge_list[i]
charge_ones_times[-1] = charge_ones_times[-1]/100
p1 = plt.plot(data_data[:,2]/10,label='v',color='b')
p2 = plt.plot(current,label='i',color='r')
p3 = plt.scatter(charge_index[0]+1,charge[0][:,3])
p4 = plt.scatter(charge_index[0]+1,charge_ones_times)

for c, d in zip(charge_index[0]+1, charge[0][:,3]):
    plt.text(c, d, d, ha='center', va='bottom', fontsize=10)

for a, b in zip(charge_index[0]+1, charge_ones_times):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=10)
plt.show()