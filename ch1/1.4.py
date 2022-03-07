from helpers import *

from vispy import scene
from vispy.visuals.transforms import STTransform
import numpy as np

import sys

import imageio

case_id=int(sys.argv[-1]) if len(sys.argv) > 1 else 0

post = None

remove_RL={'R':'', 'L':''}
    
if case_id == 0: # Fig 1.10 a
    omega = 'A'
    rules = {'A':'A+B+',
             'B':'-A-B'}
    d=10
    delta=90
    ngen=10
elif case_id == 1: # Fig 1.10 b
    omega = 'B'
    rules = {'A':'B+A+B',
             'B':'A-B-A'}
    delta=60
    ngen=6
    d=10
elif case_id == 2: # Fig 1.11 a
    omega='A'
    rules = {'A':'A+B++B-A--AA-B+',
             'B':'-A+BB++B+A--A-B'}
    delta=60
    ngen=4
    d=10
elif case_id == 3: # Fig 1.11 b
    omega='-B'
    rules = {'A':'AA-B-B+A+A-B-BA+B+AAB-A+B+AA+B-AB-B-A+A+BB-',
             'B':'+AA-B-B+A+AB+A-BB-A-B+ABB-A-BA+A+B-B-A+A+BB'}
    delta=90
    ngen=2
    d=20
elif case_id == 4: # Fig 1.15
    omega='L'
    rules={'L':'+RF-LFL-FR+',
           'R':'-LF+RFR+FL-'}
    post=remove_RL
    delta=90
    ngen=5
    d=20
elif case_id == 5: # Fig 1.16 a
    omega='-L'
    rules={'L':'LF+RFR+FL-F-LFLFL-FRFR+',
           'R':'-LFLF+RFRFR+F+RF-LFL-FR'}
    post=remove_RL
    delta=90
    ngen=3
    d=20
elif case_id == 6: # Fig 1.16 b
    omega='-L'
    rules={'L':'LFLF+RFR+FLFL-FRF-LFL-FR+F+RF-LFL-FRFRFR+',
           'R':'-LFLFLF+RFR+FL-F-LF+RFR+FLF+RFRF-LFL-FRFR'}
    post=remove_RL
    delta=90
    ngen=3
    d=10
elif case_id == 7: # Fig 1.17 a
    omega='L'
    rules={'L':'LFRFL-F-RFLFR+F+LFRFL',
           'R':'RFLFR+F+LFRFL-F-RFLFR'}
    post=remove_RL
    delta=90
    ngen=3
    d=20
elif case_id == 8: # Fig 1.17 b
    omega='L'
    # Warning : There's a mistake in the original description of the L rule !
    rules={'L':'L+F+R-F-L+F+R-F-L-F-R+F+L-F-R-F-L+F+R-F-L-F-R-F-L+F+R+F+L+F+R-F-L+F+R+F+L-F-R+F+L+F+R-F-L+F+R-F-L', 
           'R':'R-F-L+F+R-F-L+F+R+F+L-F-R+F+L+F+R-F-L+F+R+F+L+F+R-F-L-F-R-F-L+F+R-F-L-F-R+F+L-F-R-F-L+F+R-F-L+F+R'}
    post=remove_RL
    delta=45
    ngen=2
    d=20
else:
    print('Error ! Case id should be an integer in [0, 8]')
    exit(0)

delta = delta * np.pi / 180.0
    

canvas = scene.SceneCanvas(keys='interactive',
                           bgcolor='white',
                           size=(800, 800),
                           show=True)
view = canvas.central_widget.add_view()

lines = []

s     = omega
d     = np.array((0.0, 1.0))
pos   = np.array((0.0, 0.0))
pts   = [pos]
stack = []

for gen in range(ngen):
  ns = ''
  for c in s:
    if c in rules:
        ns += rules[c]
    else:
      ns += c
  s = ns

for c in s:
    if c in 'FAB':
        pts.append(pos+d)
        lines.append(pos)
        lines.append(pos+d)
        pos = pos + d
    elif c == '+':
        d = R2d(d, delta)
    elif c == '-':
        d = R2d(d, -delta)
    elif c == '[':
        stack.append((pos, d))
    elif c == ']':
        pos, d = stack.pop()

lines = np.array(lines)
xmin = lines[:,0].min()
xmax = lines[:,0].max()
ymin = lines[:,1].min()
ymax = lines[:,1].max()

bary = (0.5*(xmin+xmax), 0.5*(ymin+ymax))

Lx = xmax-xmin
Ly = ymax-ymin
Hlx = Lx // 2 * 1.1
Hly = Ly // 2 * 1.1

Hl = Hlx if Lx > Ly else Hly
r = (bary[0]-Hl, bary[1]-Hl, 2.0*Hl, 2.0*Hl)
l = scene.visuals.Line(lines, color='black', connect='segments', width=2)
view.add(l)
view.camera = scene.PanZoomCamera(rect=r, aspect=1.0)

writer = imageio.get_writer('img_1.4_{}.png'.format(case_id))
im = canvas.render()
writer.append_data(im)
writer.close()


if __name__ == '__main__' and sys.flags.interactive == 0:
    canvas.app.run()

