import sys

from vispy import scene
from vispy.visuals.transforms import STTransform
import numpy as np

omega = 'A'
rules = {'A':'B-F+CFC+F-D&F^D-F+&&CFC+F+B//',
         'B':'A&F^CFB^F^D^^-F-D^|F^B|FC^F^A//',
         'C':'|D^|F^B-F+C^F^A&&FA&F^C+F+B^F^D//',
         'D':'|CFB-F+B|FA&F^A&&FB-F+B|FC//'}
ngen = 2

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

canvas = scene.SceneCanvas(keys='interactive', bgcolor='white',
                           size=(800, 800), show=True)

view = canvas.central_widget.add_view()

elts = []
pos = np.array([0.0, 0.0, 0.0])
H = np.array([1.0, 0.0, 0.0])
L = np.array([0.0, 0.0, 1.0])
U = np.cross(H, L)
HLU = np.array((H, L, U)).T
d   = np.array([1.0, 0.0, 0.0])
alpha = np.pi*0.5

def RU(HLU, alpha):
    M = np.array((( np.cos(alpha), np.sin(alpha), 0.0),
                  (-np.sin(alpha), np.cos(alpha), 0.0),
                  (0.0, 0.0, 1.0)))
    return HLU.dot(M)

def RL(HLU, alpha):
    M = np.array(((np.cos(alpha), 0.0, -np.sin(alpha)),
                  (0.0, 1.0, 0.0),
                  (np.sin(alpha), 0.0, np.cos(alpha))))
    return HLU.dot(M)

def RH(HLU, alpha):
    M = np.array(((1.0, 0.0, 0.0),
                 (0.0, np.cos(alpha), -np.sin(alpha)),
                 (0.0, np.sin(alpha), np.cos(alpha))))

    return HLU.dot(M)

bary = np.array((0.0, 0.0, 0.0))
npts = 0

first = True
for c in s:
    if c == 'F':
        p1 = pos
        p2 = pos + HLU[:,0].T
        if first:
            color = 'red'
            first = False
        else:
            color = 'gray'
        t = scene.visuals.Tube((p1, p2), shading='smooth', tube_points=4, radius=0.1, color=color)
        view.add(t)
        pos = p2
        bary += 0.5 * (p1 + p2)
        npts += 1
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

bary /= npts
view.camera = scene.TurntableCamera()
view.camera.center = bary
        
if __name__ == '__main__' and sys.flags.interactive == 0:
    canvas.app.run()

