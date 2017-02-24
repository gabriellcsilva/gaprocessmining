import Individuo as ind
import GeneticOps as gops
import collections as col
'''
logTraces = {
    'A': ('A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A9'),
    'B': ('A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A8', 'A9'),
    'C': ('A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A8', 'A9'),
    'D': ('A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A7', 'A9')}
'''
logTraces = {
    'A': ('A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A9')}

alfabetoTarefas = ["A1","A2","A3","A4","A5","A6","A7","A8","A9"]
#alfabetoTarefas = ["A1","A2","A3", "A4"]


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

CMReuniao = {

'A1': {'in': [], 'out': ['A4', 'A5', 'A2', 'A6']},
'A2': {'in': ['A1'], 'out': ['A3', 'A5']},
'A3': {'in': ['A2'], 'out': []},
'A4': {'in': ['A1'], 'out': ['A9']},
'A5': {'in': ['A1', 'A2'], 'out': []},
'A6': {'in': ['A1'], 'out': [['A8', 'A7']]},
'A7': {'in': ['A6'], 'out': []},
'A8': {'in': ['A6'], 'out': []},
'A9': {'in': ['A4'], 'out': []},
'comeco': ['A1'],
'fim': ['A3', 'A5', 'A7', 'A8', 'A9']
}

CM2 = {
'A1': {'in': [], 'out': ['A4', 'A9', 'A5', 'A2']},
'A2': {'in': ['A1'], 'out': [['A3']]},
'A3': {'in': ['A2'], 'out': ['A6']},
'A4': {'in': ['A1'], 'out': []},
'A5': {'in': ['A1'], 'out': [['A8', 'A7']]},
'A6': {'in': ['A3'], 'out': []},
'A7': {'in': ['A5'], 'out': []},
'A8': {'in': ['A5'], 'out': []},
'A9': {'in': ['A1'], 'out': []},
'comeco':['A1'],
'fim':['A4', 'A6', 'A7', 'A8', 'A9']
}

CMReuniao2 = {
'A1':  {'out': ['A2', 'A3', 'A6'], 'in': []},
'A2': {'out': ['A4', 'A5'], 'in': ['A1']},
'A3': {'out': [['A6']], 'in': ['A1']},
'A4': {'out': ['A6', 'A9'], 'in': ['A2']},
'A5': {'out': [['A7', 'A8']], 'in': ['A2']},
'A6': {'out': [], 'in': ['A3', 'A4', 'A1']},
'A7': {'out': [], 'in': ['A5']},
'A8': {'out': [], 'in': ['A5']},
'A9': {'out': [], 'in': ['A4']},
'comeco': ['A1'],
'fim': ['A6', 'A7', 'A8', 'A9']
}

CM3 = col.OrderedDict([('A1', {'out': [['A5']], 'in': []}), ('A2', {'out': ['A3'], 'in': ['A8']}), ('A3', {'out': [['A8', 'A4']], 'in': ['A2']}), ('A4', {'out': ['A9'], 'in': ['A3']}), ('A5', {'out': ['A6'], 'in': ['A1']}), ('A6', {'out': ['A7'], 'in': ['A5']}), ('A7', {'out': [], 'in': ['A6']}), ('A8', {'out': [['A9', 'A2']], 'in': ['A3']}), ('A9', {'out': [], 'in': [['A4', 'A8']]}), ('comeco', ['A1']), ('fim', ['A7', 'A9'])])
#for i,val in testeCM.items():
#    print("tarefa ", i," - in:", val['in'], "\t\t\t\t","out", val['out'])
    # print("tarefa ",i, " - ", val, ' tipo: ', type(val['saida'][0]), len(val['saida'][0]))

res = gops.fitness(CMReuniao2, logTraces)

print(res)

'''
print('_______________________________')

for i,val in testeCM.items():
    print("tarefa ", i," - in:", val['in'], "\t\t\t\t","out", val['out'])
    #print("tarefa ",i, " - ", val, ' tipo: ', type(val['out'][0]), len(val['out'][0]))

res2 = gops.fitness(testeCM, logTraces, alfabetoTarefas)

print(res2)

'''