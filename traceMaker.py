import collections as col
import GeneticOps as gops
import numpy as np

def traceMaker(CM):
    '''CM = {
        'A1': {'in': [], 'out': ['A2']},
        'A2': {'in': ['A1'], 'out': ['A3', 'A4']},
        'A3': {'in': ['A2'], 'out': ['A5']},
        'A4': {'in': ['A2'], 'out': ['A5']},
        'A5': {'in': ['A3', 'A4'], 'out': ['A6']},
        'A6': {'in': ['A5'], 'out': [['A7', 'A8']]},
        'A7': {'in': ['A6'], 'out': ['A9']},
        'A8': {'in': ['A6'], 'out': ['A9']},
        'A9': {'in': [['A7', 'A8']], 'out': []},
        'comeco': ['A1'],
        'fim': ['A9']
    }'''

    #active is the set containing all enabled activities, possibly ready to be executed
    active = []
    #traceMade is the trace made by this function
    traceMade = []

    tabela_token = {x: 0 for x in CM.keys()}
    comeco = len(CM['comeco'])
    tabela_token['comeco'] = comeco

    # anexar na lista 'active' coloca a atividade (ou conjunto de atividades) na lista de habilitadas que podem ser executadas
    for com in CM['comeco']:
        active.append([com])

    #variable created to prevent from infinite loop individuals
    limitSet = len(CM.keys()) * 2
    limit = 0

    while len(active) > 0 and limit < limitSet:
        limit += 1
        #print(limit)
        #print('Lista de habilitados antes da iteração: ',active)
        # Escolhe uma posição da lista 'choice', que contém as tarefas habilitadas para executar - que podem ser uma tarefa simples ou uma expressão mais complexa, como AND/OR de tarefas.
        index_choice = np.random.choice(len(active))

        # se a posição escolhida tiver um OR de tarefas (to fazendo tudo baseado na primeira posição (index 0) do elemento escolhido no sorteio
        if isinstance(active[index_choice][0], list):
            # se for um OR, escolho uma das tarefas no OR sorteado para ser executada
            choice = [np.random.choice(active[index_choice][0])]
            #print('aquij', choice)
        else:
            choice = active[index_choice]
            #print('aquiw', choice)

        # ou se tiver uma sequência ou um AND
        '''
        elif isinstance(active[index_choice][0], str):
            # se for um and, faço uma lista de tarefas a serem executadas. Tenho que fazer um sorteio, já que o AND permite (segundo literatura) que as tarefas em questão sejam executadas em qualquer ordem.
            choice = list(np.random.choice(active[index_choice], len(active[index_choice]), False))
        '''
        # making copies of the data structures used, for the case of a uncomplete execution of a AND/OR task set (let's say that one task couldn't execute,
        # but i've changed the token table and other lists, so this way i can get them back to their previous states by reassigning them to these backup variables
        auxtable = tabela_token.copy()
        auxtrace = traceMade.copy()
        auxactive = active.copy()
        flag = 1


        for i in choice:
            #This FOR loop is mainly not needed, once the choice always have only one element

            # DONE- SE O CONJUNTO CHOICE FOR UM AND, CADA TAREFA TEM QUE SER EXECUTADA, ENTÃO EU TENHO QUE TER UM TIPO DE FLAG QUE ANULE TODA A 'EXECUÇÃO' (NÃO COLOQUE AS ATIVIDADES NO TRAÇO, NEM CONSUMA NENHUM TOKEN...)
            #print('1',i)
            try:
                # this try/except is to handle a task's empty input set
                if isinstance(CM[i]['in'][0], list):
                    for j in CM[i]['in'][0]:
                        if tabela_token[j] >= 1:
                            tabela_token[j] -= 1
                            traceMade.append(i)
                            if CM[i]['out']:
                                #print('dentro do ',i)
                                #print('active antes', active)
                                if isinstance(CM[i]['out'][0],str):
                                    for k in CM[i]['out']:
                                        #print('POhA',k)
                                        active.append([k])
                                else:
                                    active.append(CM[i]['out'])
                                #print('active depois', active)
                                tabela_token[i] += len(CM[i]['out'])
                            else:
                                tabela_token['fim'] += 1
                            flag = 0
                            break
                        else:
                            flag += 1

                elif isinstance(CM[i]['in'][0], str):
                    flag_and = 0
                    for j in CM[i]['in']:
                        if tabela_token[j] >= 1:
                            # todas as tarefas k tem que ter um token, se ao menos uma não tiver, j não é executada corretamente (penalidade+1)
                            tabela_token[j] -= 1
                        else:
                            flag_and += 1
                            break

                    if flag_and == 0:
                        traceMade.append(i)
                        if CM[i]['out']:
                            if isinstance(CM[i]['out'][0], str):
                                for k in CM[i]['out']:
                                    #print('POHA', k)
                                    active.append([k])
                            else:
                                active.append(CM[i]['out'])
                            tabela_token[i] += len(CM[i]['out'])
                        else:
                            tabela_token['fim'] += 1
                        flag = 0
                    else:
                        #print('aqui')
                        flag += 1
            except:
                if not CM[i]['in']:
                    if tabela_token['comeco'] >= 1:
                        # TODO parei aqui, falta decrescer os tokens, limpar o elemento escolhido do active e colocar a tarefa no trace... Pra or e pra and
                        tabela_token['comeco'] -= 1
                        traceMade.append(i)
                        if CM[i]['out']:
                            if isinstance(CM[i]['out'][0], str):
                                for k in CM[i]['out']:
                                    active.append([k])
                            else:
                                active.append(CM[i]['out'])
                            tabela_token[i] += len(CM[i]['out'])
                        else:
                            tabela_token['fim'] += 1
                        flag = 0
                        #the break here was causing the code to avoid the update of active list and etc.
                    else:
                        # o que colocar aqui? Esse é o caso negativo
                        flag += 1


            #if there was any task that didn't execute in the choice set, the flag should be != 0, then i return all the data structures back to their previous values
            if flag == 0:
                #print('aquui', active)
                active.remove(active[index_choice])
                #print('aquui2', active)

            else:

                #print('entrou na reparação')
                #print('antes token',tabela_token)
                tabela_token = auxtable
                #print('depois token', tabela_token)
                #print('antes trace', traceMade)
                traceMade = auxtrace
                #print('depois trace', traceMade)
                #print('antes active', active)
                active = auxactive
                #print('depois active', active)

                active.remove(active[index_choice])
                #se executou todos os ands e ors, manter a table e o traço
        #print('Lista de habilitados depois da iteração: ', active)

    if tabela_token['fim'] >= len(CM['fim']):
        tabela_token['fim'] -= len(CM['fim'])
        #print(tabela_token)
        #print('fim',active)
        return traceMade
    else:
        #print('tentativa de traço', traceMade)
        #print('x ray da tabela token', tabela_token)
        return []