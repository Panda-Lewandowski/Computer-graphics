from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
import math


def draw(event):
    global f_lst, r_lst, scale, dx, dy, redraw_scale, redraw_d

    a = []
    b = []
    aa = f_lst.get(0, END)
    for x in aa:
        a.append(list(x))
    bb = r_lst.get(0, END)
    for x in bb:
        b.append(list(x))

    if a is None or b is None:
        showerror('Ошибка', 'Введите точки в формате х,у')
        return
    cnv.delete('all')

    cir1, cir2, inter, l1, l2, sq = calc(a, b)
    if cir1 is None:
        showwarning('Упс', "Окружностей не найдено!")
    else:
        if (inter[0] < 0 or inter[1] < 0) and redraw_d is False:
            dx = 300
            dy = 200
            redraw_d = True
        if distance_between_points(cir1[0], cir2[0]) <= 10 and redraw_scale is False:
            scale = 20
            redraw_scale = True

        cnv.create_oval((cir1[0][0] - cir1[1]) * scale + dx, (cir1[0][1] + cir1[1]) * scale + dy,
                        (cir1[0][0] + cir1[1]) * scale + dx, (cir1[0][1] - cir1[1]) * scale + dy, fill='#FFF0F5')

        cnv.create_oval((cir2[0][0] - cir2[1]) * scale + dx, (cir2[0][1] + cir2[1]) * scale + dy,
                        (cir2[0][0] + cir2[1]) * scale + dx, (cir2[0][1] - cir2[1]) * scale + dy, fill='#E6E6FA')

        cnv.create_oval((cir1[0][0]) * scale + dx - 1.5, (cir1[0][1]) * scale + dy - 1.5,
                        (cir1[0][0]) * scale + dx + 1.5,
                        (cir1[0][1]) * scale + dy + 1.5, fil='#DB7093')

        cnv.create_oval((cir2[0][0]) * scale + dx - 1.5, (cir2[0][1]) * scale + dy - 1.5,
                        (cir2[0][0]) * scale + dx + 1.5,
                        (cir2[0][1]) * scale + dy + 1.5, fil='#9370DB')

        cnv.create_oval((inter[0]) * scale + dx - 1.5, (inter[1]) * scale + dy - 1.5, (inter[0]) * scale + dx + 1.5,
                        (inter[1]) * scale + dy + 1.5, fill="black")
        cnv.create_line(l1[0][0] * scale + dx, l1[0][1] * scale + dy, l1[1][0] * scale + dx, l1[1][1] * scale + dy,
                        width=1, fill="black")
        cnv.create_line(l2[0][0] * scale + dx, l2[0][1] * scale + dy, l2[1][0] * scale + dx, l2[1][1] * scale + dy,
                        width=1, fill="black")

        cnv.create_line(cir1[0][0] * scale + dx, cir1[0][1] * scale + dy, l1[0][0] * scale + dx, l1[0][1] * scale + dy,
                        width=1, fill="black")
        cnv.create_line(cir2[0][0] * scale + dx, cir2[0][1] * scale + dy, l2[0][0] * scale + dx, l2[0][1] * scale + dy,
                        width=1, fill="black")
        cnv.create_line(cir1[0][0] * scale + dx, cir1[0][1] * scale + dy, l2[1][0] * scale + dx, l2[1][1] * scale + dy,
                        width=1, fill="black")
        cnv.create_line(cir2[0][0] * scale + dx, cir2[0][1] * scale + dy, l1[1][0] * scale + dx, l1[1][1] * scale + dy,
                        width=1, fill="black")
    layout()
    for i in range(len(a)):
        cnv.create_oval(a[i][0] * scale + dx - 1.5, (a[i][1]) * scale + dy - 1.5, a[i][0] * scale + dx + 1.5,
                        (a[i][1]) * scale + dy + 1.5, fill="green")
    for i in range(len(b)):
        cnv.create_oval((b[i][0]) * scale + dx - 1.5, (b[i][1]) * scale + dy - 1.5, (b[i][0]) * scale + dx + 1.5,
                        (b[i][1]) * scale + dy + 1.5, fill="red")

    tx.delete('1.0', END)
    tx.insert(1.0, "Окружности найдены. Минимальная площадь: {0:.3f} \n "
                   "Окружность 1: ее радиус {1:.2f}, координаты центра ({2:.2f}, {3:.2f}) \n"
                   "Окружность 2: ее радиус {4:.2f}, координаты центра ({5:.2f}, {6:.2f}) \n"
                   "Точка пересечения касательных {7:.2f}".format(sq, cir1[1], cir1[0][0], cir1[0][1], cir2[1],
                                                                  cir2[0][0],
                                                                  cir2[0][1], inter[0], inter[1]))


