######
#timer
######
# based on Aarons answer here:
# https://stackoverflow.com/questions/41643538/python-capture-user-input-while-in-loop-executing-other-code/41643837
import time
import datetime
from threading import Thread,Lock
#import ctypes  # An included library with Python install.
#import easygui
import tkinter.messagebox


time_input=input("How long hh-mm-ss: ")
time_input=time_input.split('-')
target_time = float(time_input[0])*3600. + float(time_input[1])*60. + float(time_input[2])

class globalVars():
    pass

G = globalVars() #empty object to pass around global state
G.lock = Lock() #not really necessary in this case, but useful none the less
G.remain = 0
G.end = 0
G.start=datetime.datetime.now()
G.kill = False
G.pause = 0
G.tpause = 0

def convert_tdelta(t):
    """
    convert datetime difference to [dd,hh,mm,ss]
    """
    dd = t.days
    temp = t.seconds
    hh = int(temp/3600.)
    temp = temp-hh*3600.
    mm = int(temp/60.)
    temp = temp-mm*60.
    return [dd,hh,mm,temp]

def timer(sec):
    """
    timer function
    """
    G.end=datetime.datetime.now()+datetime.timedelta(0,sec)
    while datetime.datetime.now() < G.end:
        if G.kill:
            G.kill = False
            return
        with G.lock:
            G.remain = G.end-datetime.datetime.now()
    popup("TIMER ended - start: {} end: {}\nduration: {}\npaused: {}".format(G.start,G.end,"{} days, {} hours, {} minutes, {} secs".format(*convert_tdelta(G.end-G.start)),G.pause))

def popup(text):
    #ctypes.windll.user32.MessageBoxW(0, text, "TIMER", 1)
    #easygui.msgbox(text, title="TIMER")
    window = tkinter.Tk()
    window.wm_withdraw()
    tkinter.messagebox.showinfo(title="TIMER", message=text)
    #destroy window on okay
    window.destroy()
    #kill askinput
    G.kill = True

t = Thread(target=timer, args=(target_time,))
t.start()

def askinput():
    choice = input("#####\n1: pause\n2: continue\n3: get G.remain\n4: get t.isAlive()\n5: kill thread\nq: exit\ninput: ")
    if choice == "1":
        G.kill = True
        G.tpause=datetime.datetime.now()
        print("TIMER - Paused")
    elif choice == "2":
        dtpause = datetime.datetime.now()-G.tpause
        G.pause += dtpause.days*3600. + dtpause.seconds
        remaining = G.remain.days*3600.+G.remain.seconds
        print("TIMER - Continuing: ", remaining)
        t = Thread(target=timer, args=(remaining,))
        t.start()
    elif choice == "3":
        #with G.lock:
        print("TIMER - Time remaining (dd-hh-mm-ss): {} ".format(convert_tdelta(G.remain)))
    elif choice == "4":
        try:
            print(t.is_alive())
        except:
            print (False)
    elif choice == "5":
        G.kill = True
    elif choice == "q":
        return 0
    else:
        pass
    return 1

while askinput():
    pass

