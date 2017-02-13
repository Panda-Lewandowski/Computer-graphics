from tkinter import *
from tkinter.filedialog import *
import math

def draw(event):
    a = ent1.get()
    b = ent2.get()
    a = str_to_int(a)
    b = str_to_int(b)

    if a is None or b is None:
        return
    cnv.delete('all')
    layout()
    for i in range(len(a)):
        cnv.create_oval(a[i][0] * scale + 10, a[i][1] * scale + 10, (a[i][0] + 1) * scale + 10,
                        (a[i][1] + 1) * scale + 10, fill="green")
    for i in range(len(b)):
        cnv.create_oval(b[i][0] * scale + 10, b[i][1] * scale + 10, (b[i][0] + 1) * scale + 10,
                        (b[i][1] + 1) * scale + 10, fill="red")


def str_to_int(a):
    if a == '':
        return None
    a = a.split(' ')  # TODO а вдруг пустая строка
    for i in range(len(a)):
        a[i] = a[i].split(',')
        for j in [0, 1]:
            a[i][j] = int(a[i][j])
    return a


def layout():
    cnv.create_line(10, 0, 10, 100 * scale, width=1, arrow=LAST)
    cnv.create_line(0, 10, 100 * scale, 10, width=1, arrow=LAST)


def distance_between_points(xy1, xy2):
    x_1 = xy1[0]
    x_2 = xy2[0]
    y_1 = xy1[1]
    y_2 = xy2[1]
    dis = math.sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2)
    return dis


def calc(a):

    return

root = Tk()

scale = 5
#1,1 2,14 82,12 9,3 8,14 50,52 92,7
#82,12 62,35 98,14 64,21 3,3 9,5
but = Button(root)
but["text"] = "Отобразить ответ"
ent1 = Entry(root, width=50, bd=3)
ent2 = Entry(root, width=50, bd=3)
lab1 = Label(root, text="Первое можество точек:", font="Times 12")
lab2 = Label(root, text="Второе можество точек:", font="Times 12")

cnv = Canvas(root, height=100*scale, width=100*scale)

but.bind("<Button-1>", draw)


lab1.pack()
ent1.pack()
lab2.pack()
ent2.pack()
but.pack()
cnv.pack()

root.mainloop()