def layout():
    cnv.create_line(dx, dy, dx, 10 * scale + dy, width=1, arrow=LAST)
    cnv.create_text(dx, 10 * scale + dy, text='Y', font="Times 12")
    cnv.create_line(dx, dy, 10 * scale + dx, dy, width=1, arrow=LAST)  # ось у
    cnv.create_text(10 * scale + dx, dy, text='X', font="Times 12")


def redraw_max(event):
    global scale, cnv
    scale += 1
    cnv.delete('all')
    draw(event)


def redraw_min(event):
    global scale, cnv
    scale -= 1
    cnv.delete('all')
    draw(event)


def to_right(event):
    global dx, cnv
    dx += 10
    cnv.delete('all')
    draw(event)


def to_left(event):
    global dx, cnv
    dx -= 10
    cnv.delete('all')
    draw(event)


def to_top(event):
    global dy, cnv
    dy -= 10
    cnv.delete('all')
    draw(event)


def to_bottom(event):
    global dy, cnv
    dy += 10
    cnv.delete('all')
    draw(event)


def str_to_float(a):
    if a == '':
        return None
    a = a.split(' ')
    for i in range(len(a)):
        try:
            a[i] = float(a[i])
        except ValueError:
            showwarning('Упс', "Уберите лишние пробелы или добавьте еще одну координату!")
            return None
    return a


def distance_between_points(xy1, xy2):
    x_1 = xy1[0]
    x_2 = xy2[0]
    y_1 = xy1[1]
    y_2 = xy2[1]
    dis = math.sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2)
    return dis


def calc(a, b):
    global scale
    min_squere = None
    circle1 = None
    circle2 = None
    line1 = None
    line2 = None
    inter_points = None
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

                            k = rad_a / rad_b  # коэфициент подобия

                            xm = (centre_a[0] + centre_b[0] * k) / (1 + k)  # точка пересечения касательных
                            ym = (centre_a[1] + centre_b[1] * k) / (1 + k)

                            r = math.sqrt(distance_between_points([xm, ym], centre_a) ** 2 - rad_a ** 2)

                            d = math.sqrt(math.pow(abs(centre_a[0] - xm), 2) + math.pow(abs(centre_a[1] - ym),
                                                                                        2))  # расстояние между центрами окружностей
                            if d >= r + rad_a:
                                continue

                            aa = (r ** 2 - rad_a ** 2 + d ** 2) / (
                                2 * d)  # расстояние от r до точки пересечения линии, соединяющей точки пересечения
                            h = math.sqrt(math.pow(r, 2) - math.pow(aa,
                                                                    2))  # //расстояние от точки пересеч окружностей до линииб соед т пересеч

                            x0 = xm + aa * (centre_a[0] - xm) / d  # точка пересеч линии соединения и линии центров
                            y0 = ym + aa * (centre_a[1] - ym) / d

                            up_a = [x0 + h * (centre_a[1] - ym) / d,
                                    y0 - h * (centre_a[0] - xm) / d]
                            down_a = [x0 - h * (centre_a[1] - ym) / d,
                                      y0 + h * (centre_a[0] - xm) / d]
                            # print(up_a, '\n', down_a, '\n')

                            # _________________________________________________________________

                            r = math.sqrt(distance_between_points([xm, ym], centre_b) ** 2 - rad_b ** 2)

                            d = math.sqrt(math.pow(abs(centre_b[0] - xm), 2) + math.pow(abs(centre_b[1] - ym),
                                                                                        2))  # расстояние между центрами окружностей
                            if d >= r + rad_b:
                                continue

                            aa = (r ** 2 - rad_b ** 2 + d ** 2) / (
                                2 * d)  # расстояние от r до точки пересечения линии, соединяющей точки пересечения
                            h = math.sqrt(math.pow(r, 2) - math.pow(aa,
                                                                    2))  # //расстояние от точки пересеч окружностей до линииб соед т пересеч

                            x0 = xm + aa * (centre_b[0] - xm) / d  # точка пересеч линии соединения и линии центров
                            y0 = ym + aa * (centre_b[1] - ym) / d

                            up_b = [x0 + h * (centre_b[1] - ym) / d,
                                    y0 - h * (centre_b[0] - xm) / d]
                            down_b = [x0 - h * (centre_b[1] - ym) / d,
                                      y0 + h * (centre_b[0] - xm) / d]
                            # print(up_b, '\n', down_b, '\n')


                            d1 = distance_between_points(up_a, down_a)
                            d2 = distance_between_points([xm, ym], centre_a)
                            squere1 = (d1 * d2) / 2
                            d1 = distance_between_points(up_b, down_b)
                            d2 = distance_between_points([xm, ym], centre_b)
                            squere2 = (d1 * d2) / 2
                            if min_squere is None or abs(squere1 - squere2) < min_squere:
                                min_squere = abs(squere1 - squere2)
                                circle1 = [centre_a, rad_a]
                                circle2 = [centre_b, rad_b]
                                line1 = [up_a, up_b]
                                line2 = [down_b, down_a]
                                inter_points = [xm, ym]

    return circle1, circle2, inter_points, line1, line2, min_squere


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


