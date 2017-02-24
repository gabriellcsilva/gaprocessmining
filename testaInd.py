import Individuo as ind
import GeneticOps as gops
import firingRule as fr
import collections as col

logTraces = {
    'A': ('A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A9'),
    'B': ('A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A8', 'A9'),
    'C': ('A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A8', 'A9'),
    'D': ('A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A7', 'A9')}

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
CM1 = col.OrderedDict([('A1', {'in': [], 'out': [['A8', 'A7', 'A9']]}), ('A2', {'in': [], 'out': ['A4', 'A3']}), ('A3', {'in': ['A2'], 'out': ['A5']}), ('A4', {'in': ['A2'], 'out': []}), ('A5', {'in': ['A3'], 'out': ['A6']}), ('A6', {'in': ['A5'], 'out': []}), ('A7', {'in': ['A1'], 'out': [['A9']]}), ('A8', {'in': ['A1'], 'out': ['A9']}), ('A9', {'in': [['A7', 'A8', 'A1']], 'out': []}), ('comeco', ['A1', 'A2']), ('fim', ['A4', 'A6', 'A9'])])
for i,val in CM1.items():
    print(i,'-', val)

resultado = gops.fitnessNew(CM1, logTraces)
print('__________')
print(resultado)

'''
for i,val in CMArtigo28.items():
    print(i,'-', val)

resultado = fr.fitnessNew(CMArtigo28, logTraces)
print('__________')
print(resultado)
'''