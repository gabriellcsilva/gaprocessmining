import pandas as pd
import copy as copy
import collections as col
from numpy import random
import individuo_old as ind
import GeneticOps as gops
import matplotlib.pyplot as plt
import preprocessLog as pps

log = pd.read_csv("evcteste1.csv", sep=";", encoding = "latin1", header=None)
log = log[4]
### TRANSFORMANDO ATIVS DO LOG EM LETRAS DO ALFABETO ###
pps.preprocess(log)

prelog = {'A': log}

alfabetoTarefas = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','X','Y']


'''
log = log[log[4] !='login error']
### login error filtrado ###
log.to_csv("evcteste1.csv", sep=";", index=False, header=False)
#log = pd.read_csv("logs/teste.csv", sep=";", encoding = "latin1", header=None)
#log = pd.read_csv("evc.csv", sep=";", encoding = "latin1", header=None)
#set = log[4].unique()
'''

dicionario_ativ = {
    'A' : 'user logout',
    'B' : 'resource view',
    'C' : 'url view',
    'D' : 'course view',
    'E' : 'user login',
    'F' : 'page view',
    'G' : 'workshop view',
    'H' : 'assignment view',
    'I' : 'assignment upload',
    'J' : 'blog view',
    'K' : 'user view all',
    'L' : 'user view',
    'M' : 'user change password',
    'N' : 'data view',
    'O' : 'message write',
    'P' : 'user update',
    'Q' : 'data add',
    'R' : 'data update',
    'S' : 'blog update',
    'T' : 'blog add',
    'U' : 'forum view forum',
    'V' : 'assignment view all',
    'X' : 'data record delete',
    'Y' : 'library mailer'}

# Inicialização dos parâmetros
tamPop = 50

mutation_rate = 0.3
crossover_rate = 0.8
elite_rate = 0.3
max_generations = 100
best_fitness = []
vetor_fitness = []

populacao = {x: [ind.criarIndividuo(alfabetoTarefas),0] for x in range(tamPop)}

#TODO FAZER A POP INICIAL EM LIST, E NÃO DICT (e acertar os trechos onde eu uso items() pra fazer um sort)

for i, val in populacao.items():
    result = gops.fitness(val[0], prelog, alfabetoTarefas)
    val[1] = result[0]

# Calculando os dados de fitness pros gráficos
aux = [val[1] for i, val in populacao.items()]

min_fit = min(aux)
max_fit = max(aux)
avg = sum(aux) / len(aux)
# Armazeno o melhor indivíduo de cada geração
sorted_pop = sorted(populacao.items(), key=lambda t: t[1][1])
best_fitness.append(sorted_pop[-1])
vetor_fitness.append([min_fit, max_fit, avg])

while max_generations > 0:
    new_pop = []

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
        offspring1[0] = gops.mutationA(offspring1[0], mutation_rate)
        offspring2[0] = gops.mutationA(offspring2[0], mutation_rate)

        # Calculando o fitness
        offspring1[1] = gops.fitness(offspring1[0], prelog, alfabetoTarefas)[0]
        offspring2[1] = gops.fitness(offspring2[0], prelog, alfabetoTarefas)[0]

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

plt.show()


for i, val in best_fitness[-1][0].items():
    print('Tarefa',i, '\t => ', val)

print('fitness: ', best_fitness[-1][1])