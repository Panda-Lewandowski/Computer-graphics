from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
import math


def draw(event):
    a = ent1.get()
    b = ent2.get()
    a = str_to_float(a)
    b = str_to_float(b)

    if a is None or b is None:
        showerror('Ошибка', 'Введите точки в формате х,у')
        return
    cnv.delete('all')
    layout()

    cir1, cir2, inter, l1, l2 = calc(a, b)
    if cir1 is None:
        showwarning('Упс', "Окружностей не найдено!")
    else:
        print(cir1, cir2, inter, l1, l2)
        cnv.create_line(l1[0][0] * scale + 10, l1[0][1] * scale + 10,  l1[1][0] * scale + 10, l1[1][1] * scale + 10, fill='darkblue')
        cnv.create_line(l2[0][0] * scale + 10, l2[0][1] * scale + 10, l2[1][0] * scale + 10, l2[1][1] * scale + 10, fill='darkblue')
        cnv.create_oval((cir1[0][0] - cir1[1]) * scale + 10, (cir1[0][1] + cir1[1]) * scale + 10,
                        (cir1[0][0] + cir1[1]) * scale + 10, (cir1[0][1] - cir1[1]) * scale + 10, fill='#FFF0F5')
        cnv.create_oval((cir2[0][0] - cir2[1]) * scale + 10, (cir2[0][1] + cir2[1]) * scale + 10,
                        (cir2[0][0] + cir2[1]) * scale + 10, (cir2[0][1] - cir2[1]) * scale + 10, fill='#E6E6FA')
        cnv.create_oval((cir1[0][0] - 0.2) * scale + 10, (cir1[0][1] - 0.2) * scale + 10, (cir1[0][0] + 0.2) * scale + 10,
                        (cir1[0][1] + 0.2) * scale + 10, fil='#DB7093')
        cnv.create_oval((cir2[0][0] - 0.2) * scale + 10, (cir2[0][1] - 0.2) * scale + 10,
                        (cir2[0][0] + 0.2) * scale + 10,
                        (cir2[0][1] + 0.2) * scale + 10, fil='#9370DB')
        """cnv.create_polygon(cir1[0][0] * scale + 10, cir1[0][1] * scale + 10, l1[0][0] * scale + 10,
                           l1[0][1] * scale + 10, inter[0] * scale + 10, inter[1] * scale, l2[1][0] * scale + 10,
                           l2[1][1] * scale + 10, cir2[0][0] * scale + 10, cir2[0][1] * scale + 10, l1[1][0] * scale + 10,
                           l1[1][1] * scale + 10, inter[0] * scale + 10, inter[1] * scale, l2[1][0] * scale + 10,
                           l2[1][1] * scale + 10, cir1[0][0] * scale + 10, cir1[0][1] * scale + 10)"""
    for i in range(len(a)):
        cnv.create_oval((a[i][0] - 0.2) * scale + 10, (a[i][1] - 0.2) * scale + 10, (a[i][0] + 0.2) * scale + 10,
                        (a[i][1] + 0.2) * scale + 10, fill="green")
    for i in range(len(b)):
        cnv.create_oval((b[i][0] - 0.2) * scale + 10, (b[i][1] - 0.2) * scale + 10, (b[i][0] + 0.2) * scale + 10,
                        (b[i][1] + 0.2) * scale + 10, fill="red")

    tx.delete('1.0', END)
    tx.insert(1.0, "Окружности найдены. \n "
                   "Окружность 1: ее радиус {0:.2f}, координаты центра ({1:.2f}, {2:.2f}) \n"
                   "Окружность 2: ее радиус {3:.2f}, координаты центра ({4:.2f}, {5:.2f}) \n"
                   "Точка пересечения касательных {6:.2f}".format(cir1[1], cir1[0][0], cir1[0][1], cir2[1], cir2[0][0],
                                                           cir2[0][1], inter[0], inter[1]))


def redraw(event):
    global scale, cnv, overscale
    if scale < 20 and overscale == False:
        scale += 1
        cnv.delete('all')
        draw(event)
    else:
        if scale == 2:
            overscale = False
        else:
            overscale = True
        scale -= 1
        cnv.delete('all')
        draw(event)


def str_to_float(a):
    if a == '':
        return None
    a = a.split(' ')
    for i in range(len(a)):
        a[i] = a[i].split(',')
        for j in [0, 1]:
            a[i][j] = float(a[i][j])
    return a


