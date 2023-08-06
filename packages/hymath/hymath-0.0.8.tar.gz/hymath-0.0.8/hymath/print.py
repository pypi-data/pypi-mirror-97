from time import*
from sys import*

def clean(a):
    sleep(a)
    stdout.write('\033[2J\033[00H')
def clear():
    stdout.write('\033[2J\033[00H')
# def pr(*a):
#     for i in a:
#         print(i,end="")
# pr("e"+"1")
def fun(x,*a):
    for j in a:
        for i in j:
            print(i,end="")
            sleep(x)
    print("")
def h_logo(x,a):
    for i in range(len(a)):
        if a[i] == "0":
            print("\033[0m ",end="")
            sleep(x)
        elif a[i] == "1":
            print("\033[41m ",end="")
            sleep(x)
        elif a[i] == "2":
            print("\033[42m ",end="")
            sleep(x)
        elif a[i] == "3":
            print("\033[43m ",end="")
            sleep(x)
        elif a[i] == "4":
            print("\033[44m ",end="")
            sleep(x)
        elif a[i] == "5":
            print("\033[45m ",end="")
            sleep(x)
        elif a[i] == "6":
            print("\033[46m ",end="")
            sleep(x)
        elif a[i] == "7":
            print("\033[47m ",end="")
            sleep(x)
        elif a[i] == "d":
            print("\033[30m",end="")
            sleep(x)
        elif a[i] == "r":
            print("\033[31m",end="")
            sleep(x)
        elif a[i] == "g":
            print("\033[32m",end="")
            sleep(x)
        elif a[i] == "y":
            print("\033[33m",end="")
            sleep(x)
        elif a[i] == "b":
            print("\033[34m",end="")
            sleep(x)
        elif a[i] == "p":
            print("\033[35m",end="")
            sleep(x)
        elif a[i] == "c":
            print("\033[36m",end="")
            sleep(x)
        elif a[i] == "w":
            print("\033[37m",end="")
            sleep(x)
        else:
            print(a[i],end="")
            sleep(x)
    print("\033[0m",end="")
def logo(a):
    for i in range(len(a)):
        if a[i] == "0":
            print("\033[0m ",end="")
        elif a[i] == "1":
            print("\033[41m ",end="")
        elif a[i] == "2":
            print("\033[42m ",end="")
        elif a[i] == "3":
            print("\033[43m ",end="")
        elif a[i] == "4":
            print("\033[44m ",end="")
        elif a[i] == "5":
            print("\033[45m ",end="")
        elif a[i] == "6":
            print("\033[46m ",end="")
        elif a[i] == "7":
            print("\033[47m ",end="")
        elif a[i] == "d":
            print("\033[30m",end="")
        elif a[i] == "r":
            print("\033[31m",end="")
        elif a[i] == "g":
            print("\033[32m",end="")
        elif a[i] == "y":
            print("\033[33m",end="")
        elif a[i] == "b":
            print("\033[34m",end="")
        elif a[i] == "p":
            print("\033[35m",end="")
        elif a[i] == "c":
            print("\033[36m",end="")
        elif a[i] == "w":
            print("\033[37m",end="")
        else:
            print(a[i],end="")
    print("\033[0m")