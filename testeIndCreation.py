import Individuo as ind
import GeneticOps as gops

alfabetoTarefas = ["A1","A2","A3","A4","A5","A6","A7","A8","A9"]

testeCM = ind.criarIndividuo(alfabetoTarefas)

for k, val in testeCM.items():
    print(k, '\t', val)


'''testeCM = {
    'A1': {'in':['A3'], 'out':['A9']},
    'A2': {'in':['A3'], 'out':['A6']},
    'A3': {'in':[], 'out':['A2']},
    'A4': {'in':['A9'], 'out':['A8']},
    'A5': {'in':['A3'], 'out':['A8']},
    'A6': {'in':['A9'], 'out':['A7']},
    'A7': {'in':['A3'], 'out':['A6']},
    'A8': {'in':['A3'], 'out':['A3']},
    'A9': {'in':['A1'], 'out':[]}
}
'''

print('\n')
testeCMM = gops.mutationA(testeCM, 1)

for k, val in testeCMM.items():
    print(k, '\t', val)