def quit_win(event):
    root.destroy()
    navigation.destroy()
    r.destroy()


def insert_lst_f(event):
    global f_lst, ent_f
    p = ent_f.get()
    p = str_to_float(p)
    if p is None:
        return
    if len(p) > 2 or len(p) < 2:
        showwarning('Упс', "У точки должно быть всего две координаты!")
        return
    f_lst.insert(END, p)
    ent_f.delete(0, END)


def insert_lst_s(event):
    global r_lst, ent_s
    p = ent_s.get()
    p = str_to_float(p)
    if p is None:
        return
    if len(p) > 2 or len(p) < 2:
        showwarning('Упс', "У точки должно быть всего две координаты!")
        return
    r_lst.insert(END, p)
    ent_s.delete(0, END)


def del_point_red(event):
    global f_lst
    f_lst.delete(ACTIVE)


def del_point_green(event):
    global r_lst
    r_lst.delete(ACTIVE)


def ch_point_red(event):
    global f_lst
    p = ent_f.get()
    p = str_to_float(p)
    if p is None:
        return
    if len(p) > 2 or len(p) < 2:
        showwarning('Упс', "У точки должно быть всего две координаты!")
        return
    f_lst.delete(ACTIVE)
    f_lst.insert(END, p)
    ent_f.delete(0, END)


def ch_point_green(event):
    global r_lst
    p = ent_s.get()
    p = str_to_float(p)
    if p is None:
        return
    if len(p) > 2 or len(p) < 2:
        showwarning('Упс', "У точки должно быть всего две координаты!")
        return
    r_lst.delete(ACTIVE)
    r_lst.insert(END, p)
    ent_s.delete(0, END)


root = Tk()
root.title("Поле точек")
r = Tk()
r.title("Инструменты")
navigation = Tk()
navigation.title("Навигация")
root.geometry('700x600')
r.wm_geometry("+%d+%d" % (10, 10))
root.wm_geometry("+%d+%d" % (650, 10))
navigation.wm_geometry("+%d+%d" % (150, 400))

