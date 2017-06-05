from subroutine import horizon
import numpy as np
from math import pi, sin, cos

M = 48
shx = 600 / 2 + 50
shy = 710 / 2 - 50


def rotateX(x, y, z, teta):
    teta = teta * pi / 180
    buf = y
    y = cos(teta) * y - sin(teta) * z
    z = cos(teta) * z + sin(teta) * buf
    return x, y, z


def rotateY(x, y, z, teta):
    teta = teta * pi / 180
    buf = x
    x = cos(teta) * x - sin(teta) * z
    z = cos(teta) * z + sin(teta) * buf
    return x, y, z


def rotateZ(x, y, z, teta):
    teta = teta * pi / 180
    buf = x
    x = cos(teta) * x - sin(teta) * y
    y = cos(teta) * y + sin(teta) * buf
    return x, y, z


def tranform(x, y, z, tetax, tetay, tetaz):
    x, y, z = rotateX(x, y, z, tetax)
    x, y, z = rotateY(x, y, z, tetay)
    x, y, z = rotateZ(x, y, z, tetaz)
    x = x * M + shx
    y = y * M + shy
    return round(x), round(y), round(z)


def float_horizon(scene_width, scene_hight, x_min, x_max, x_step, z_min, z_max, z_step,
                  tx, ty, tz, func, image):
    # инициализация переменных
    x_right = -1
    y_right = -1
    x_left = -1
    y_left = -1

    # инициализация массивов горизонтов
    top = {x: 0 for x in range(1, int(scene_width) + 1)}
    bottom = {x: scene_hight for x in range(1, int(scene_width) + 1)}

    z = z_max
    while z >= z_min:
        z_buf = z
        x_prev = x_min
        y_prev = func(x_min, z)
        x_prev, y_prev, z_buf = tranform(x_prev, y_prev, z, tx, ty, tz)

        # Обрабатываем левое ребро(смотрим предыдущее с текущим)
        if x_left != -1:
            top, bottom = horizon(x_prev, y_prev, x_left, y_left, top, bottom, image)
        x_left = x_prev
        y_left = y_prev

        x = x_min
        while x <= x_max:
            y = func(x, z)
            x_curr = x
            y_curr = y
            x_curr, y_curr, z_buf = tranform(x_curr, y_curr, z, tx, ty, tz)

            # Добавление в горизонт и  отрисовка линий
            top, bottom = horizon(x_prev, y_prev, x_curr, y_curr, top, bottom, image)
            x_prev = x_curr
            y_prev = y_curr

            x += x_step

        # Обрабатываем правое ребро(смотрим текущее со следующим)
        if z != z_max:
            x_right = x_max
            y_right = func(x_max, z - z_step)
            x_right, y_right, z_buf = tranform(x_right, y_right, z-z_step, tx, ty, tz)
            top, bottom = horizon(x_prev, y_prev, x_right, y_right, top, bottom, image)

        z -= z_step

    return image

