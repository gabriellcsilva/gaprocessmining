import GeneticOps as gops
import collections as col
import individuo_old as ind
import traceMaker_OLD as tm

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
#print(j)
#i = ind.criarIndividuo(["A1","A2","A3","A4","A5","A6","A7","A8","A9"])
i = col.OrderedDict([('a', {'out': ['c', 'e', 'a', 'f', 'd'], 'in': [['a', 'c', 'd']]}), ('b', {'out': ['e', 'f', 'd'], 'in': []}), ('c', {'out': ['a'], 'in': ['a', 'd']}), ('d', {'out': [['a', 'c', 'e', 'f']], 'in': [['a', 'b']]}), ('e', {'out': [], 'in': [['a', 'b', 'd', 'f']]}), ('f', {'out': ['e'], 'in': ['a', 'b', 'd']}), ('comeco', ['b']), ('fim', ['e'])])
#i = col.OrderedDict([('A1', {'out': ['A4'], 'in': []}), ('A2', {'out': ['A3'], 'in': []}), ('A3', {'out': [], 'in': ['A2']}), ('A4', {'out': ['A5'], 'in': ['A1']}), ('A5', {'out': ['A6'], 'in': ['A4']}), ('A6', {'out': [['A8', 'A7']], 'in': ['A5']}), ('A7', {'out': ['A9'], 'in': ['A6']}), ('A8', {'out': [['A9']], 'in': ['A6']}), ('A9', {'out': [], 'in': [['A8', 'A7']]}), ('comeco', ['A1', 'A2']), ('fim', ['A3', 'A9'])])

print(i)
result = tm.traceMaker(i)

print(result)


