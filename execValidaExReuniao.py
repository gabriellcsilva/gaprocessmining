import Individuo as ind
import GeneticOps as gops

logTraces = {
    'A': ('A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A9'),
    'B': ('A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A8', 'A9'),
    'C': ('A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A8', 'A9'),
    'D': ('A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A7', 'A9')}


#logTraces = {'A': ('A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A9')}
#logTraces = {'B': ('A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A8', 'A9')}
#logTraces = {'C': ('A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A8', 'A9')}
#logTraces = {'D': ('A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A7', 'A9')}


alfabetoTarefas = ["A1","A2","A3","A4","A5","A6","A7","A8","A9"]
#alfabetoTarefas = ["A1","A2","A3", "A4"]
testeCM = ind.criarIndividuo(alfabetoTarefas)
'''testeCM = {
    'A1': {'in':[['A3', 'A5']], 'out':['A9']},
    'A2': {'in':['A3'], 'out':['A6']},
    'A3': {'in':[], 'out':['A5', 'A8', 'A1', 'A3', 'A7', 'A9', 'A2']},
    'A4': {'in':[['A5', 'A9']], 'out':['A8']},
    'A5': {'in':['A3'], 'out':['A6', 'A3', 'A1', 'A7', 'A4', 'A8']},
    'A6': {'in':[['A2', 'A5', 'A7', 'A9']], 'out':['A7']},
    'A7': {'in':[['A3', 'A5', 'A6']], 'out':['A6']},
    'A8': {'in':['A3', 'A4', 'A5', 'A9'], 'out':['A3']},
    'A9': {'in':['A1','A3'], 'out':[]}
}'''
# OBS importante: Aparentemente o token game está bem feito, após experimentos incluindo e retirando atividades do modelo abaixo,
# observou-se que a marcação final de tokens ou a quantidade de punições exprime a incapacidade do modelo de representar o traço de eventos usado:
# 1- Ao retirar tarefas do output, tokens relativos a essas não serão produzidos, o que forçará que sejam produzidos tokens artificiais, punindo o individuo.
# 2- Ao retirar tarefas do input, tokens produzidos pelos outputs não serão consumidos, acusando na marcação da tabela de tokens
CMArtigo28 = {
    'A1': {'in':[], 'out':['A2']},
    'A2': {'in':['A1'], 'out':['A3', 'A4']},
    'A3': {'in':['A2'], 'out':['A5']},
    'A4': {'in':['A2'], 'out':['A5']},
    'A5': {'in':['A3', 'A4'], 'out':['A6']},
    'A6': {'in':['A5'], 'out':[['A7','A8']]},
    'A7': {'in':['A6'], 'out':['A9']},
    'A8': {'in':['A6'], 'out':['A9']},
    'A9': {'in':[['A7','A8']], 'out':[]}
}


#for i,val in testeCM.items():
#    print("tarefa ", i," - in:", val['in'], "\t\t\t\t","out", val['out'])
    # print("tarefa ",i, " - ", val, ' tipo: ', type(val['saida'][0]), len(val['saida'][0]))

res = gops.fitness(CMArtigo28, logTraces, alfabetoTarefas)

print('fitness: ', res[0], '\nCorretamente executadas: ', res[1],'\ntotal de eventos no log: ', res[2],'\nTraços corretamente executados: ', res[3], '\ntotal de traços no log: ', res[4], '\nTotal de penalidades: ', res[5])

print('_______________________________')

for i,val in testeCM.items():
    print("tarefa ", i," - in:", val['in'], "\t\t\t\t","out", val['out'])
    #print("tarefa ",i, " - ", val, ' tipo: ', type(val['out'][0]), len(val['out'][0]))

res2 = gops.fitness(testeCM, logTraces, alfabetoTarefas)

print('fitness: ', res2[0], '\nCorretamente executadas: ', res2[1],'\ntotal de eventos no log: ', res2[2],'\nTraços corretamente executados: ', res2[3], '\ntotal de traços no log: ', res2[4], '\nTotal de penalidades: ', res2[5])