import firingRule as fr


# alfabetoTarefas = ["A1","A2","A3","A4","A5","A6","A7","A8","A9"]
#
# logTraces = {
#     'A': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A9'],
#     'B': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A8', 'A9'],
#     'C': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A8', 'A9'],
#     'D': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A7', 'A9']}
#
# logA = {
#     'A': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A9']
# }
#
# logB = {
#     'B': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A8', 'A9']}
#
# logC = {
#     'C': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A8', 'A9']}
#
# logD = {
#     'D': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A7', 'A9']}
#
#
# CMArtigo28 = {
#     'A1': {'in':[[],[]], 'out':[['AND'],['A2']]},
#     'A2': {'in':[['AND'],['A1']], 'out':[['AND'],['A3', 'A4']]},
#     'A3': {'in':[['AND'],['A2']], 'out':[['AND'],['A5']]},
#     'A4': {'in':[['AND'],['A2']], 'out':[['AND'],['A5']]},
#     'A5': {'in':[['AND'],['A3', 'A4']], 'out':[['AND'],['A6']]},
#     'A6': {'in':[['AND'],['A5']], 'out':[['xOR'],['A7','A8']]},
#     'A7': {'in':[['AND'],['A6']], 'out':[['AND'],['A9']]},
#     'A8': {'in':[['AND'],['A6']], 'out':[['AND'],['A9']]},
#     'A9': {'in':[['xOR'],['A7','A8']], 'out':[[],[]]},
#     'inicio': [['AND'],['A1']],
#     'fim': [['AND'],['A9']]
# }

alfa_complex = ('A1','A2','A3','A4','A5','A6')

log_complex = {
    'A': ['A4','A3','A5']
}
log_complex2 = {
    'A': ['A4', 'A3', 'A1', 'A4', 'A5'],
    'B': ['A4', 'A3', 'A5']
}

log_complex1 = {
    'B' : ['A1', 'A6', 'A6', 'A6', 'A6', 'A6', 'A6', 'A6', 'A6']
}


ind_teste_complex = {
'A1' : {'in': [[], []], 'out': [['AND', 'AND', 'AND'], ['A6'], []]},
'A2' : {'in': [['AND'], ['A2', 'A4']], 'out': [['AND', 'AND', 'AND'], ['A6'], ['A2']]},
'A3' : {'in': [['AND', 'xOR', 'xOR'], ['A4'], []], 'out': [['xOR'], ['A5', 'A6']]},
'A4' : {'in': [[], []], 'out': [['AND', 'AND', 'AND'], ['A2'], ['A6', 'A3']]},
'A5' : {'in': [['AND'], ['A3']], 'out': [[], []]},
'A6' : {'in': [['AND', 'xOR', 'xOR'], ['A1', 'A2'], ['A3', 'A4', 'A6']], 'out': [['AND', 'xOR', 'AND'], ['A6'], []]},
'inicio' : [['xOR'], ['A1', 'A4']],
'fim' : [['AND'], ['A5']]
}


result = fr.firingRule(ind_teste_complex, log_complex2)

print(result)

for i, val in ind_teste_complex.items():
    print(i, ' ', val)