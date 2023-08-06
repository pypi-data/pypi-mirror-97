def factor(x):
    j = []
    try:
        if x<=0:
            print("\033[1;91mError!!!")
            exit()

    except:
        print("\033[1;91mError!!!")
        exit()
    for i in range(x+1):
        if i >= 1:
            if x % i == 0:
                j.append(i)
    return j
def big(a, b):
    try:
        if a == 0 or b == 0:
            print("\033[1;91mError!!!")
            exit()

    except:
        print("\033[1;91mError!!!")
        exit()
    c = a % b
    while c != 0:
        a = b
        b = c
        c = a % b
    return b
def small(a, b):
    try:
        if a == 0 or b == 0:
            print("\033[1;91mError!!!")
            exit()
    except:
        print("\033[1;91mError!!!")
        exit()
    e = a
    f = b
    c = a % b
    while c != 0:
        a = b
        b = c
        c = a % b
    d = e*f/b
    return d
def cut_factor(a):
    b = 2
    c = []
    e=[]
    try:
        a = int(a)
    except:
        print("Error!!!")
        exit()
    while b <= a:
        if a % b == 0:
            a /= b
            c.append(b)
        else:
            b += 1
    for i in range(len(c) - 1):
        e.append(c[i])
    e.append(c[-1])
    return e