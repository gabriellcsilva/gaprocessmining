import timeit
print(timeit.timeit('''

import collections as col
import precisionCalc as pc
import GeneticOps as gops
import Individuo as ind


logTraces = {
    'A': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A9'],
    'B': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A8', 'A9'],
    'C': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A8', 'A9'],
    'D': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A7', 'A9']}


CMArtigo28 = {
    'A1': {'in':[], 'out':['A2']},
    'A2': {'in':['A1'], 'out':['A3', 'A4']},
    'A3': {'in':['A2'], 'out':['A5']},
    'A4': {'in':['A2'], 'out':['A5']},
    'A5': {'in':['A3', 'A4'], 'out':['A6']},
    'A6': {'in':['A5'], 'out':[['A7','A8']]},
    'A7': {'in':['A6'], 'out':['A9']},
    'A8': {'in':['A6'], 'out':['A9']},
    'A9': {'in':[['A7','A8']], 'out':[]},
    'comeco': ['A1'],
    'fim': ['A9']
}
j = col.OrderedDict(CMArtigo28)

#i = col.OrderedDict([('A1', {'out': ['A4'], 'in': []}), ('A2', {'out': ['A3'], 'in': []}), ('A3', {'out': [], 'in': ['A2']}), ('A4', {'out': ['A5'], 'in': ['A1']}), ('A5', {'out': ['A6'], 'in': ['A4']}), ('A6', {'out': [['A8', 'A7']], 'in': ['A5']}), ('A7', {'out': ['A9'], 'in': ['A6']}), ('A8', {'out': [['A9']], 'in': ['A6']}), ('A9', {'out': [], 'in': [['A8', 'A7']]}), ('comeco', ['A1', 'A2']), ('fim', ['A3', 'A9'])])
##i = ind.criarIndividuo(["A1","A2","A3","A4","A5","A6","A7","A8","A9"])
set_quant = len(logTraces) * 15


precision_result = pc.precisionCalc(logTraces,j,set_quant)
''', number = 1000))


'''
for k in precision_result:
    print(k)

res1 = gops.fitnessNew(CMArtigo28, logTraces)
res2 = gops.fitnessNew(i, logTraces)

print('1', res1)
print('2', res2)

'''