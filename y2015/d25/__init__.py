def task1():
    v = 20151125
    x, y = 0, 0
    while (x, y) != (3018, 3009):
        v = (v * 252533) % 33554393
        x += 1
        y -= 1
        if y < 0:
            y = x
            x = 0
            print(y)
    print(v)