def layout():
    cnv.create_line(10, 0, 10, 100 * scale, width=1, arrow=LAST)
    cnv.create_text(10, 110 * scale, text='Y', font="Times 12")
    cnv.create_line(0, 10, 100 * scale, 10, width=1, arrow=LAST)  # ось у
    cnv.create_text(110 * scale, 10, text='X', font="Times 12")


def distance_between_points(xy1, xy2):
    x_1 = xy1[0]
    x_2 = xy2[0]
    y_1 = xy1[1]
    y_2 = xy2[1]
    dis = math.sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2)
    return dis


def calc(a, b):
    min_squere = None
    circle1 = None
    circle2 = None
    inter_points = None
    line1 = None
    line2 = None
    for i in range(len(a) - 2):  # первая связка-точка
        for j in range(i + 1, len(a) - 1):  # вторая связка-точка
            for k in range(j + 1, len(a)):  # третья связка-точка
                res = find_cir(a[i], a[j], a[k])
                # print(a[i], a[j], a[k], centre_a, rad_a)
                if res is None:
                    continue
                else:
                    centre_a = res[0]
                    rad_a = res[1]

                for l in range(len(b) - 2):  # первая связка-точка
                    for m in range(l + 1, len(b) - 1):  # вторая связка-точка
                        for n in range(m + 1, len(b)):  # третья связка-точка
                            res = find_cir(b[l], b[m], b[n])
                            # print(b[i], b[j], b[k], centre_b, rad_b)
                            if res is None:
                                continue
                            else:
                                centre_b = res[0]
                                rad_b = res[1]

                            look_dis = distance_between_points(centre_b, centre_a)
                            if look_dis <= rad_a + rad_b:
                                continue

                            look_dis = distance_between_points(centre_b, b[i])

                            # находим все прямые проходящие через эти точки
                            line_il = get_line(a[i], b[l])
                            line_im = get_line(a[i], b[m])
                            line_in = get_line(a[i], b[n])

                            line_jl = get_line(a[j], b[l])
                            line_jm = get_line(a[j], b[m])
                            line_jn = get_line(a[j], b[n])

                            line_kl = get_line(a[k], b[l])
                            line_km = get_line(a[k], b[m])
                            line_kn = get_line(a[k], b[n])

                            lines = []

                            if line_il is not None: lines.append([line_il, a[i], b[l]])
                            if line_im is not None: lines.append([line_im, a[i], b[m]])
                            if line_in is not None: lines.append([line_in, a[i], b[n]])

                            if line_jl is not None: lines.append([line_jl, a[j], b[l]])
                            if line_jm is not None: lines.append([line_jm, a[j], b[m]])
                            if line_jn is not None: lines.append([line_jn, a[j], b[n]])

                            if line_kl is not None: lines.append([line_kl, a[k], b[l]])
                            if line_km is not None: lines.append([line_km, a[k], b[m]])
                            if line_kn is not None: lines.append([line_kn, a[k], b[n]])
                            # print(lines)

                            for line in lines:
                                if not is_tangent(centre_a[0], centre_a[0], rad_a, line[0][0], line[0][1]) and \
                                       not is_tangent(centre_b[0], centre_b[0], rad_b, line[0][0], line[0][1]):
                                    lines.remove(line)

                            if len(lines) < 2:
                                continue

                            #print(lines)
                            between = distance_between_points(centre_a, centre_b)
                            #print(between)
                            # находим все их  точки перерсечения
                            for s in range(len(lines) - 1):
                                for t in range(s + 1, len(lines)):
                                    points = intersection(lines[s][0][0], lines[s][0][1], lines[t][0][0], lines[t][0][1])
                                    if points is None:
                                        continue
                                    else:
                                        #print(points)
                                        d1 = distance_between_points(points, centre_a)
                                        d2 = distance_between_points(points, centre_b)
                                        #print(d1 + d2, between)
                                        if (d1 + d2) - between < 0.0001:
                                            squere1 = (d1 * distance_between_points(lines[s][1], lines[t][1])) / 2
                                            squere2 = (d2 * distance_between_points(lines[s][2], lines[t][2])) / 2
                                            if min_squere is None or abs(squere1 - squere2) < min_squere:
                                                min_squere = abs(squere1 - squere2)
                                                circle1 = [centre_a, rad_a]
                                                circle2 = [centre_b, rad_b]
                                                inter_points = points
                                                line1 = [lines[s][1], lines[s][2]]
                                                line2 = [lines[t][1], lines[t][2]]

    return circle1, circle2, inter_points, line1, line2


