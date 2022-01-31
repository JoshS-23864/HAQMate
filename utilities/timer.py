from tkinter import *
import time
import threading

t=10
close = False

def countdown(ti):
    global t
    tk = Tk()
    label1=Label(tk,justify='center')
    label1.pack()
    t = ti
    def clock():
        global close
        global t
        if close:
            tk.destroy()
            return
        mins, secs = divmod(t, 60)
        tex = '{:02d}:{:02d}'.format(mins, secs)
        if t!=0:
            t-=1
            label1.config(text=tex,font='times 25')
        else:
            label1.config(text="time up!",font='times 25')
            return
        tk.after(1000,clock)    
    clock()
    tk.mainloop()



def closeTimer():
    global close
    close = True

# countdown(30)