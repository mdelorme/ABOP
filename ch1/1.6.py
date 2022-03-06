import sys

from helpers import *

from vispy import scene
import numpy as np

import imageio

case_id = int(sys.argv[-1]) if len(sys.argv) > 1 else 0

cases = [('F', {'F':'F[+F]F[-F]F'},   5, 25.7),
         ('F', {'F':'F[+F]F[-F][F]'}, 5, 20.0),
         ('F', {'F':'FF-[-F+F+F]+[+F-F-F]'}, 4, 22.5),
         ('X', {'X':'F[+X]F[-X]+X', 'F':'FF'}, 7, 20.0),
         ('X', {'X':'F[+X][-X]FX', 'F':'FF'}, 7, 25.7),
         ('X', {'X':'F-[[X]+X]+F[+FX]-X', 'F':'FF'}, 5, 22.5)
]

omega, rules, ngen, delta = cases[case_id]
delta = np.pi / 180.0 * delta
    
s     = omega
d     = np.array((0.0, 1.0))
pos   = np.array((0.0, 1.0))
pts   = [pos]
lines = []
stack = []

for gen in range(ngen):
    ns = ''
    for c in s:
        if c in rules:
            ns += rules[c]
        else:
            ns += c
    s = ns

canvas = scene.SceneCanvas(keys='interactive',
                           bgcolor='white',
                           size=(800, 800),
                           show=True)
view = canvas.central_widget.add_view()

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
r = (bary[0]-Hl, bary[1]-Hl, bary[0]+Hl, bary[1]+Hl)
l = scene.visuals.Line(lines, color='black', connect='segments', width=2)
view.add(l)
view.camera = scene.PanZoomCamera(rect=r, aspect=1.0)
view.camera.center = tuple(bary)

writer = imageio.get_writer('img_1.6_{}.png'.format(case_id))
im = canvas.render()
writer.append_data(im)
writer.close()


if __name__ == '__main__' and sys.flags.interactive == 0:
    canvas.app.run()


    
