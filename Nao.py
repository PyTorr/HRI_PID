from tkinter import *
from tkinter import messagebox as tkMessageBox
import numpy as np

# from Tkinter import *
# import tkMessageBox
# from PIL import Image
# from resizeimage import resizeimage
import timeit
# import numpy as np
import nao_pid
import pandas as pd


root = Tk()
root.geometry('{}x{}'.format(600, 400))
t = timeit.Timer()
t1 = 0
t2 = 0
rt_kp, rt_ki, rt_kd = 2, 0.05, 0.5
level = 0

shapes = ['circle','triangle', 'square']
colors = ['red','yellow', 'blue']
objects = pd.DataFrame(data = np.array([shapes,colors]).T, columns=['shape','color'])


def helloCallBack(shape_clicked , kid_df):
   global t1, t2, right_shape, level
   # tkMessageBox.showinfo( "Hello Python", "Hello World")
   t2 = t.timer()
   rt = t2-t1 # response time

   s = shape_clicked - right_shape # right/ wrong = 0/1

   # PID
   robot = nao_pid.robot()

   temp_val = [s, rt]
   temp_val = np.array(temp_val, 'float')
   temp_df = pd.DataFrame(data=temp_val.reshape(1, 2), columns=['right','rt'])
   kid_df = kid_df.append(temp_df.round(2))

   rt_pid = nao_pid.PID(rt_kp, rt_ki, rt_kd, np.array(kid_df.rt), robot.setpoint['response_time'], np.float(temp_df.rt))
   vp, lvl = robot.pid_action(s, rt_pid)
   level += lvl
   t1 = t.timer()

   # todo: nao do vp atribute and level
   nao_do(vp, level)

   print('response time: ', np.round(rt,2), np.round(rt_pid,2))
   print('robot actions: ', vp, level)


def Start_callback(number, textWidget):
   global t1, right_shape
   # nao says: .... todo: connect nao

   t1 = 0
   t1 = t.timer()
   textWidget.insert(END, "Game starting\n Good Luck!")

# B = Tkinter.Button(top, text ="Hello", command = helloCallBack)

i1 = PhotoImage(file='01circle.png')
i2 = PhotoImage(file='02triangle.png')
i3 = PhotoImage(file='03square.png')

path1 = '/home/torr/PycharmProjects/HRI_PID/red.gif'

px = 30

kid_df = pd.DataFrame(data=np.zeros([1,2]), columns=['right','rt'])

textWidget = Text(root, width=20, height =1, pady=20)

textWidget.grid(row=2, column=2)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

b1= Button(root, image=i1, text="BUTTON1", command=lambda: helloCallBack(1, kid_df))
b1.grid(row=0, column=0, padx =px, pady = 40, columnspan = 2)


b2 = Button(root, image=i2, text="BUTTON2", command=lambda: helloCallBack(2, kid_df))
b2.grid(row=0, column=2, padx = px, columnspan = 2)

b3 = Button(root, image=i3, text="BUTTON3", command=lambda: helloCallBack(3, kid_df))
b3.grid(row=0, column=4, padx = px, columnspan = 2)

b4 = Button(root, text="Start/ Next", command=lambda: Start_callback(0, textWidget))
b4.grid(row=1, column=2, padx = px, columnspan = 2)


root.geometry('600x400')
# B.pack()
root.mainloop()

print('welcome to our game')


# nao says hello

def nao_say(atribue, level):
   i=0
   if level == 0:
      nao_says = 'can you show me the shape with color' + objects.color[i]
   if level == 1:
      nao_says = 'can you show me the' + objects.shape[i] + 'shape'


def nao_do(atribute, level):
   pass
# chose color or shape as A
# text2speach: can you show me the A shape
# Timer
# Person clicked -> close timer
# check right/ wrong
# take Timer to PID
# robot response


