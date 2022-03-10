import numpy as np
import string

def init_HLU():
    H = np.array([1.0, 0.0, 0.0])
    L = np.array([0.0, 0.0, 1.0])
    U = np.cross(H, L)
    HLU = np.array((H, L, U)).T

    return HLU

def R2d(v, alpha):
    M = np.array(((np.cos(alpha), -np.sin(alpha)),
                  (np.sin(alpha),  np.cos(alpha))))
    return M.dot(v)

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

def parse_parametric_expression(expr):
  expr = expr.replace(' ', '')

  pred, rest = expr.split(':')
  cond, succ = rest.split('->')

  arguments = pred[2:-1].split(',')
  pred = pred[0]

  return ((pred, arguments), cond, succ)

def extract_bracket(expr, i):
  open = 1
  s = ''
  while open:
    c = expr[i]
    if c == ')':
      open -= 1
    elif c == '(':
      open += 1
    
    if open:
      s += c
    i+=1
  return s, i-1
    

def tokenize(expr):
  i = 0
  N = len(expr)
  mod_names = string.ascii_uppercase + string.ascii_lowercase + '+&/-[]'
  tokens = []
  while i < N:
    c = expr[i]
    if c in mod_names:
      if i+1 < N and expr[i+1] == '(':
        sub, i = extract_bracket(expr, i+2)
      else:
        sub = ''
      tokens.append((c, sub.split(',')))
    i+=1

  return tokens

def build_expressions(tokens):
    exprs = []
    for t in tokens:
        if t[1][0]:
            s = '{}({})'.format(t[0], ','.join(t[1]))
        else:
            s = t[0]
        exprs.append(s)
    return exprs

def is_parametric_expression_valid(expr, rule, table={}):
  mod = expr[0]
  args = expr[2:-1].split(',')

  if mod != rule[0][0]:
    return False, expr

  arg_list = list(zip(rule[0][1], args))

  cond_str = rule[1]
  for a in arg_list:
    cond_str = cond_str.replace(a[0], a[1])

  eval_cond = eval(cond_str)
  if not eval_cond:
    return False, expr

  succ = rule[2]
  for a in arg_list:
    succ = succ.replace(a[0], a[1])

  translation_table = dict({'^':'**'}, **table)
  for t in translation_table.items():
    succ = succ.replace(t[0], t[1])

  tokens = tokenize(succ)

  new_exp = ''
  for mod, params in tokens:
    if params[0]:
      p = list(str(eval(pa)) for pa in params)
      mod = mod + '({})'.format(','.join(p))
    new_exp += mod

  return True, new_exp