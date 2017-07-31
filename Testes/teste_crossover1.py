import GeneticOps as gops
import individuo_old as ind

alfabetoTarefas = ["A1","A2","A3","A4","A5"]
tamPop = 5

populacao = {x: [ind.criarIndividuo(alfabetoTarefas),0] for x in range(tamPop)}
for i, val in populacao.items():
    print(i,'\t',val,'\n')

print('\n')

result = gops.crossover1(populacao, 0.8, alfabetoTarefas)

for j in result:
    print(j,'\n')

print('\n')
'''
for i, val in populacao.items():
    print(i,'\t',val,'\n')
'''