from subroutine import side_rib, is_visiable, horizon, intersection
import numpy as np
from math import sin

def f(x, z):
    return sin(2 * x * z)


def float_horizon(scene_width, scene_hight, x_min, x_max, x_step, z_min, z_max, z_step, func, scene):
    # инициализация переменных
    x_right = -1
    y_right = -1
    x_left = -1
    y_left = -1

    # инициализация массивов горизонтов
    top = {x : 0 for x in range(1, int(scene_width)+1)}
    bottom = {x : scene_hight for x in range(1, int(scene_width)+1)}

    # вычисление функции на каждой плоскости z = const
    # начиная с ближайшей к наблюдателю плоскости Zmax
    for z in range(z_max, z_min, - z_step):
        # инициализация предыдущих значений по х и у
        x_prev = x_min
        y_prev = func(x_min, z)
        """если используется видовое преобразование(поворот???),
        то его нужно применить к х_prev и y_prev в данной точке"""
        # обработка левого бокового ребра
        x_left, y_left, top, bottom = side_rib(x_prev, y_prev, x_left, y_left, top, bottom)
        prev_flag = is_visiable(x_prev, y_prev, top, bottom)

        # для каждой точки на кривой, лежащей в плоскости z = const
        for x in range(x_min, x_max, x_step):
            y = func(x, z)
            """если используется видовое преобразование, 
            то его нужно применить к данной точке"""
            # проверка видимости текущей точки и заполнение соответствующего массива горизонта
            cur_flag = is_visiable(x, y, top, bottom)
            if prev_flag == cur_flag:
                if cur_flag == -1 or cur_flag == 1:
                    scene.addLine(x_prev, y_prev, x, y)
                    top, bottom = horizon(x_prev, y_prev, x, y, top, bottom)
            else:
                # если видимость изменилась, то вычисляется пересечение
                # и заполняется массив горизонта
                if cur_flag == 0:
                    if prev_flag == 1:
                        xi, yi = intersection(x_prev, y_prev, x, y, top)
                    else:
                        xi, yi = intersection(x_prev, y_prev, x, y, bottom)

                    scene.addLine(x_prev, y_prev, xi, yi)
                    top, bottom = horizon(x_prev, y_prev, xi, yi, top, bottom)
                else:
                    if cur_flag == 1:
                        if prev_flag == 0:
                            xi, yi = intersection(x_prev, y_prev, x, y, top)
                            scene.addLine(xi, yi, x, y)
                            top, bottom = horizon(xi, yi, x, y, top, bottom)
                        else:
                            xi, yi = intersection(x_prev, y_prev, x, y, bottom)
                            scene.addLine(x_prev, y_prev, xi, yi)
                            top, bottom = horizon(x_prev, y_prev, xi, yi, top, bottom)
                            xi, yi = intersection(x_prev, y_prev, x, y, top)
                            scene.addLine(xi, yi, x, y)
                            top, bottom = horizon(xi, yi, x, y, top, bottom)
                    else:
                        if prev_flag == 0:
                            xi, yi = intersection(x_prev, y_prev, x, y, top)
                            scene.addLine(xi, yi, x, y)
                            top, bottom = horizon(xi, yi, x, y, top, bottom)
                        else:
                            xi, yi = intersection(x_prev, y_prev, x, y, top)
                            scene.addLine(x_prev, y_prev, xi, yi)
                            top, bottom = horizon(x_prev, y_prev, xi, yi, top, bottom)
                            xi, yi = intersection(x_prev, y_prev, x, y, bottom)
                            scene.addLine(xi, yi, x, y)
                            top, bottom = horizon(xi, yi, x, y, top, bottom)

            prev_flag = cur_flag
            x_prev = x
            y_prev = y

        x_right, y_right, top, bottom = side_rib(x, y, x_right, y_right, top, bottom)



