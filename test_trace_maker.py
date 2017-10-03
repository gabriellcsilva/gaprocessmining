import trace_maker as tm
import firing_rule as fr
import json as json
import precision_calc as prc
import new_genetic_ops as gops


ind_teste_complex = {
    'A1': {'in': [[], []], 'out': [['AND', 'AND', 'AND'], ['A6'], []]},
    'A2': {'in': [['AND'], ['A2', 'A4']], 'out': [['AND', 'AND', 'AND'], ['A6'], ['A2']]},
    'A3': {'in': [['AND', 'xOR', 'xOR'], ['A4'], []], 'out': [['xOR'], ['A5', 'A6']]},
    'A4': {'in': [[], []], 'out': [['AND', 'AND', 'AND'], ['A2'], ['A6', 'A3']]},
    'A5': {'in': [['AND'], ['A3']], 'out': [[], []]},
    'A6': {'in': [['AND', 'xOR', 'xOR'], ['A1', 'A2'], ['A3', 'A4', 'A6']], 'out': [['AND', 'xOR', 'AND'], ['A6'], []]},
    'inicio': [['xOR'], ['A1', 'A4']],
    'fim': [['AND'], ['A5']]
    }

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


ind_teste_complex2 = {
    'A1': {'in': [[], []], 'out': [['AND', 'xOR', 'xOR'], ['A2', 'A4'], ['A3', 'A5']]},
    'A2': {'in': [['AND'], ['A1']], 'out': [['AND'], ['A6']]},
    'A3': {'in': [['AND'], ['A1']], 'out': [['AND'], ['A8']]},
    'A4': {'in': [['AND'], ['A1']], 'out': [['AND'], ['A7']]},
    'A5': {'in': [['AND'], ['A1']], 'out': [['AND'], ['A8']]},
    'A6': {'in': [['AND'], ['A2']], 'out': [['AND'], ['A8']]},
    'A7': {'in': [['AND'], ['A4']], 'out': [['AND'], ['A8']]},
    'A8': {'in': [['AND', 'xOR', 'xOR'], ['A6', 'A7'], ['A3', 'A5']], 'out': [[], []]},
    'inicio': [['xOR'],['A1']],
    'fim': [['xOR'],['A8']]
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

ind_teste_complex3altered = {
    'A1': {'in': [[], []], 'out': [['AND','xOR','xOR'], ['A4', 'A6'], ['A3', 'A5']]},
    'A2': {'in': [[], []], 'out': [['AND'], ['A8']]},
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
    'inicio': [['AND'], ['A1','A2']],
    'fim': [['AND'], ['A17']]
}


# result = tm.trace_maker(CMArtigo28, 20)
#
# print(result)

logTraces = {
    'A': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A9'],
    'B': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A8', 'A9'],
    'C': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A8', 'A9'],
    'D': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A7', 'A9']}

logs_art_process02 = {
    'A': ['A1', 'A5', 'A4', 'A7', 'A8'],
    'B': ['A1', 'A4', 'A5', 'A7', 'A8'],
    'C': ['A1', 'A3', 'A2', 'A6', 'A8'],
    'D': ['A1', 'A5', 'A2', 'A6', 'A8'],
    'E': ['A1', 'A2', 'A3', 'A6', 'A8'],
    'F': ['A1', 'A3', 'A4', 'A7', 'A8'],
    'G': ['A1', 'A4', 'A3', 'A7', 'A8'],
    'H': ['A1', 'A2', 'A5', 'A6', 'A8']}

with open('my_jsonprocess03.txt') as fp:
    logs_art_process03 = json.load(fp)
'''if ['A1', 'A2', 'A6', 'A3', 'A8', 'A9', 'A7', 'A11', 'A10', 'A12', 'A15', 'A16', 'A17'] in logs_art_process03.values():
    print('yes')
else:
    print('po')
exit()'''
setquant = int(len(logs_art_process03) * 1)
max_len_trace = max([len(x) for x in logs_art_process03.values()]) * 4
weights = {'comp': 0.8, 'prec': 0.2}

result = prc.precision_calc_full(logs_art_process03, ind_teste_complex3altered, setquant, max_len_trace)

print(result)

# result = gops.fitness(ind_teste_complex2, logs_art_process02, setquant, max_len_trace, weights)








'''
# result = fr.firingRule(ind_teste_complex3, logs03)

for foo, bar in result[0].items():
    print(foo, '-> ', bar)
print(result[1])
'''
'''
logs_art = []
for i in range(1000000):
    result = tm.trace_maker(ind_teste_complex3, 20)
    if result[0] == True:
        if result[1] not in logs_art:
            logs_art.append(result[1])

sorted_logs = sorted(logs_art)
print(len(sorted_logs))

logs_art_process03 = {i:val for i, val in enumerate(sorted_logs)}

with open('my_json.txt', 'w') as fp:
    json.dump(logs_art_process03, fp)
'''

'''
setquant = len(logTraces) * 15

precision = prc.precision_calc(logTraces,CMArtigo28, setquant,20)

print(precision[0])
'''