scale = 9
dx = 10
dy = 10
redraw_scale = False
redraw_d = False
scale_p = ttk.Button(navigation)
scale_p['text'] = "Увеличить"
scale_m = ttk.Button(navigation)
scale_m['text'] = 'Уменьшить'
right = ttk.Button(navigation)
right['text'] = '〉'
left = ttk.Button(navigation)
left['text'] = '〈'
bottom = ttk.Button(navigation)
bottom['text'] = '﹀'
top = ttk.Button(navigation)
top['text'] = '︿'

scrollbar1 = Scrollbar(r)
scrollbar2 = Scrollbar(r)
f_lst = Listbox(r, selectmode=SINGLE, height=10, yscrollcommand=scrollbar1.set)
r_lst = Listbox(r, selectmode=SINGLE, height=10, yscrollcommand=scrollbar2.set)
scrollbar1.config(command=f_lst.yview)
scrollbar2.config(command=r_lst.yview)
lab_f = Label(r, text="Красное можество точек", font="Times 12")
lab_s = Label(r, text="Зеленое можество точек", font="Times 12")
xy_f = Label(r, text='Введите красную точку  ', font="Times 12")
xy_s = Label(r, text='Введите зеленую точку  ', font="Times 12")
ent_f = Entry(r, width=50, bd=3)
ent_s = Entry(r, width=50, bd=3)

but_del_r = ttk.Button(r)
but_del_r['text'] = 'Удалить красную точку'
but_del_g = ttk.Button(r)
but_del_g['text'] = 'Удалить зеленую точку'
but_ch_r = ttk.Button(r)
but_ch_r['text'] = 'Изменить красную точку'
but_ch_g = ttk.Button(r)
but_ch_g['text'] = 'Изменить зеленую точку'
but_answ = ttk.Button(r)
but_answ["text"] = "Отобразить ответ"
but_exit = ttk.Button(r)
but_exit['text'] = 'Выход'

ent_f.bind('<Return>', insert_lst_f)
ent_s.bind('<Return>', insert_lst_s)
but_del_r.bind('<Button-1>', del_point_red)
but_del_g.bind('<Button-1>', del_point_green)
but_ch_r.bind('<Button-1>', ch_point_red)
but_ch_g.bind('<Button-1>', ch_point_green)

cnv = Canvas(root, height=600, width=700, bg='white')
tx = Text(root, width=700, height=4, font='Times 12')

but_answ.bind("<Button-1>", draw)
scale_p.bind('<Button-1>', redraw_max)
scale_m.bind('<Button-1>', redraw_min)
right.bind('<Button-1>', to_right)
left.bind('<Button-1>', to_left)
top.bind('<Button-1>', to_top)
bottom.bind('<Button-1>', to_bottom)
but_exit.bind('<Button-1>', quit_win)

"""var=IntVar()
var.set(1)
rad0 = Radiobutton(r,text="Первая",
          variable=var,value=0)
rad1 = Radiobutton(r,text="Вторая",
          variable=var,value=1)"""

f_lst.grid(row=1, column=0, padx=10)
r_lst.grid(row=1, column=1, padx=10)
lab_f.grid(row=0, column=0, padx=5)
lab_s.grid(row=0, column=1, padx=5)
xy_f.grid(row=2, column=0, pady=5)
ent_f.grid(row=2, column=1, pady=5)
xy_s.grid(row=3, column=0, pady=5)
ent_s.grid(row=3, column=1, pady=5)

but_del_r.grid(row=4, column=0, padx=2, pady=5)
but_del_g.grid(row=5, column=0, padx=2, pady=5)
but_answ.grid(row=4, column=2, padx=2, pady=5)
but_exit.grid(row=5, column=2, padx=2, pady=5)
but_ch_r.grid(row=4, column=1, padx=2, pady=5)
but_ch_g.grid(row=5, column=1, padx=2, pady=5)

tx.pack()
cnv.pack()

scale_p.grid(row=0, column=0, padx=20)
scale_m.grid(row=1, column=0, padx=20, pady=5)
right.grid(row=0, column=1, padx=20)
left.grid(row=1, column=1, padx=20, pady=5)
top.grid(row=0, column=2, padx=20)
bottom.grid(row=1, column=2, padx=20, pady=5)

r.mainloop()
root.mainloop()
navigation.mainloop()
