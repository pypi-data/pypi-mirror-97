from time import *
from turtle import *
import os
def stamp(something,speed,FT):
    for i in something:
        print(i,end='')
        sleep(speed)
    if FT == 1:
        print()
    sleep(0.5)
def turprint(some,size,place):
    pen = Turtle()
    pen.hideturtle()
    pen.penup()
    write(some,align=place,font=("微软雅黑", size,"normal"))
def clear():
    print("\033[2J""")
    print("\033[99999A")
def clean():
    os.system("clear")
def steap(something1,speed1):
    clear()
    stamp(something1,speed1)
def plaympf(mpf):
    os.system(mpf)
