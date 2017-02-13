from tkinter import *
from tkinter.filedialog import *
import math
import numpy as np


def draw(canv, from_t, to_t):
    global scale
    for t in np.arange(from_t, to_t, 0.001):
        x = (12 * math.cos(t)*scale - 5 * math.cos(12 / 5 * t) * scale)+20
        y = (12 * math.sin(t)*scale - 5 * math.sin(12 / 5 * t) * scale)+20
        canv.create_oval(x * scale, y * scale, x * scale + 1, y * scale + 1)

def change_scale(event):
    global scale, cnv
    scale += 1
    cnv.destroy()
    cnv_new = Canvas(root, height=100 * scale, width=200 * scale)
    cnv_new.delete('all')
    draw(cnv_new, 0, 4 * math.pi)
    cnv_new.pack()
    cnv = cnv_new

root = Tk()
scale = 1

but = Button(root)
but["text"] = "Масштабировать"

cnv = Canvas(root, height=100*scale, width=100*scale)
draw(cnv, 0, 4 * math.pi)
but.bind("<Button-1>", change_scale)


but.pack()
cnv.pack()

root.mainloop()