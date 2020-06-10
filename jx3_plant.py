# coding:utf-8
'''
Author  : 夜雨流@破阵子
Date    : 2020.5.27
Version : V1.0
'''
import tkinter as tk
from pynput import mouse
from pynput import keyboard
from pynput.mouse import Button, Controller
import time
import _thread

# plant main function
def processing(operator):
    global FlowerpotCoords
    global ButtonCoords
    mouse = Controller()
    for fc, bc in zip(FlowerpotCoords, ButtonCoords):
        var.set(operator + 'ing......')
        mouse.position = fc
        mouse.click(Button.right, 1)
        time.sleep(0.5)
        mouse.position = bc
        mouse.click(Button.left, 1)
        time.sleep(0.5)

def main():
    global FlowerpotCoords
    global ButtonCoords
    if not (len(FlowerpotCoords) == NUM_FLOWERPOT and len(ButtonCoords) == NUM_FLOWERPOT):
        var.set('无法种花，还没记录位置')
    else:
        while len(FlowerpotCoords) > 0:
            processing('种花')
            for t in range(610)[::-1]:
                if len(FlowerpotCoords) == 0:
                    break
                var.set('%d秒后进行收花' % t)
                time.sleep(1)
            processing('收花')

def multi_thread_main():
    _thread.start_new_thread(main, ())

# count click
def on_click(x, y, button, pressed):
    global FlowerpotCoords
    mouse = Controller()
    if button.name == 'right' and pressed:
        FlowerpotCoords.append(mouse.position)
        var.set('记录中(左键%d次右键%d次)' % (len(ButtonCoords), len(FlowerpotCoords)))
    if button.name == 'left' and pressed:
        ButtonCoords.append(mouse.position)
        var.set('记录中(左键%d次右键%d次)' % (len(ButtonCoords), len(FlowerpotCoords)))
    if len(FlowerpotCoords) == NUM_FLOWERPOT and len(ButtonCoords) == NUM_FLOWERPOT:
        var.set('记录成功！！！请种花！！！')
        return False
    elif len(FlowerpotCoords) > NUM_FLOWERPOT or len(ButtonCoords) > NUM_FLOWERPOT:
        var.set('记录失败！！！(左键%d次右键%d次)' % (len(ButtonCoords), len(FlowerpotCoords)))
        return False

# reset
def reset(plot=False):
    global FlowerpotCoords
    global ButtonCoords
    FlowerpotCoords = []
    ButtonCoords = []
    if plot:
        var.set('已清空位置记录')

# listen mouse
def listen():
    global FlowerpotCoords
    global ButtonCoords
    reset()
    var.set('请收一次花，以便记录鼠标位置')
    listener = mouse.Listener(on_click=on_click)
    listener.start()

def stop():
    reset()
    var.set('种花快乐(●◡●)Author：夜雨流@破阵子')

if __name__ == '__main__':
    NUM_FLOWERPOT = 15
    FlowerpotCoords = []
    ButtonCoords = []

    # set window
    root = tk.Tk()
    root.title('剑网3种花精灵V1.0——Produced by 夜雨流@破阵子')
    root.geometry('420x100')

    # set label
    var = tk.StringVar()
    var.set('点击按钮记录位置')
    label = tk.Label(root, textvariable=var, bg='red', font=('Arial', 12), width=30, height=2)
    label.pack()

    # set location button
    flowerpot = tk.Button(root, text="记录位置", command=listen)
    flowerpot.place(x=10, y=40, width=100, height=40)

    # set run button
    run = tk.Button(root, text="开始种花", command=multi_thread_main)
    run.place(x=110, y=40, width=100, height=40)

    # set stop button
    stop = tk.Button(root, text="停止种花", command=stop)
    stop.place(x=210, y=40, width=100, height=40)

    # set reset button
    button = tk.Button(root, text="重置", command=lambda: reset(plot=True))
    button.place(x=310, y=40, width=100, height=40)

    root.mainloop()
