import collections as col

a = col.OrderedDict(
    [('A', {'out': [['AND'], ['B', 'G', 'E', 'D', 'C', 'A']], 'in': [['xOR'], ['A', 'D', 'G']]}),
    ('B', {'out': [['AND', 'xOR', 'AND'], ['B'], ['G', 'D']], 'in': [['AND'], ['A', 'B', 'D', 'F']]}),
    ('C', {'out': [[], []], 'in': [['AND'], ['A', 'D', 'E', 'F']]}),
    ('D', {'out': [['xOR'], ['C', 'E', 'A', 'B']], 'in': [['xOR', 'xOR', 'AND'], ['A'], ['B']]}),
    ('E', {'out': [['AND', 'xOR', 'xOR'], [], ['C']], 'in': [['AND', 'xOR', 'xOR'], ['A', 'D'], ['F']]}),
    ('F', {'out': [['xOR'], ['C', 'E', 'G', 'B']], 'in': [[], []]}),
    ('G', {'out': [['AND', 'AND', 'xOR'], [], ['A']], 'in': [['AND', 'xOR', 'AND'], ['A', 'B', 'F'], []]}),
    ('inicio', [['AND'], ['F']]),
    ('fim', [['xOR'], ['C']])])

table_token = {task: [] for task in a.keys()}

for i in table_token.keys() - ['inicio','fim']:
    if not a[i]['out'][0]:
        table_token['fim'].append(i)
        table_token['fim'].append(i)
    else:
        table_token[i].append(a[i]['out'])
        table_token[i].append(a[i]['out'])


table_token['inicio'].append(a['inicio'])
print('referencia')
'''
for p in table_token.items():
    print(p)
'''
fim_set = table_token.pop('fim')

#aux = [j for i in table_token.values() for j in i]
# Only got knows why len(j[-1]) works and len(j[1]) doesnt - they're the same index...
# God told me that it doesn't work because the tokens in the 'fim' key have only the 0 index, so using -1 works

# That's a "double" comprehension, the structure is this:
# [ (statement) (optional(if statement else statement) (outter for loop (inner for loop)) ]
# then i apply the sum function to the whole structure
# basically, the if separates complex structures from simple ones, so i know what index to apply len()
# TODO Note to myself: separate the 'fim' from the others, since with a bigger task name, accessing indexes and/or getting len()
# TODO could lead to inconsistencies
aux = sum([len(j[2])+len(j[1]) if len(j[0])==3 else len(j[-1]) for i in table_token.values() for j in i]) + len(fim_set)
print(aux)
'''
for i in table_token.values():
    for j in i:
        print(j)
        
'''
print('measurement test')
print(len(table_token))