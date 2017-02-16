from tkinter import *
from tkinter import ttk
import math


def draw(event):
    a = ent1.get()
    b = ent2.get()
    a = str_to_int(a)
    b = str_to_int(b)

    if a is None or b is None:
        cnv.create_text(100, 10, text='Введите точки!', font="Times 12")
        return
    cnv.delete('all')
    layout()
    for i in range(len(a)):
        cnv.create_oval(a[i][0] * scale + 10, a[i][1] * scale + 10, (a[i][0] + 1) * scale + 10,
                        (a[i][1] + 1) * scale + 10, fill="green")
    for i in range(len(b)):
        cnv.create_oval(b[i][0] * scale + 10, b[i][1] * scale + 10, (b[i][0] + 1) * scale + 10,
                        (b[i][1] + 1) * scale + 10, fill="red")
    print(calc(a, b))


def redraw(event):
    global scale, cnv, overscale
    if scale < 5 and overscale == False:
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


def str_to_int(a):
    if a == '':
        return None
    a = a.split(' ')  # а вдруг пустая строка
    for i in range(len(a)):
        a[i] = a[i].split(',')
        for j in [0, 1]:
            a[i][j] = int(a[i][j])
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
    p1 = None
    p2 = None
    q1 = None
    q2 = None
    for i in range(len(a) - 2):  # первая связка-точка
        for j in range(i + 1, len(a) - 1):  # вторая связка-точка
            for k in range(j + 1, len(a)):  # третья связка-точка
                centre_a, rad_a = find_cir(a[i], a[j], a[k])
                print(a[i], a[j], a[k], centre_a, rad_a)
                # TODO сделать провенрку на возврат нан

                for l in range(len(b) - 2):  # первая связка-точка
                    for m in range(l + 1, len(b) - 1):  # вторая связка-точка
                        for n in range(m + 1, len(b)):  # третья связка-точка
                            centre_b, rad_b = find_cir(b[l], b[m], b[n])

                            # находим все прямые проходящие через эти точки
                            line_il = get_line(a[i], b[l])
                            line_im = get_line(a[i], b[m])
                            line_in = get_line(a[i], b[n])

                            if line_il is None or line_im is None or line_in is None:
                                continue

                            line_jl = get_line(a[j], b[l])
                            line_jm = get_line(a[j], b[m])
                            line_jn = get_line(a[j], b[n])

                            if line_jl is None or line_jm is None or line_jn is None:
                                continue

                            line_kl = get_line(a[k], b[l])
                            line_km = get_line(a[k], b[m])
                            line_kn = get_line(a[k], b[n])

                            if line_kl is None or line_km is None or line_kn is None:
                                continue

                            il = False
                            im = False
                            inn = False

                            jl = False
                            jm = False
                            jn = False

                            kl = False
                            km = False
                            kn = False

                            # проверяем, являются ли прямые касателньными
                            if is_tangent(centre_a[0], centre_a[0], rad_a, line_il[0], line_il[1]) and \
                                    is_tangent(centre_b[0], centre_b[0], rad_b, line_il[0], line_il[1]):
                                il = True
                            if is_tangent(centre_a[0], centre_a[0], rad_a, line_im[0], line_im[1]) and \
                                    is_tangent(centre_b[0], centre_b[0], rad_b, line_im[0], line_im[1]):
                                im = True
                            if is_tangent(centre_a[0], centre_a[0], rad_a, line_in[0], line_in[1]) and \
                                    is_tangent(centre_b[0], centre_b[0], rad_b, line_in[0], line_in[1]):
                                inn = True

                            if is_tangent(centre_a[0], centre_a[0], rad_a, line_jl[0], line_jl[1]) and \
                                    is_tangent(centre_b[0], centre_b[0], rad_b, line_jl[0], line_jl[1]):
                                jl = True
                            if is_tangent(centre_a[0], centre_a[0], rad_a, line_jm[0], line_jm[1]) and \
                                    is_tangent(centre_b[0], centre_b[0], rad_b, line_jm[0], line_jm[1]):
                                jm = True
                            if is_tangent(centre_a[0], centre_a[0], rad_a, line_jn[0], line_jn[1]) and \
                                    is_tangent(centre_b[0], centre_b[0], rad_b, line_jn[0], line_jn[1]):
                                jn = True

                            if is_tangent(centre_a[0], centre_a[0], rad_a, line_kl[0], line_kl[1]) and \
                                    is_tangent(centre_b[0], centre_b[0], rad_b, line_kl[0], line_kl[1]):
                                kl = True
                            if is_tangent(centre_a[0], centre_a[0], rad_a, line_km[0], line_km[1]) and \
                                    is_tangent(centre_b[0], centre_b[0], rad_b, line_km[0], line_km[1]):
                                km = True
                            if is_tangent(centre_a[0], centre_a[0], rad_a, line_kn[0], line_kn[1]) and \
                                    is_tangent(centre_b[0], centre_b[0], rad_b, line_kn[0], line_kn[1]):
                                kn = True

                            tan = []  # массив касательных

                            if il: tan.append([line_il, a[i], b[l]])
                            if im: tan.append([line_im, a[i], b[m]])
                            if inn: tan.append([line_in, a[i], b[n]])

                            if jl: tan.append([line_jl, a[j], b[l]])
                            if jm: tan.append([line_jm, a[j], b[m]])
                            if jn: tan.append([line_jn, a[j], b[n]])

                            if kl: tan.append([line_kl, a[k], b[l]])
                            if km: tan.append([line_km, a[k], b[m]])
                            if kn: tan.append([line_kn, a[k], b[n]])

                            if len(tan) < 2:
                                continue

                            between = distance_between_points(centre_a, centre_b)
                            # находим все их  точки перерсечения
                            for s in range(len(tan) - 1):
                                for t in range(s + 1, len(tan)):
                                    points = intersection(tan[s][0][0], tan[s][0][1], tan[t][0][0], tan[t][0][1])
                                    if points is None:
                                        continue
                                    else:
                                        d1 = distance_between_points(points, centre_a)
                                        d2 = distance_between_points(points, centre_b)
                                        if d1 + d2 == between:
                                            squere1 = (d1 * distance_between_points(tan[s][1], tan[t][1])) / 2
                                            squere2 = (d2 * distance_between_points(tan[s][2], tan[t][2])) / 2
                                            if min_squere is None or abs(squere1 - squere2) < min_squere:
                                                min_squere = abs(squere1 - squere2)
    return min_squere


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
        return [x_centre, y_centre], radius
    else:
        return None


