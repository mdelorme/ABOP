base = 'b'
rules = {'a':'ab', 'b':'a'}

def evolve(s):
    ns = ''
    for c in s:
        ns += rules[c]
    return ns

s = base
n_generations = 10
for i in range(n_generations):
    print('Generation #{} : {}'.format(i, s))
    s = evolve(s)
print('Final : {}'.format(s))
