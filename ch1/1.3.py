from helpers import *

from vispy import scene
from vispy.visuals.transforms import STTransform
import numpy as np

import sys

import imageio

case_id=int(sys.argv[-1]) if len(sys.argv) > 1 else 0
    
if case_id == 0: # Fig 1.6 d
    omega = 'F-F-F-F'
    rules = {'F':'F-F+F+FF-F-F+F'}
    d=3
    delta=90
    ngen=3
elif case_id == 1: # Fig 1.7 a
    omega = 'F-F-F-F'
    rules = {'F':'F+FF-FF-F-F+F+FF-F-F+F+FF+FF-F'}
    d=5
    delta=90
    ngen=2
elif case_id == 2: # Fig 1.7 b
    omega='-F'
    rules = {'F':'F+F-F-F+F'}
    d=4
    delta=90
    ngen=4
elif case_id == 3: # Fig 1.8
    omega='F+F+F+F'
    rules= {'F':'F+f-FF+F+FF+Ff+FF-f+FF-F-FF-Ff-FFF',
            'f':'ffffff'}
    d=3
    delta=90
    ngen=2
elif case_id == 4: # Fig 1.9 a
    omega='F-F-F-F'
    rules = {'F':'FF-F-F-F-F-F+F'}
    d=4
    delta=90
    x0=-200
    y0=600
    ngen=4
elif case_id == 5: # Fig 1.9 b
    omega='F-F-F-F'
    rules={'F':'FF-F-F-F-FF'}
    d=4
    delta=90
    ngen=4
elif case_id == 6: # Fig 1.9 c
    omega='F-F-F-F'
    rules={'F':'FF-F+F-F-FF'}
    d=10
    delta=90
    ngen=3
elif case_id == 7: # Fig 1.9 d
    omega='F-F-F-F'
    rules={'F':'FF-F--F-F'}
    d=5
    delta=90
    ngen=4
elif case_id == 8: # Fig 1.9 e
    omega='F-F-F-F'
    rules={'F':'F-FF--F-F'}
    d=5
    delta=90
    ngen=5
elif case_id == 9: # Fig 1.9 f
    omega='F-F-F-F'
    rules={'F':'F-F+F-F-F'}
    d=10
    delta=90
    ngen=4
else:
    print('Error ! Case id is unknown. It should be an integer in [0, 9]')
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
    if c == 'F':
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

writer = imageio.get_writer('img_1.3_{}.png'.format(case_id))
im = canvas.render()
writer.append_data(im)
writer.close()


if __name__ == '__main__' and sys.flags.interactive == 0:
    canvas.app.run()

