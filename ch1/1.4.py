from turtle import *
import sys

set_id=int(sys.argv[-1]) if len(sys.argv) > 1 else 0

x0=-200
y0=600

post = None

remove_RL={'R':'', 'L':''}
    
if set_id == 0: # Fig 1.10 a
    omega = 'A'
    rules = {'A':'A+B+',
             'B':'-A-B'}
    d=10
    delta=90
    ngen=10
elif set_id == 1: # Fig 1.10 b
    omega = 'B'
    rules = {'A':'B+A+B',
             'B':'A-B-A'}
    delta=60
    ngen=6
    d=10
    y0=200
elif set_id == 2: # Fig 1.11 a
    omega='A'
    rules = {'A':'A+B++B-A--AA-B+',
             'B':'-A+BB++B+A--A-B'}
    delta=60
    ngen=4
    d=10
    y0=200
elif set_id == 3: # Fig 1.11 b
    omega='-B'
    rules = {'A':'AA-B-B+A+A-B-BA+B+AAB-A+B+AA+B-AB-B-A+A+BB-',
             'B':'+AA-B-B+A+AB+A-BB-A-B+ABB-A-BA+A+B-B-A+A+BB'}
    delta=90
    ngen=2
    d=20
elif set_id == 4: # Fig 1.15
    omega='L'
    rules={'L':'+RF-LFL-FR+',
           'R':'-LF+RFR+FL-'}
    post=remove_RL
    delta=90
    ngen=5
    d=20
    y0=200
elif set_id == 5: # Fig 1.16 a
    omega='-L'
    rules={'L':'LF+RFR+FL-F-LFLFL-FRFR+',
           'R':'-LFLF+RFRFR+F+RF-LFL-FR'}
    post=remove_RL
    delta=90
    ngen=3
    d=20
elif set_id == 6: # Fig 1.16 b
    omega='-L'
    rules={'L':'LFLF+RFR+FLFL-FRF-LFL-FR+F+RF-LFL-FRFRFR+',
           'R':'-LFLFLF+RFR+FL-F-LF+RFR+FLF+RFRF-LFL-FRFR'}
    post=remove_RL
    delta=90
    ngen=3
    d=10
elif set_id == 7: # Fig 1.17 a
    omega='L'
    rules={'L':'LFRFL-F-RFLFR+F+LFRFL',
           'R':'RFLFR+F+LFRFL-F-RFLFR'}
    post=remove_RL
    delta=90
    ngen=3
    d=20
elif set_id == 8: # Fig 1.17 b
    omega='L'
    # Warning : There's a mistake in the original description of the L rule !
    rules={'L':'L+F+R-F-L+F+R-F-L-F-R+F+L-F-R-F-L+F+R-F-L-F-R-F-L+F+R+F+L+F+R-F-L+F+R+F+L-F-R+F+L+F+R-F-L+F+R-F-L', 
           'R':'R-F-L+F+R-F-L+F+R+F+L-F-R+F+L+F+R-F-L+F+R+F+L+F+R-F-L-F-R-F-L+F+R-F-L-F-R+F+L-F-R-F-L+F+R-F-L+F+R'}
    post=remove_RL
    delta=45
    ngen=2
    d=20

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
        if c.isupper():
            fd(d)
        elif c.islower():
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

def post_process(s):
    if post == None:
        return s
    
    ns = ''
    for c in s:
        if c in post:
            ns += post[c]
        else:
            ns += c
    return ns
    
s = omega
for i in range(ngen):
    s = evolve(s)
s = post_process(s)
draw_set(s)


