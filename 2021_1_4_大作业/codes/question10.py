"""
项目：日本国旗
白底红色圆
长宽比：3：2
圆形直径为旗面宽度的3/5

颜色：
白色：255,255,255
红色：188, 0, 45
"""
import turtle as t

# 设置旗面大小
ch = 900
k = 2 / 3 * ch
t.screensize(canvwidth=ch, canvheight=k, bg=None)
t.speed(6)
t.colormode(255)
f_r = 188, 0, 45
f_w = 255, 255, 255

# 原型直径
l = 3 / 5 * k

t.pencolor(f_r)

# 画旗面
t.penup()
t.goto(-ch / 2, k / 2)
t.pendown()
t.pencolor(f_r)
for i in range(2):
    t.fd(ch)
    t.right(90)
    t.fd(k)
    t.right(90)

t.penup()
t.home()
t.fd(l/2)
t.right(90)
t.fillcolor(f_r)
t.pendown()
t.begin_fill()
t.circle(-l/2)
t.end_fill()

t.hideturtle()
t.done()
