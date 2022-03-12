from helpers import *
import helpers
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
helpers.debug = False

case_id = 0 if len(sys.argv) < 2 else int(sys.argv[-1])
if case_id == 0:
  omega = 'A(10,1)'
  p1 = parse_parametric_expression('A(l,w) : True -> !(w)F(l)[&(a0)B(l*r2,w*wr)]/(d)A(l*r1,w*wr)')
  p2 = parse_parametric_expression('B(l,w) : True -> !(w)F(l)[-(a2)$C(l*r2,w*wr)]C(l*r1,w*wr)')
  p3 = parse_parametric_expression('C(l,w) : True -> !(w)F(l)[+(a2)$B(l*r2,w*wr)]B(l*r1,w*wr)')
  rules = [p1, p2, p3]
  r1 = 0.9
  r2 = 0.6
  a0 = 45.0*np.pi/180.0
  a2 = 45.0*np.pi/180.0
  d  = 137.5*np.pi/180.0
  wr = 0.707
  table = {'r1':str(r1),
           'r2':str(r2),
           'a0':str(a0),
           'a2':str(a2),
           'd':str(d),
           'wr':str(wr)}
  ngen = 10
elif case_id == 1:
  omega = 'A(10,1)'
  p1 = parse_parametric_expression('A(l,w) : True -> !(w)F(l)[&(a0)B(l*r2,w*wr)]/(d)A(l*r1,w*wr)')
  p2 = parse_parametric_expression('B(l,w) : True -> !(w)F(l)[-(a2)$C(l*r2,w*wr)]C(l*r1,w*wr)')
  p3 = parse_parametric_expression('C(l,w) : True -> !(w)F(l)[+(a2)$B(l*r2,w*wr)]B(l*r1,w*wr)')
  rules = [p1, p2, p3]
  r1 = 0.9
  r2 = 0.9
  a0 = 45.0*np.pi/180.0
  a2 = 45.0*np.pi/180.0
  d  = 137.5*np.pi/180.0
  wr = 0.707
  table = {'r1':str(r1),
           'r2':str(r2),
           'a0':str(a0),
           'a2':str(a2),
           'd':str(d),
           'wr':str(wr)}
  ngen = 10 
elif case_id == 2:
  omega = 'A(10,1)'
  p1 = parse_parametric_expression('A(l,w) : True -> !(w)F(l)[&(a0)B(l*r2,w*wr)]/(d)A(l*r1,w*wr)')
  p2 = parse_parametric_expression('B(l,w) : True -> !(w)F(l)[-(a2)$C(l*r2,w*wr)]C(l*r1,w*wr)')
  p3 = parse_parametric_expression('C(l,w) : True -> !(w)F(l)[+(a2)$B(l*r2,w*wr)]B(l*r1,w*wr)')
  rules = [p1, p2, p3]
  r1 = 0.9
  r2 = 0.8
  a0 = 45.0*np.pi/180.0
  a2 = 45.0*np.pi/180.0
  d  = 137.5*np.pi/180.0
  wr = 0.707
  table = {'r1':str(r1),
           'r2':str(r2),
           'a0':str(a0),
           'a2':str(a2),
           'd':str(d),
           'wr':str(wr)}
  ngen = 10 
elif case_id == 3:
  omega = 'A(10,1)'
  p1 = parse_parametric_expression('A(l,w) : True -> !(w)F(l)[&(a0)B(l*r2,w*wr)]/(d)A(l*r1,w*wr)')
  p2 = parse_parametric_expression('B(l,w) : True -> !(w)F(l)[-(a2)$C(l*r2,w*wr)]C(l*r1,w*wr)')
  p3 = parse_parametric_expression('C(l,w) : True -> !(w)F(l)[+(a2)$B(l*r2,w*wr)]B(l*r1,w*wr)')
  rules = [p1, p2, p3]
  r1 = 0.9
  r2 = 0.7
  a0 = 30.0*np.pi/180.0
  a2 = 30.0*np.pi/180.0
  d  = 137.5*np.pi/180.0
  wr = 0.707
  table = {'r1':str(r1),
           'r2':str(r2),
           'a0':str(a0),
           'a2':str(a2),
           'd':str(d),
           'wr':str(wr)}
  ngen = 10 

s = omega
for i in range(ngen):
  s = evolve(s, rules, table)

canvas = scene.SceneCanvas(keys='interactive',
                          bgcolor='white',
                          size=(800, 800),
                          show=True)
view = canvas.central_widget.add_view()

lines = []
HLU=init_HLU()

pos = np.array((0.0, 0.0, 0.0))
pts = []
bary = [pos]
stack = []

tokens = tokenize(s)

cur_w = 0.1

for t in tokens:
  if t[0] == 'F':
    if t[1][0]:
      L = float(t[1][0])
    new_pos = pos + HLU[:,0].T * L
    pts.append(new_pos)
    lines.append((pos, new_pos, cur_w))
    pos = new_pos
  elif t[0] == '+':
    if t[1][0]:
      delta = float(t[1][0])
    HLU = RU(HLU, delta)
  elif t[0] == '-':
    if t[1][0]:
      delta = float(t[1][0])
    HLU = RU(HLU, -delta)
  elif t[0] == '&':
    if t[1][0]:
      delta = float(t[1][0])
    HLU = RL(HLU, delta)
  elif t[0] == '^':
    if t[1][0]:
      delta = float(t[1][0])
    HLU = RL(HLU, -delta)
  elif t[0] == '\\':
    if t[1][0]:
      delta = float(t[1][0])
    HLU = RH(HLU, -delta)
  elif t[0] == '/':
    if t[1][0]:
      delta = float(t[1][0])
    HLU = RH(HLU, delta)
  elif t[0] == '!':
    cur_w = float(t[1][0])
  elif t[0] == '$':
    HLU = get_LU(HLU)
  elif t[0] == '[':
    stack.append((pos, d, HLU))
  elif t[0] == ']':
    pos, d, HLU = stack.pop()


pts = np.array(pts)
#sc = RawSegmentCollection('agg', linewidth="local")
#sc.append(lines[:,:3], lines[:,3:6], linewidth=lines[:,6])
#sc['antialias'] = 1
#sc['color'] = 'black'
#view.add(sc)
for p1, p2, w in lines:
  t = scene.visuals.Tube((p1, p2), radius=w, tube_points=5, shading='smooth', color='gray')
  view.add(t)
bary = sum(pts)
bary /= pts.shape[0]

view.camera = scene.TurntableCamera()
view.camera.center = bary
view.camera.up = 'y'

writer = imageio.get_writer('img_2.6_{}.png'.format(case_id))
im = canvas.render()
writer.append_data(im)
writer.close()

if __name__ == '__main__' and sys.flags.interactive == 0:
    canvas.app.run()

