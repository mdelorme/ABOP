import sys

from helpers import *

from vispy import scene
import numpy as np
import random

import imageio

seed = int(sys.argv[-1]) if len(sys.argv) > 1 else 0

cases = [('F', {'F':[(0.33, 'F[+F]F[-F]F'),
                     (0.66, 'F[+F]F'),
                     (1.0,  'F[-F]F')]}, 
                     5, 25.7)]

omega, rules, ngen, delta = cases[0]
delta = np.pi / 180.0 * delta

canvas = scene.SceneCanvas(keys='interactive',
                           bgcolor='white',
                           size=(800, 800),
                           show=True)
view = canvas.central_widget.add_view()

lines = []
random.seed(seed)

s     = omega
d     = np.array((0.0, 1.0))
pos   = np.array((0.0, 0.0))
pts   = [pos]
stack = []

for gen in range(ngen):
  ns = ''
  for c in s:
    if c in rules:
      rg = random.random()
      rule = rules[c]
      for r in rule:
        if r[0] > rg:
          ns += r[1]
          break 
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
Hlx = Lx // 2
Hly = Ly // 2

Hl = Hlx if Lx > Ly else Hly
r = (bary[0]-Hl, bary[1]-Hl, 2.0*Hl, 2.0*Hl)
l = scene.visuals.Line(lines, color='black', connect='segments', width=2)
view.add(l)
view.camera = scene.PanZoomCamera(rect=r, aspect=1.0)

writer = imageio.get_writer('img_1.7_{}.png'.format(seed))
im = canvas.render()
writer.append_data(im)
writer.close()


if __name__ == '__main__' and sys.flags.interactive == 0:
    canvas.app.run()


    
