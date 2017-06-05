from PyQt5.QtCore import Qt

def sign(x):
    if not x:
        return 0
    else:
        return x / abs(x)


def horizon(x1, y1, x2, y2, top, bottom, image):
    # на самом деле это брезенхем
    x = x1
    y = y1
    dx = x2 - x1
    dy = y2 - y1
    sx = sign(dx)
    sy = sign(dy)
    dx = abs(dx)
    dy = abs(dy)

    # если точка
    if dx == 0 and dy == 0 and 0 <= x < image.width():
        if y >= top[x]:
            top[x] = y
            image.setPixel(round(x), round(image.height() - y), Qt.black)

        if y <= bottom[x]:
            bottom[x] = y
            image.setPixel(round(x), round(image.height() - y), Qt.black)

        return top, bottom

    #  Нужно ли менять местами х и у
    change = 0
    if dy > dx:
        dx, dy = dy, dx
        change = 1

    y_max_curr = top[x]
    y_min_curr = bottom[x]
    e = 2 * dy - dx

    i = 1
    while i <= dx:
        if 0 <= x < image.width():

            if y >= top[x]:
                if y >= y_max_curr:
                    y_max_curr = y
                image.setPixel(round(x), round(image.height() - y), Qt.black)

            if y <= bottom[x]:
                if y <= y_min_curr:
                    y_min_curr = y
                image.setPixel(round(x), round(image.height() - y), Qt.black)

        if e >= 0:
            if change:
                top[x] = y_max_curr
                bottom[x] = y_min_curr

                x += sx

                y_max_curr = top[x]
                y_min_curr = bottom[x]

            else:
                y += sy

            e -= 2 * dx
        else:
            if not change:
                top[x] = y_max_curr
                bottom[x] = y_min_curr

                x += sx

                y_max_curr = top[x]
                y_min_curr = bottom[x]

            else:
                y += sy

            e += 2 * dy

        i += 1
    return top, bottom


if __name__ == "__main__":
    pass