def find_cir(p1, p2, p3):  # поиск окружности по трем точкам
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    x3, y3 = p3[0], p3[1]
    if x1 == x2 == x3:  # три точки лежат на одной прямой
        return None
    if x2 == x1:  # случай, когда одна хорда вертикальная, ее коэф = int
        x2, x3 = x3, x2
        y2, y3 = y3, y2
    elif x2 == x3:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    ma = (y2 - y1) / (x2 - x1)  # наклонный коэф 1-ой хорды
    mb = (y3 - y2) / (x3 - x2)  # накл коэф 2-ой хорды
    if ma != mb:  # прямые совпадают
        x_centre = (ma * mb * (y1 - y3) + mb * (x1 + x2) - ma * (x2 + x3)) / (2 * (mb - ma))
        if ma == 0:
            y_centre = (-1 / mb) * (x_centre - (x2 + x3) / 2) + ((y2 + y3) / 2)
        else:
            y_centre = (-1 / ma) * (x_centre - (x1 + x2) / 2) + ((y1 + y2) / 2)
        radius = distance_between_points([x_centre, y_centre], [x1, y1])
        return [[x_centre, y_centre], radius]
    else:
        return None


def get_line(p1, p2):
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    try:
        k = (y1 - y2) / (x1 - x2)
    except ZeroDivisionError:
        return None
    b = y2 - k * x2
    return [k, b]


def is_tangent(x0, y0, rad, k, v):
    c = x0 ** 2 + v ** 2 - 2 * y0 * v + y0 ** 2 - rad ** 2
    a = k ** 2 + 1
    b = -2 * x0 - 2 * y0 * k + 2 * k * v
    D = b ** 2 - 4 * a * c
    if D != 0:
        return False
    else:
        return True


def intersection(k1, b1, k2, b2):
    try:
        x = (b2 - b1) / (k1 - k2)
    except ZeroDivisionError:
        return None
    y = k1 * x + b1
    return [x, y]


def k_comb(n, k):
    assert n > k, "Check values in k_comb!"
    return int(math.factorial(n) / (math.factorial(k) * math.factorial(n - k)))


def quit_win(event):
    global root, widgets
    root.destroy()
    widgets.destroy()


root = Tk()
root.title("Поле точек")
widgets = Tk()
widgets.title("Инструменты")
root.geometry('700x600')
widgets.wm_geometry("+%d+%d" % (100, 100))
root.wm_geometry("+%d+%d" % (500, 50))

scale = 9
overscale = False
but_scale = ttk.Button(widgets)
but_scale['text'] = "Масштабировать"
but_answ = ttk.Button(widgets)
but_answ["text"] = "Отобразить ответ"
but_exit = ttk.Button(widgets)
but_exit['text'] = 'Выход'

ent1 = Entry(widgets, width=50, bd=3)
ent2 = Entry(widgets, width=50, bd=3)
tx = Text(root, width=700, height=4, font='Times 12')
ent1.insert(0, '1.70,4.852 6.5,4.852 4,6 10,12.34 23.9,12')
ent2.insert(0, '2.7,9.453 23.5,14 5.3,9.453 4,9 23,34 3,4')
lab1 = Label(widgets, text="Первое можество точек:", font="Times 12", highlightcolor='red')
lab2 = Label(widgets, text="Второе можество точек:", font="Times 12", highlightcolor='green')

cnv = Canvas(root, height=600, width=700, bg='white')
but_answ.bind("<Button-1>", draw)
but_scale.bind('<Button-1>', redraw)
but_exit.bind('<Button-1>', quit_win)

lab1.pack()
ent1.pack()
ent1.focus_set()
lab2.pack()
tx.pack()
ent2.pack()
but_answ.pack()
but_scale.pack()
but_exit.pack()
cnv.pack()

"""lab1.grid(row=0, column=0)
lab2.grid(row=2, column=0)
ent1.grid(row=1, column=0)
ent2.grid(row=3, column=0)
but_answ.grid(row=4, column=0)
but_scale.grid(row=4, column=1)
cnv.grid(row=0, column=1)"""

root.mainloop()
widgets.mainloop()
