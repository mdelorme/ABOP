from helpers import *
import numpy as np
from vispy import scene
import sys
import imageio

def evolve(s, rules, table):
  tokens = tokenize(s)
  tokens = build_expressions(tokens)
  new_expr = ''
  for t in tokens:
    for r in rules:
      valid, expr = is_parametric_expression_valid(t, r, table)
      if valid:
        new_expr += expr
        break
    else:
      new_expr += t
  return new_expr

scale = 1.0

case_id = 0 if len(sys.argv) < 2 else int(sys.argv[-1])
if case_id == 0:
  omega = 'B(2)A(4,4)'
  p1 = parse_parametric_expression('A(x,y) : y <= 3 -> A(x*2,x+y)')
  p2 = parse_parametric_expression('A(x,y) : y > 3  -> B(x)A(x/y,0)')
  p3 = parse_parametric_expression('B(x) : x < 1 -> C')
  p4 = parse_parametric_expression('B(x) : x >= 1 -> B(x-1)')
  rules = [p1, p2, p3, p4]
  table = {}
  ngen = 4
elif case_id == 1:
  omega = 'F(1)'
  p1 = parse_parametric_expression('F(x) : True -> F(x*p) + F(x*h) - - F(x*h)+F(x*q)')
  rules = [p1]
  c = 1
  p = 0.3
  q = c-p
  h = (p*q)**0.5
  table = {'c':str(c), 'p':str(p), 'q':str(q), 'h':str(h)}
  ngen = 6
  scale = 10.0
  delta = 86.0 * np.pi / 180.0
elif case_id == 2:
  omega = 'F(1,0)'
  p1 = parse_parametric_expression('F(x, t) : t == 0 -> F(x*p, 2) + F(x*h, 1)--F(x*h,1) + F(x*q,0)')
  p2 = parse_parametric_expression('F(x, t) : t > 0 -> F(x, t-1)')
  rules = [p1, p2]
  c = 1
  p = 0.3
  q = c-p
  h = (p*q)**0.5
  table = {'c':str(c), 'p':str(p), 'q':str(q), 'h':str(h)}
  ngen = 10
  scale = 10.0
  delta = 86.0 * np.pi / 180.0
elif case_id == 3:
  omega = 'A(1)'
  p1 = parse_parametric_expression('A(s):True -> F(s)[+A(s/R)][-A(s/R)]')
  rules = [p1]
  R = 1.456
  table = {'R':str(R)}
  delta = 85.0 * np.pi / 180.0
  ngen = 12
  


s = omega
if case_id == 0:
  print(s)
for i in range(ngen):
  s = evolve(s, rules, table)
  if case_id == 0:
    print(s)


if case_id > 0:


  canvas = scene.SceneCanvas(keys='interactive',
                           bgcolor='white',
                           size=(800, 800),
                           show=True)
  view = canvas.central_widget.add_view()

  lines = []

  pos = np.array((0.0, 0.0))
  d   = np.array((1.0, 0.0))
  pts = []
  stack = []

  tokens = tokenize(s)

  for t in tokens:
    if t[0] == 'F':
      if t[1][0]:
        L = float(t[1][0])
      new_pos = pos + d*L
      pts.append(new_pos)
      lines.append(pos)
      lines.append(new_pos)
      pos = new_pos
    elif t[0] == '+':
      if t[1][0]:
        delta = float(t[1][0])
      d = R2d(d, delta)
    elif t[0] == '-':
      if t[1][0]:
        delta = float(t[1][0])
      d = R2d(d, -delta)
    elif t[0] == '[':
      stack.append((pos, d))
    elif t[0] == ']':
      pos, d = stack.pop()

lines = np.array(lines) * scale

xmin = lines[:,0].min()
xmax = lines[:,0].max()
ymin = lines[:,1].min()
ymax = lines[:,1].max()

bary = (0.5*(xmin+xmax), 0.5*(ymin+ymax))

Lx = xmax-xmin
Ly = ymax-ymin
Hlx = Lx / 2
Hly = Ly / 2

Hl = Hlx if Lx > Ly else Hly
r = (bary[0]-Hl, bary[1]-Hl, 2.0*Hl, 2.0*Hl)
l = scene.visuals.Line(lines, color='black', connect='segments', width=2)

view.add(l)
view.camera = scene.PanZoomCamera(rect=r, aspect=1.0)

writer = imageio.get_writer('img_1.10_{}.png'.format(case_id))
im = canvas.render()
writer.append_data(im)
writer.close()


if __name__ == '__main__' and sys.flags.interactive == 0:
    canvas.app.run()

