import copy as copy
import collections as col
from numpy import random
import Individuo as ind
import GeneticOps as gops
import matplotlib.pyplot as plt


alfabetoTarefas = ["A1","A2","A3","A4","A5","A6","A7","A8","A9"]
#alfabetoTarefas = ["A1","A2","A3","A4", "A5", "A6"]

logTraces = {
    'A': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A9'],
    'B': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A8', 'A9'],
    'C': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A8', 'A9'],
    'D': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A7', 'A9']}
'''
logTraces = {
    'A': ('A1', 'A4', 'A2', 'A5'),
    'B': ('A1', 'A4', 'A3', 'A5'),
    'C': ('A1', 'A2', 'A4', 'A5'),
    'D': ('A1', 'A3', 'A4', 'A5')}
'''

'''
logTraces = {
    'A': ('A1', 'A2', 'A3', 'A4', 'A5'),
    'B': ('A1', 'A2', 'A3', 'A4', 'A6'),
    'C': ('A1', 'A2', 'A3', 'A4', 'A5'),
    'D': ('A1', 'A2', 'A3', 'A4', 'A6')}
'''

# Inicialização dos parâmetros
tamPop = 1000

mutation_rate = 0.6
crossover_rate = 1
elite_rate = 0.1
max_generations = 80
best_fitness = []
vetor_fitness = []
set_quant = set_quant = len(logTraces) * 15

populacao = [[ind.criarIndividuo(alfabetoTarefas),0] for x in range(tamPop)]

#TODO FAZER A POP INICIAL EM LIST, E NÃO DICT (e acertar os trechos onde eu uso items() pra fazer um sort)

for val in populacao:
    result = gops.fitnessNew(val[0], logTraces, set_quant)
    val[1] = result[0]

# Calculando os dados de fitness pros gráficos
aux = [val[1] for val in populacao]

min_fit = min(aux)
max_fit = max(aux)
avg = sum(aux) / len(aux)

# Armazeno o melhor indivíduo de cada geração
sorted_pop = sorted(populacao, key=lambda t: t[1])

best_fitness.append(sorted_pop[-1])
vetor_fitness.append([min_fit, max_fit, avg])

while max_generations > 0:
    new_pop = []
    print(max_generations)
    if random.random() < elite_rate:
        #Ordenando de novo só pra garantir, depois vou testar se é mesmo necessário
        # TODO se ocorre elitismo na primeira geração, dá index error ( porque a primeira população é dict, ajeitar)
        #populacao = sorted(populacao.items(), key=lambda x: x[1][1])
        new_pop.append(copy.deepcopy(populacao[-1]))
        new_pop.append(copy.deepcopy(populacao[-2]))

    while len(new_pop) < len(populacao):
        # Criando dois filhos por crossover (O próprio crossover chama a rotina de seleção dos pais)
        result = gops.crossover1(populacao, crossover_rate, alfabetoTarefas)
        offspring1 = result[0]
        offspring2 = result[1]

        # Fazendo a mutação
        offspring1[0] = gops.mutationB(offspring1[0], mutation_rate)
        offspring2[0] = gops.mutationB(offspring2[0], mutation_rate)

        # Calculando o fitness
        offspring1[1] = gops.fitnessNew(offspring1[0], logTraces, set_quant)[0]
        offspring2[1] = gops.fitnessNew(offspring2[0], logTraces, set_quant)[0]

        # Adicionando à nova população
        new_pop.append(offspring1)
        new_pop.append(offspring2)

    aux = [val[1] for val in new_pop]

    min_fit = min(aux)
    max_fit = max(aux)
    avg = sum(aux)/len(aux)

    sorted_pop = sorted(new_pop, key=lambda t: t[1])
    best_fitness.append(sorted_pop[-1])

    vetor_fitness.append([min_fit, max_fit, avg])
    populacao = new_pop

    max_generations -= 1
v_max = [i[1] for i in vetor_fitness]
v_min = [i[0] for i in vetor_fitness]
v_avg = [i[2] for i in vetor_fitness]
plt.plot(v_avg, label="Média", linewidth=2.0)
plt.plot(v_max, label="Maior fitness", linewidth=2.0)
plt.plot(v_min, label="Menor Fitness", linestyle=':', linewidth=1.0)
plt.ylabel("Fitness")
plt.xlabel("Gerações")
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=4, ncol=2, mode="expand", borderaxespad=0., prop={'size':10})
plt.ylim([-20,2])
plt.show()

print('maior fitness achado: ',max(v_max))
sorted_best = sorted(best_fitness, key=lambda t: t[1])
print('individuo: ', sorted_best[-1])


for i, val in best_fitness[-1][0].items():
    print('Tarefa',i, '\t => ', val)

print(best_fitness[-1])
print('fitness: ', best_fitness[-1][1])


