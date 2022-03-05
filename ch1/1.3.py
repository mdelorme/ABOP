from turtle import *
import sys

set_id=int(sys.argv[-1]) if len(sys.argv) > 1 else 0

x0=-200
y0=600
    
if set_id == 0: # Fig 1.6 d
    omega = 'F-F-F-F'
    rules = {'F':'F-F+F+FF-F-F+F'}
    d=3
    delta=90
    ngen=3
elif set_id == 1: # Fig 1.7 a
    omega = 'F-F-F-F'
    rules = {'F':'F+FF-FF-F-F+F+FF-F-F+F+FF+FF-F'}
    d=5
    delta=90
    ngen=2
elif set_id == 2: # Fig 1.7 b
    omega='-F'
    rules = {'F':'F+F-F-F+F'}
    d=4
    delta=90
    ngen=4
elif set_id == 3: # Fig 1.8
    omega='F+F+F+F'
    rules= {'F':'F+f-FF+F+FF+Ff+FF-f+FF-F-FF-Ff-FFF',
            'f':'ffffff'}
    d=3
    delta=90
    ngen=2
elif set_id == 4: # Fig 1.9 a
    omega='F-F-F-F'
    rules = {'F':'FF-F-F-F-F-F+F'}
    d=4
    delta=90
    x0=-200
    y0=600
    ngen=4
elif set_id == 5: # Fig 1.9 b
    omega='F-F-F-F'
    rules={'F':'FF-F-F-F-FF'}
    d=4
    delta=90
    ngen=4
elif set_id == 6: # Fig 1.9 c
    omega='F-F-F-F'
    rules={'F':'FF-F+F-F-FF'}
    d=10
    delta=90
    ngen=3
elif set_id == 7: # Fig 1.9 d
    omega='F-F-F-F'
    rules={'F':'FF-F--F-F'}
    d=5
    delta=90
    ngen=4
elif set_id == 8: # Fig 1.9 e
    omega='F-F-F-F'
    rules={'F':'F-FF--F-F'}
    d=5
    delta=90
    ngen=5
elif set_id == 9: # Fig 1.9 f
    omega='F-F-F-F'
    rules={'F':'F-F+F-F-F'}
    d=10
    delta=90
    ngen=4
    
pu()
setpos(x0, y0)
speed(0)
pd()


W, H = 1024, 1024
hideturtle()
tracer(10, 1)

def draw_set(s):
    color('black', 'gray')
    ts = getscreen()
    ts.screensize(W, H)
    begin_fill()
    for c in s:
        if c == 'F':
            fd(d)
        elif c == 'f':
            pu()
            fd(d)
            pd()
        elif c == '-':
            right(delta)
        elif c == '+':
            left(delta)
    done()

def evolve(s):
    ns = ''
    for c in s:
        if c in rules:
            ns += rules[c]
        else:
            ns += c
    return ns

s = omega
for i in range(ngen):
    s = evolve(s)
draw_set(s)


