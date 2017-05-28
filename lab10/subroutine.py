def sign(x):
    if not x:
        return 0
    else:
        return x / abs(x)


def side_rib(x, y, xrib, yrib, top, bottom):
    """Если xrib = -1, то встреченапервая кривая и
    ребро не создается"""
    if xrib == -1:
        xrib = x
        yrib = y
    else:
        top, bottom = horizon(xrib, yrib, x, y, top, bottom)
        xrib = x
        yrib = y
    return xrib, yrib, top, bottom


def is_visiable(x, y, top, bottom):
    """Видимость точки определяется по отношению к
    верхнему и нижнему плавающему горизонтам.
    Если точка лежит на самом горизонте, то она считается видимой.
    0 - unvisiable
    1 - if visiable and over
    -1 - visiable and under"""
    if top[x] > y > bottom[x]:
        return 0
    if y >= top[x]:
        return 1
    if y <= bottom[x]:
        return -1


def horizon(x1, y1, x2, y2, top, bottom):
    """Используется линейная интерполяция
    для заполнения массивов горизонтов между  x1 и x2"""
    # проверка вертикальности наклона
    if abs(x2 - x1) == 0:
        top[x2] = max(top[x2], y2)
        bottom[x2] = min(bottom[x2], y2)
    else:
        t = (y2 - y1) / (x2 - x1)
        for x in range(x1, x2 + 1):
            y = t * (x - x1) + y1
            top[x] = max(top[x], y)
            bottom[x] = min(bottom[x], y)

    return top, bottom


def intersection(x1, y1, x2, y2, hor):
    # проверка бесконечности наклона
    if x2 - x1 == 0:
        xi = x2
        yi = hor[x2]
    else:
        # вычисление пересечения
        """обход начинается с самой левой используемой точки 
        пересечение считается обнаруженным,
        когда изменяется знак разности значений у"""
        t = (y2 - y1) / (x2 - x1)
        ysign = sign(y1 + t - hor[x1 + 1])
        csign = ysign
        yi = y1 + t
        xi = x1 + 1

        while csign == ysign:
            yi += t
            xi += 1
            csign = sign(yi - hor[xi])

        # выбирается ближайшее целое число
        if abs(yi - t - hor[xi - 1]) <= abs(yi - hor[xi]):
            yi -= t
            xi -= 1

    return xi, yi


if __name__ == "__main__":
    pass