def get_line(p1, p2):
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p1[1]
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


root = Tk()
root.title("Поле точек")
widgets = Tk()
widgets.title("Инструменты")
root.geometry('700x600')
widgets.wm_geometry("+%d+%d" % (100, 100))
root.wm_geometry("+%d+%d" % (500, 50))

scale = 3
overscale = False
but_scale = ttk.Button(widgets)
but_scale['text'] = "Масштабировать"
but_answ = ttk.Button(widgets)
but_answ["text"] = "Отобразить ответ"
text1 = StringVar()
text1.set('3,9 2,12 9,9')
text2 = StringVar()
text2.set("4,4 9,2 8,4")
ent1 = Entry(widgets, width=50, bd=3, textvariable=text1)
ent2 = Entry(widgets, width=50, bd=3, textvariable=text2)

lab1 = Label(widgets, text="Первое можество точек:", font="Times 12", highlightcolor='red')
lab2 = Label(widgets, text="Второе можество точек:", font="Times 12", highlightcolor='green')

cnv = Canvas(root, height=600, width=700, bg='white')
but_answ.bind("<Button-1>", draw)
but_scale.bind('<Button-1>', redraw)

lab1.pack()
ent1.pack()
lab2.pack()
ent2.pack()
but_answ.pack()
but_scale.pack()
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
