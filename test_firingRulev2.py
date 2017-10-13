import firing_rule as fr
import collections as col
import new_genetic_ops as gops
import trace_maker as tm
import precision_calc as prc


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
CMArtigo28 = {
    'A1': {'in':[[],[]], 'out':[['AND'],['A2']]},
    'A2': {'in':[['AND'],['A1']], 'out':[['AND'],['A3', 'A4']]},
    'A3': {'in':[['AND'],['A2']], 'out':[['AND'],['A5']]},
    'A4': {'in':[['AND'],['A2']], 'out':[['AND'],['A5']]},
    'A5': {'in':[['AND'],['A3', 'A4']], 'out':[['AND'],['A6']]},
    'A6': {'in':[['AND'],['A5']], 'out':[['xOR'],['A7','A8']]},
    'A7': {'in':[['AND'],['A6']], 'out':[['AND'],['A9']]},
    'A8': {'in':[['AND'],['A6']], 'out':[['AND'],['A9']]},
    'A9': {'in':[['xOR'],['A7','A8']], 'out':[[],[]]},
    'inicio': [['AND'],['A1']],
    'fim': [['AND'],['A9']]
}

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

log_complex3 = {
    'A': ['A1', 'A5', 'A6', 'A9', 'A7', 'A11', 'A10', 'A13', 'A15', 'A16', 'A17'],
    'B': ['A1', 'A6', 'A3', 'A9', 'A7', 'A10', 'A11', 'A15', 'A12', 'A16', 'A17'],
    'C': ['A1', 'A5', 'A4', 'A8', 'A10', 'A15', 'A12', 'A16', 'A17'],
    'D': ['A1', 'A3', 'A2', 'A10', 'A14', 'A13', 'A8', 'A16', 'A17'],
    'E': ['A1', 'A4', 'A5', 'A8', 'A10', 'A15', 'A12', 'A16', 'A17'],
    'F': ['A1', 'A6', 'A3', 'A10', 'A14', 'A12', 'A16', 'A7', 'A9', 'A11', 'A17'],
}

ind_teste_complex3 = {
    'A1': {'in': [[], []], 'out': [['AND','xOR','xOR'], ['A2', 'A4', 'A6'], ['A3', 'A5']]},
    'A2': {'in': [['AND'], ['A1']], 'out': [['AND'], ['A8']]},
    'A3': {'in': [['AND'], ['A1']], 'out': [['AND'], ['A10']]},
    'A4': {'in': [['AND'], ['A1']], 'out': [['AND'], ['A8']]},
    'A5': {'in': [['AND'], ['A1']], 'out': [['AND'], ['A10']]},
    'A6': {'in': [['AND'], ['A1']], 'out': [['AND'], ['A7', 'A9']]},
    'A7': {'in': [['AND'], ['A6']], 'out': [['AND'], ['A11']]},
    'A8': {'in': [['xOR'], ['A2', 'A4']], 'out': [['AND'], ['A17']]},
    'A9': {'in': [['AND'], ['A6']], 'out': [['xOR'], ['A11']]},
    'A10': {'in': [['xOR'], ['A3', 'A5']], 'out': [['AND', 'xOR', 'xOR'], ['A12', 'A13'], ['A14', 'A15']]},
    'A11': {'in': [['AND'], ['A7', 'A9']], 'out': [['AND'], ['A17']]},
    'A12': {'in': [['AND'], ['A10']], 'out': [['AND'], ['A16']]},
    'A13': {'in': [['AND'], ['A10']], 'out': [['AND'], ['A16']]},
    'A14': {'in': [['AND'], ['A10']], 'out': [['AND'], ['A16']]},
    'A15': {'in': [['AND'], ['A10']], 'out': [['AND'], ['A16']]},
    'A16': {'in': [['AND', 'xOR', 'xOR'], ['A12', 'A13'], ['A14', 'A15']], 'out': [['AND'], ['A17']]},
    'A17': {'in': [['AND', 'xOR', 'AND'], ['A8', 'A11'], ['A16']], 'out': [[], []]},
    'inicio': [['AND'], ['A1']],
    'fim': [['AND'], ['A17']]
}


# result = fr.firingRule(ind_teste_complex3, log_complex3)
#
# print(result)
#
# for i, val in ind_teste_complex3.items():
#     print(i, ' ', val)

logTraces = {
    'A': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A9'],
    'B': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A8', 'A9'],
    'C': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A8', 'A9'],
    'D': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A7', 'A9']}

max_len = max([len(bar) for bar in logTraces.values()]) * 4
set_quant = len(logTraces)*2

a = col.OrderedDict([('A1', {'out': [[], []], 'in': [[], []]}),
             ('A2', {'out': [['AND', 'AND', 'AND'], ['A4', 'A2', 'A8', 'A6'], ['A9']], 'in': [['xOR'], ['A4', 'A6', 'A2']]}),
             ('A3', {'out': [['xOR'], ['A5']], 'in': [['AND'], ['A4', 'A7']]}),
             ('A4', {'out': [['xOR', 'xOR', 'xOR'], ['A7'], ['A3', 'A2', 'A9']], 'in': [['xOR', 'xOR', 'xOR'], [], ['A6', 'A2']]}),
             ('A5', {'out': [[], []], 'in': [['AND'], ['A7', 'A3']]}),
             ('A6', {'out': [['AND'], ['A2', 'A7', 'A4']], 'in': [['xOR', 'xOR', 'xOR'], ['A2', 'A7'], []]}),
             ('A7', {'out': [['xOR'], ['A3', 'A9', 'A6', 'A7', 'A5']], 'in': [['xOR'], ['A4', 'A6', 'A7']]}),
             ('A8', {'out': [[], []], 'in': [['AND'], ['A2']]}),
             ('A9', {'out': [['xOR'], ['A9']], 'in': [['AND'], ['A4', 'A2', 'A7', 'A9']]}),
             ('fim', [['xOR'], ['A5', 'A1', 'A8']]),
             ('inicio', [['xOR'], ['A1']])])


max_len = max([len(x) for x in logTraces.values()]) * 4
set_quant = len(logTraces) * 4
art_logs = []
for i in range(set_quant):
    trace = tm.trace_maker(CMArtigo28, max_len)
    if trace[0]:
        art_logs.append(trace[1])

result = prc.positional_set(art_logs)

for i, val in sorted(result.items()):
    print(i,'-', val)


test = {'A4': {'before': {'A2', 'A3'}, 'after': {'A5', 'A3'}}, 'A7': {'before': {'A6'}, 'after': {'A9'}}, 'A8': {'before': {'A6'}, 'after': {'A9'}}, 'A5': {'before': {'A4', 'A3'}, 'after': {'A6'}}, 'A2': {'before': set(), 'after': {'A4', 'A3'}}, 'A9': {'before': {'A7', 'A8'}, 'after': set()}, 'process': {'end': {'A9'}, 'start': {'A2'}}, 'A6': {'before': {'A5'}, 'after': {'A7', 'A8'}}, 'A3': {'before': {'A2', 'A4'}, 'after': {'A5', 'A4'}}}
test2 = {'A1': {'before': set(), 'after': {'A2'}}, 'A2': {'before': {'A1'}, 'after': set()}, 'process':{'start': {'A1'}, 'end':{'A2'}}}
fit = prc.positional_precision(test, result)
print(fit)