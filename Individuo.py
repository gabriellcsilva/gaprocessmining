from numpy import random
import collections as col
import copy as copy

def criarIndividuo(alfabetoTarefas):
    matrizInd = {tarefa: {"in": [], "out": []} for tarefa in alfabetoTarefas}
    matrizInd = col.OrderedDict(sorted(matrizInd.items(), key=lambda t: t[0]))

    ##########OBS DA SARA: A TAREFA A SER A INICIAL TEM QUE SER EXCLUÍDA DOS SORTEIOS, DE FORMA QUE NENHUMA CHEGUE NELA (INPUT {})
    ###EM VEZ DE SUBSTITUIR O SORTEADO COM VAZIO, ADICIONAR O VAZIO?
    ###INCLUIR A REPETIÇÃO FUTURAMENTE

    '''
    Preenchendo aleatoriamente os conjuntos de I/O de cada tarefa
    '''
    sorteioIO = random.choice(alfabetoTarefas, 2, False)
    #removendo a tarefa que será o input
    alfabeto = copy.deepcopy(alfabetoTarefas)
    alfabeto.remove(sorteioIO[0])

    #matrizInd[sorteioIO[1]]['out'] = []

    #TODO: ESCOLHER UM PRA RETIRAR DO ALFABETO, E OUTRO PRA VIRAR UM CASO DE IF NO FOR ABAIXO
    #todo IF tarefa == sorteioOutput: conj[out] = []
    #todo alfabetoTarefas.remove(sorteioInput)

    # OBS.: Depois tem que pensar em como trabalhar com a primeira e última atividade do processo,
    # ou seja, a in da primeira e a saída da última (deixar esses conjuntos vazios)
    # OBS2.: Os conjuntos de in serão decididos com base no sorteio dos de saída

    for tarefa, conj in matrizInd.items():
        if tarefa == sorteioIO[1]:
            conj['out'] = []
        else:
            roleta = random.random()
            ''' if tarefa = tarefa escolhida pra seer o fim: out = [] else continua a rotina abaixo '''
            if (roleta <= 0.34):
                # o conjunto de saída será apenas uma atividade (caso sequencial)
                conj["out"].append(random.choice(alfabeto))

            elif (0.34 < roleta <= 0.67):
                # o conjunto de saída será um AND(a,b,c,d...), expresso no seguinte formato -> [a,b,c,d]...]
                qtdTasks = random.random_integers(1, len(alfabeto))
                sorteio = random.choice(alfabeto, qtdTasks, False)
                sorteio = list(sorteio)
                #conj["out"].extend(sorteio)
                #conj["out"] = [a for a in sorteio]
                conj["out"] = sorteio
            else:
                qtdTasks = random.random_integers(2, len(alfabeto))
                sorteio = random.choice(alfabeto, qtdTasks, False)
                sorteio = list(sorteio)
                conj["out"].append(sorteio)
                # o conjunto de saída será um OR(a,b,c,d...), expresso no seguinte formato -> [[a,b,c,d...]]

    ###PREENCHENDO O INPUT###
    ##juntar com o trecho acima##

    for i, val in matrizInd.items():
        #Caso 1: se for uma instancia de array - ou seja, um OR
        try:
            if isinstance(val["out"][0],list):
                for j in val['out'][0]:
                    #print(i, 'saída: ', j)
                    matrizInd[j]['in'].append(i)
            #Caso 2: se for uma lista - ou seja, uma sequência única ou um AND
            else:
                for j in val['out']:
                    #print(i, 'saída: ', j)
                    matrizInd[j]['in'].append(i)
        except:
            continue


    # Mudando a relação do input pra OR ou deixando AND
    for i, val in matrizInd.items():
        if len(val['in']) > 1:
            if (random.random()>0.5):
                val['in'] = [val['in']]
    #

    ### preenchendo os inicios e fins do processo
    comeco = []
    fim = []
    for i, val in matrizInd.items():
        if not val['in']:
            comeco.append(i)

        if not val['out']:
            fim.append(i)
    ###


    ###mudando a relação da entrada e saída do processo
    if len(comeco) >= 2:
        if (random.random() > 0.5):
            comeco = [comeco]
    elif len(fim) >= 2:
        if (random.random() > 0.5):
            fim = [fim]
    ###

    matrizInd['comeco'] = comeco
    matrizInd['fim'] = fim

    return matrizInd


