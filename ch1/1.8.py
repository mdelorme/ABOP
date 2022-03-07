import sys

from vispy import scene
import numpy as np
import string
import random

import imageio

from helpers import *

class Rule:
  def __init__(self, s):
    f1, f2 = s.split('->')
    f1 = f1.replace(' ', '')
    f2 = f2.replace(' ', '')
    self.v = f2
    self.left, t12 = f1.split('<')
    self.k, self.right = t12.split('>')

    if self.left == '*':
      self.left = None
    if self.right == '*':
      self.right = None

  def validate(self, left_context, predecessor, right_context):
    if predecessor != self.k:
      return False
    if self.left and left_context != self.left:
      return False
    if self.right and right_context != self.right:
      return False
    return True

class System:
  def __init__(self, omega, rules, ignore):
    self.omega  = omega
    self.rules  = rules
    self.ignore = ignore

  def extract_context(self, s, pos):
    left_context  = None
    predecessor   = ''
    right_context = None

    predecessor = s[pos]
    left_str  = s[:pos][::-1]
    right_str = s[pos+1:]

    for c in self.ignore:
      left_str = left_str.replace(c, '')
      right_str = right_str.replace(c, '')

    valid_tokens = string.ascii_lowercase + string.ascii_uppercase + string.digits
    nopen = 0
    for c in right_str:
      if c == '[':
        nopen += 1
      elif c == ']':
        if nopen == 0:
          break
        else:
          nopen -= 1
      elif c in valid_tokens and nopen == 0:
        right_context = c
        break

    for c in left_str:
      if c == ']':
        nopen += 1
      elif c == '[':
        if nopen > 0:
          nopen -= 1
      elif c in valid_tokens and nopen == 0:
        left_context = c
        break

    return left_context, predecessor, right_context

  def evolve(self, s):
    L = len(s)
    ns = ''
    for i in range(L):
      left_c, pred, right_c = self.extract_context(s, i)

      for r in self.rules:
        if r.validate(left_c, pred, right_c):
          ns += r.v
          break
      else:
        ns += s[i]
    return ns

case_id = int(sys.argv[-1]) if len(sys.argv) > 1 else 0

if case_id == 0:
  omega = 'F1F1F1'
  ignore = '+-F'
  rules = [Rule('0 < 0 > 0 -> 0'),
           Rule('0 < 0 > 1 -> 1[+F1F1]'),
           Rule('0 < 1 > 0 -> 1'),
           Rule('0 < 1 > 1 -> 1'),
           Rule('1 < 0 > 0 -> 0'),
           Rule('1 < 0 > 1 -> 1F1'),
           Rule('1 < 1 > 0 -> 0'),
           Rule('1 < 1 > 1 -> 0'),
           Rule('* < + > * -> -'),
           Rule('* < - > * -> +')]
  system = System(omega, rules, ignore)
  delta = 22.5 * np.pi / 180.0
  ngen  = 30
elif case_id == 1:
  omega = 'F1F1F1'
  ignore = '+-F'
  rules = [Rule('0 < 0 > 0 -> 1'),
           Rule('0 < 0 > 1 -> 1[-F1F1]'),
           Rule('0 < 1 > 0 -> 1'),
           Rule('0 < 1 > 1 -> 1'),
           Rule('1 < 0 > 0 -> 0'),
           Rule('1 < 0 > 1 -> 1F1'),
           Rule('1 < 1 > 0 -> 1'),
           Rule('1 < 1 > 1 -> 0'),
           Rule('* < + > * -> -'),
           Rule('* < - > * -> +')]
  system = System(omega, rules, ignore)
  delta = 22.5 * np.pi / 180.0
  ngen  = 30
elif case_id == 2:
  omega = 'F1F1F1'
  ignore = '+-F'
  rules = [Rule('0 < 0 > 0 -> 0'),
           Rule('0 < 0 > 1 -> 1'),
           Rule('0 < 1 > 0 -> 0'),
           Rule('0 < 1 > 1 -> 1[+F1F1]'),
           Rule('1 < 0 > 0 -> 0'),
           Rule('1 < 0 > 1 -> 1F1'),
           Rule('1 < 1 > 0 -> 0'),
           Rule('1 < 1 > 1 -> 0'),
           Rule('* < - > * -> +'),
           Rule('* < + > * -> -')]
  system = System(omega, rules, ignore)
  delta = 25.75 * np.pi / 180.0
  ngen = 26
elif case_id == 3:
  omega  = 'F0F1F1'
  ignore = '+-F'
  rules = [Rule('0 < 0 > 0 -> 1'),
           Rule('0 < 0 > 1 -> 0'),
           Rule('0 < 1 > 0 -> 0'),
           Rule('0 < 1 > 1 -> 1F1'),
           Rule('1 < 0 > 0 -> 1'),
           Rule('1 < 0 > 1 -> 1[+F1F1]'),
           Rule('1 < 1 > 0 -> 1'),
           Rule('1 < 1 > 1 -> 0'),
           Rule('* < - > * -> +'),
           Rule('* < + > * -> -')]
  system = System(omega, rules, ignore)
  delta = 25.75 * np.pi / 180.0
  ngen = 24
elif case_id == 4:
  omega  = 'F1F1F1'
  ignore = '+-F'
  rules = [Rule('0 < 0 > 0 -> 0'),
           Rule('0 < 0 > 1 -> 1[-F1F1]'),
           Rule('0 < 1 > 0 -> 1'),
           Rule('0 < 1 > 1 -> 1'),
           Rule('1 < 0 > 0 -> 0'),
           Rule('1 < 0 > 1 -> 1F1'),
           Rule('1 < 1 > 0 -> 1'),
           Rule('1 < 1 > 1 -> 0'),
           Rule('* < - > * -> +'),
           Rule('* < + > * -> -')]
  system = System(omega, rules, ignore)
  delta = 22.5 * np.pi / 180.0
  ngen = 26

canvas = scene.SceneCanvas(keys='interactive',
                           bgcolor='white',
                           size=(800, 800),
                           show=True)
view = canvas.central_widget.add_view()

lines = []

s     = system.omega
d     = np.array((0.0, 1.0))
pos   = np.array((0.0, 0.0))
pts   = [pos]
stack = []

for gen in range(ngen):
  s = system.evolve(s)

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

writer = imageio.get_writer('img_1.8_{}.png'.format(case_id))
im = canvas.render()
writer.append_data(im)
writer.close()


if __name__ == '__main__' and sys.flags.interactive == 0:
    canvas.app.run()

