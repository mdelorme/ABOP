import sys

from helpers import *

from vispy import scene
from vispy.visuals.transforms import STTransform
import numpy as np

import imageio

omega = 'A'
rules = {'A':'B-F+CFC+F-D&F^D-F+&&CFC+F+B//',
         'B':'A&F^CFB^F^D^^-F-D^|F^B|FC^F^A//',
         'C':'|D^|F^B-F+C^F^A&&FA&F^C+F+B^F^D//',
         'D':'|CFB-F+B|FA&F^A&&FB-F+B|FC//'}
ngen = 3

def evolve(s):
    ns = ''
    for c in s:
        if c in rules:
            ns += rules[c]
        else:
            ns += c
    return ns

s = omega
for gen in range(ngen):
    s = evolve(s)

HLU=init_HLU()

canvas = scene.SceneCanvas(keys='interactive', bgcolor='white',
                           size=(800, 800), show=True)

view = canvas.central_widget.add_view()

pos = np.array([0.0, 0.0, 0.0])

d   = np.array([1.0, 0.0, 0.0])
alpha = np.pi*0.5


pts  = [pos]
bary = np.array((0.0, 0.0, 0.0))
npts = 0

first = True
for c in s:
    if c == 'F':
        new_pos = pos + HLU[:,0].T
        pts.append(new_pos)
        pos = new_pos
    elif c == '+':
        HLU = RU(HLU, alpha)
    elif c == '-':
        HLU = RU(HLU, -alpha)
    elif c == '&':
        HLU = RL(HLU, alpha)
    elif c == '^':
        HLU = RL(HLU, -alpha)
    elif c == '\\':
        HLU = RH(HLU, alpha)
    elif c == '/':
        HLU = RH(HLU, -alpha)
    elif c == '|':
        HLU = RU(HLU, 2.0*alpha)

        
pts = np.array(pts)
tube = scene.visuals.Tube(pts, radius=0.1, tube_points=8, shading='smooth', color='gray')
bary = sum(pts)
bary /= pts.shape[0]

view.add(tube)
view.camera = scene.TurntableCamera()
view.camera.center = bary


writer = imageio.get_writer('img_1.5.png')
im = canvas.render()
writer.append_data(im)
writer.close()
        
if __name__ == '__main__' and sys.flags.interactive == 0:
    canvas.app.run()

