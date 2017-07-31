from numpy import random
import copy as copy
import firingRuleOld as fr
import math as math
import individuo_old as ind
import precision_calc as pc

# Fitness com nova implementação da firing rule (Todo: Falta representar e lidar com os tokens de encerramento)

def fitnessNew(individuo, logs, set_quant):
    resultado = fr.firingRule(individuo, logs)
    variaveis = resultado[-1]
    total_len_traces = sum([len(x) for x in logs.values()])
    total_traces = len(logs)

    # Na formula, no lugar de parsed_traces tem o numero de traços no log menos os que não foram totalmente executados (onde ocorreu
    # punição por faltar tokens. Como eu já tinha calculado o numero de traços executados corretamente, dá na mesma.


    punishment = (variaveis['missing_tokens_all'] / (variaveis['parsed_traces_all'] + 1)) + \
                 (variaveis['soma_tabela_tokens_all'] / (total_traces - variaveis['traces_tokens_left_all'] + 1)) + \
                 variaveis['penal_ini_all'] + variaveis['penal_fim_all']
    # print(punishment)

    # TODO SOMAR O BEGIN PUNISHMENT E VER SE TÁ FAZENDO DIFERENÇA

    precisao = pc.precisionCalc(logs,individuo,set_quant)[0]

    completude = ((variaveis['parsed_all'] - punishment) / total_len_traces)

    #finalScore = (score + precisao) / 2
    finalScore = (completude*0.5) + (precisao*0.5)

    # Formula do artigo 372: score = (0.4 * (parsed/total_len_traces)) + (0.6 * (parsed_traces/total_traces))
    # score = (0.4 * (parsed / total_len_traces)) + (0.6 * (parsed_traces / total_traces))

    return [finalScore, resultado, completude, precisao]


def fitnessOld_22_02_2017(individuo, logs):
    resultado = fr.firingRule(individuo, logs)
    variaveis = resultado[-1]
    total_len_traces = sum([len(x) for x in logs.values()])
    total_traces = len(logs)

    # Na formula, no lugar de parsed_traces tem o numero de traços no log menos os que não foram totalmente executados (onde ocorreu
    # punição por faltar tokens. Como eu já tinha calculado o numero de traços executados corretamente, dá na mesma.


    punishment = (variaveis['missing_tokens_all'] / (variaveis['parsed_traces_all'] + 1)) + \
                 (variaveis['soma_tabela_tokens_all'] / (total_traces - variaveis['traces_tokens_left_all'] + 1)) + \
                 variaveis['penal_ini_all'] + variaveis['penal_fim_all']
    # print(punishment)

    # TODO SOMAR O BEGIN PUNISHMENT E VER SE TÁ FAZENDO DIFERENÇA
    combInd = 1
    for i, val in individuo.items():
        if i not in ("comeco", "fim"):
            if val['out']:
                try:
                    if isinstance(val['out'][0], list):
                        # print(val['out'])
                        combInd *= math.factorial(len(val['out'][0]))
                    else:
                        combInd *= math.factorial(len(val['out']))
                except:
                    print('não deveria vir pra essa exception')

    if len(individuo['comeco']) != 0:
        combInd *= math.factorial(len(individuo['comeco']))
    else:
        combInd *= 1000000
    '''if len(individuo['fim']) != 0:
        combInd *= math.factorial(len(individuo['fim']))
    else:
        combInd *= 1000000'''

    precisao = abs(1 - (combInd / len(logs)))
    print('precisão', precisao)
    precisaoExp = math.exp(-precisao)
    print('precisaoExp', precisaoExp)

    score = ((variaveis['parsed_all'] - punishment) / total_len_traces)

    finalScore = (score + precisaoExp) / 2

    # Formula do artigo 372: score = (0.4 * (parsed/total_len_traces)) + (0.6 * (parsed_traces/total_traces))
    # score = (0.4 * (parsed / total_len_traces)) + (0.6 * (parsed_traces / total_traces))

    return [finalScore, resultado, score, precisaoExp]


def fitness(ind, traces):
    # token_table['fim'] = len(ind['fim'])
    parsed = 0
    beginPenalty = 0

    tokens_left = []
    # OBS.: Faz sentido zerar a tabela de tokens de um traço pra outro?
    parsed = 0
    # Detalhe p/ depois: os +1 na var 'parsed' são inúteis, já que eu to calculando mais na frente pelas penalidades
    penalty = 0
    missing_tokens = 0
    parsed_traces = 0
    traces_tokens_left = 0
    total_traces = len(traces)

    for i, val in traces.items():
        token_table = {x: 0 for x in ind.keys()}
        token_table['comeco'] = len(ind['comeco'])

        beginTraces = val[:token_table['comeco']]
        otherTraces = val[token_table['comeco']:]

        # Executando os traços de eventos iniciais de acordo com a quantidade de tarefas iniciais do indivíduo
        if token_table['comeco'] >= 1:
            for j in beginTraces:
                try:
                    # se eu achar o evento no conjunto de começos, eu marco como executado corretamente e passo pro próximo
                    # Só vai funcionar se for puro OR/AND, ou se eu fixar o OR na primeira posição e garantir que só vou buscar um traço de evento nele apenas uma vez, senão o OR pode se comportar como AND!
                    for task in ind['comeco']:
                        if isinstance(task, list):
                            # caso o conjunto de começos contenha um OR. Ex.: [A, B, [C, D], E]
                            if j in task:
                                token_table['comeco'] -= 1
                                if not ind[j]['out']:
                                    # TODO: checar as relações entre as atividades do conjunto saída
                                    token_table['fim'] += 1
                                else:
                                    token_table[j] = len(ind[j]['out'])
                                parsed += 1
                                break
                        elif task == j:
                            token_table['comeco'] -= 1
                            if not ind[j]['out']:
                                # TODO: checar as relações entre as atividades do conjunto saída
                                token_table['fim'] += 1
                            else:
                                token_table[j] = len(ind[j]['out'])
                            parsed += 1
                            break
                        else:
                            # se o individuo tiver tarefas de inicio, mas nenhuma bater com o começo do log
                            beginPenalty += 1000
                except Exception as e:
                    print(str(e))
        else:
            # se o indivíduo não tiver nenhum começo
            beginPenalty += 9000

        for k in otherTraces:
            for task in ind[k]['in']:
                # caso 1: se uma das posições do input for um OR
                if isinstance(task, list):
                    # print('Caso 2')
                    # print(ind[j]['in'])
                    flag_or = 0

                    for l in task:
                        # se eu achar pelo menos um do input na lista dos possivelmente habilitados
                        if token_table[l] >= 1:
                            parsed += 1
                            flag_or = 1
                            token_table[l] -= 1

                            # habilitando o output da tarefa
                            try:
                                if isinstance(ind[k]['out'][0], list):
                                    # or_enabled.extend(ind[j]['out'][0])
                                    token_table[k] += 1
                                else:
                                    # enabled.extend(ind[j]['out'])
                                    token_table[k] += len(ind[k]['out'])
                            except:
                                continue
                                # print('fimOR1')
                            break

                    # Se não entrar no if, ou seja, nenhuma tarefa do OR estiver habilitada, é aplicada a punição
                    if flag_or == 0:
                        # print('aqui não deveria entrar')
                        # print(penalty,' de penalidade')
                        # penalty += len(ind[j]['in'])
                        penalty += 1
                        parsed += 1
                        # or_enabled = []

                        # habilitando o output da tarefa
                        try:
                            if isinstance(ind[k]['out'][0], list):
                                # or_enabled.extend(ind[j]['out'][0])
                                token_table[k] += 1
                            else:
                                # enabled.extend(ind[j]['out'])
                                token_table[k] += len(ind[k]['out'])
                        except:
                            # print('fimOR2')
                            continue

                # caso o input do evento seja um AND ou uma sequência
                else:
                    # print(ind[j]['in'])
                    aux = 0
                    for m in ind[k]['in']:
                        if token_table[m] >= 1:
                            token_table[m] -= 1
                            aux += 1
                    # print(aux)
                    # Se a penalidade é interpretada simplesmente pela não execução da tarefa propriamente
                    # faz sentido penalizar apenas em 1
                    # penalty += len(ind[j]['in']) - aux
                    if (len(ind[k]['in']) - aux) >= 1:
                        # Se a diferença entre o tamanho de input do and e a qtd de tokens consumidos for maior que 1, penaliza
                        penalty += 1
                    # print(penalty)
                    parsed += 1

                    try:
                        if isinstance(ind[k]['out'][0], list):
                            # or_enabled.extend(ind[j]['out'][0])
                            token_table[k] += 1
                        else:
                            # enabled.extend(ind[j]['out'])
                            token_table[k] += len(ind[k]['out'])
                    except:
                        # print('fimAnd')
                        continue

            '''limpando as variáveis auxiliares'''
        tokens_left.append({i: token_table})

        if penalty == 0:
            parsed_traces += 1

        sum_token_table = sum([m for l, m in token_table.items()])

        if sum_token_table > 0:
            traces_tokens_left += 1

        missing_tokens += penalty
        penalty = 0
        # TODO tirei um [] de token table, só pra registrar se ocorrer algum erro com a variável

    total_len_traces = sum([len(x) for x in traces.values()])
    parsed = total_len_traces - missing_tokens
    # Na formula, no lugar de parsed_traces tem o numero de traços no log menos os que não foram totalmente executados (onde ocorreu
    # punição por faltar tokens. Como eu já tinha calculado o numero de traços executados corretamente, dá na mesma.
    total_left_tokens = 0

    for i in tokens_left:
        for j, val in i.items():
            total_left_tokens += sum([k for j, k in val.items()])

    # print(total_left_tokens, " o total")
    # print(missing_tokens, " punições por não ter o token pra executar")
    punishment = (missing_tokens / (parsed_traces + 1)) + (
        total_left_tokens / (total_traces - traces_tokens_left + 1)) + beginPenalty
    # print(punishment)

    # TODO SOMAR O BEGIN PUNISHMENT E VER SE TÁ FAZENDO DIFERENÇA

    score = ((parsed - punishment) / total_len_traces)
    # Formula do artigo 372: score = (0.4 * (parsed/total_len_traces)) + (0.6 * (parsed_traces/total_traces))
    # score = (0.4 * (parsed / total_len_traces)) + (0.6 * (parsed_traces / total_traces))

    return [score, parsed, total_len_traces, parsed_traces, total_traces, missing_tokens, tokens_left, sum_token_table]


def fitnessLEGACY(ind, traces, alfabeto):
    # token_table = {x: 0 for x in alfabeto}

    token_table = {x: 0 for x in ind.keys()}
    token_table['comeco'] = len(ind['comeco'])
    ##TODO ACRESCENTAR OS TOKENS INICIAIS DE ACORDO COM A RELAÇÃO DO CONJUNTO DE ENTRADA
    tokens_left = []
    # OBS.: Faz sentido zerar a tabela de tokens de um traço pra outro?
    parsed = 0
    # Detalhe p/ depois: os +1 na var 'parsed' são inúteis, já que eu to calculando mais na frente pelas penalidades
    penalty = 0
    missing_tokens = 0
    parsed_traces = 0
    traces_tokens_left = 0
    total_traces = len(traces)

    for i, val in traces.items():
        # Idéia: talvez separar o caso inicial, fazendo um slice no traço de eventos
        # Obs.: Talvez esvaziar o or_enabled não seja uma boa idéia, caso por exemplo sejam acumuladas saídas OR de nós
        # diferentes, esvaziar tudo eliminaria os tokens dos ORs anteriores
        for j in val:
            # pra simplificar, vou considerar que as relações de in/out são 'puras' (OR ou AND/Seq)
            '''
            Val -> traço de eventos
            j -> um evento do atual traço
            '''
            # caso o evento atual seja o inicio - input vazio
            if not ind[j]['in']:
                parsed += 1
                # print('caso 1')
                try:
                    if isinstance(ind[j]['out'][0], list):
                        # print('não devia entrar aqui')
                        # or_enabled.extend(ind[j]['out'][0])
                        token_table[j] += 1
                    else:
                        # print('devia entrar aqui')
                        # enabled.extend(ind[j]['out'])
                        token_table[j] += len(ind[j]['out'])
                except:
                    continue
                    # print('fimSEQ')
                    # enabled.extend(ind[j]['out'])

            # Caso o input do evento atual seja um OR
            elif isinstance(ind[j]['in'][0], list):
                # print('Caso 2')
                # print(ind[j]['in'])
                flag_or = 0

                for k in ind[j]['in'][0]:
                    # se eu achar pelo menos um do input na lista dos possivelmente habilitados
                    if token_table[k] >= 1:
                        # print(k)
                        # print(or_enabled)
                        parsed += 1
                        flag_or = 1
                        # or_enabled = []
                        # or_enabled.remove(k)
                        # print(token_table)
                        token_table[k] -= 1

                        # habilitando o output da tarefa
                        try:
                            if isinstance(ind[j]['out'][0], list):
                                # or_enabled.extend(ind[j]['out'][0])
                                token_table[j] += 1
                            else:
                                # enabled.extend(ind[j]['out'])
                                token_table[j] += len(ind[j]['out'])
                        except:
                            continue
                            # print('fimOR1')
                        break

                # Se não entrar no if, ou seja, nenhuma tarefa do OR estiver habilitada, é aplicada a punição
                if flag_or == 0:
                    # print('aqui não deveria entrar')
                    # print(penalty,' de penalidade')
                    # penalty += len(ind[j]['in'])
                    penalty += 1
                    parsed += 1
                    # or_enabled = []

                    # habilitando o output da tarefa
                    try:
                        if isinstance(ind[j]['out'][0], list):
                            # or_enabled.extend(ind[j]['out'][0])
                            token_table[j] += 1
                        else:
                            # enabled.extend(ind[j]['out'])
                            token_table[j] += len(ind[j]['out'])
                    except:
                        # print('fimOR2')
                        continue

            # caso o input do evento seja um AND ou uma sequência
            else:
                # print(ind[j]['in'])
                aux = 0
                for k in ind[j]['in']:
                    if token_table[k] >= 1:
                        token_table[k] -= 1
                        aux += 1
                # print(aux)
                # Se a penalidade é interpretada simplesmente pela não execução da tarefa propriamente
                # faz sentido penalizar apenas em 1
                # penalty += len(ind[j]['in']) - aux
                if (len(ind[j]['in']) - aux) >= 1:
                    # Se a diferença entre o tamanho de input do and e a qtd de tokens consumidos for maior que 1, penaliza
                    penalty += 1
                # print(penalty)
                parsed += 1

                try:
                    if isinstance(ind[j]['out'][0], list):
                        # or_enabled.extend(ind[j]['out'][0])
                        token_table[j] += 1
                    else:
                        # enabled.extend(ind[j]['out'])
                        token_table[j] += len(ind[j]['out'])
                except:
                    # print('fimAnd')
                    continue

        '''limpando as variáveis auxiliares'''

        if penalty == 0:
            parsed_traces += 1

        sum_token_table = sum([m for l, m in token_table.items()])

        if sum_token_table > 0:
            traces_tokens_left += 1

        missing_tokens += penalty
        penalty = 0
        # TODO tirei um [] de token table, só pra registrar se ocorrer algum erro com a variável
        tokens_left.append({i: token_table})
        token_table = {x: 0 for x in alfabeto}

    total_len_traces = sum([len(x) for x in traces.values()])
    parsed = total_len_traces - missing_tokens
    # Na formula, no lugar de parsed_traces tem o numero de traços no log menos os que não foram totalmente executados (onde ocorreu
    # punição por faltar tokens. Como eu já tinha calculado o numero de traços executados corretamente, dá na mesma.
    total_left_tokens = 0

    for i in tokens_left:
        for j, val in i.items():
            total_left_tokens += sum([k for j, k in val.items()])

    # print(total_left_tokens, " o total")
    # print(missing_tokens, " punições por não ter o token pra executar")
    punishment = (missing_tokens / (parsed_traces + 1)) + (total_left_tokens / (total_traces - traces_tokens_left + 1))
    # print(punishment)

    score = ((parsed - punishment) / total_len_traces)
    # Formula do artigo 372: score = (0.4 * (parsed/total_len_traces)) + (0.6 * (parsed_traces/total_traces))
    # score = (0.4 * (parsed / total_len_traces)) + (0.6 * (parsed_traces / total_traces))

    return [score, parsed, total_len_traces, parsed_traces, total_traces, missing_tokens, tokens_left]


def tournament_selection(populacao):
    try:
        choice = random.choice(len(populacao), 5, False)
        selection = [populacao[x] for x in choice]
        selection = sorted(selection, key=lambda t: t[1])
    except:
        print('deu problema porque: ')
        print(selection)
    return selection[-1]


def crossover1(populacao, crossover_rate, alfabeto):
    # nesse eu não vou bagunçar o interior do I/O ainda, só tratar como um todo
    parent1 = tournament_selection(populacao)
    parent2 = tournament_selection(populacao)
    # copiando os filhos dos pais, sob os quais eu vou operar
    offspring1 = copy.deepcopy(parent1)
    offspring2 = copy.deepcopy(parent2)
    if random.random() <= crossover_rate:
        # Selecionando a tarefa de cada pai que será trabalhada no crossover
        task_name = random.choice(alfabeto, 1)[0]
        off1_task = copy.deepcopy(offspring1[0][task_name])
        off2_task = copy.deepcopy(offspring2[0][task_name])

        # Limpando a tarefa em questão do próprio filho
        # TODO: depois testar se tirando essa atribuição, dá o mesmo resultado (altera o offspring passado como argumento)
        offspring1[0] = update_elements(offspring1[0], off1_task, task_name, 'remove')
        offspring2[0] = update_elements(offspring2[0], off2_task, task_name, 'remove')

        # Fazendo o crossover da tarefa e ajeitando o cromossomo
        # TODO Trocar os conjuntos de in/out entre as tarefas
        offspring1[0] = update_elements(offspring1[0], off2_task, task_name, 'add')
        offspring2[0] = update_elements(offspring2[0], off1_task, task_name, 'add')

        offspring1[0][task_name] = off2_task
        offspring2[0][task_name] = off1_task

        correct_elements(offspring1[0])
        correct_elements(offspring2[0])

        # Recalculando o fitness
        ''' TEM QUE SER CALCULADO FORA, POR CAUSA DA NECESSIDADE DE PASSAR OS LOGS PRA FUNÇÃO FITNESS'''
        # offspring1[1] = fitness(offspring1[0], logTraces, alfabetoTarefas)
        offspring1[1] = 0
        offspring2[1] = 0

        ### preenchendo os inicios e fins do processo dos filhos
        comeco1 = []
        fim1 = []
        for p, val in offspring1[0].items():
            if p not in ['comeco', 'fim']:
                if not val['in']:
                    comeco1.append(p)
                if not val['out']:
                    fim1.append(p)

        offspring1[0]['comeco'] = comeco1
        offspring1[0]['fim'] = fim1

        comeco2 = []
        fim2 = []
        for q, val in offspring2[0].items():
            if q not in ['comeco', 'fim']:
                if not val['in']:
                    comeco2.append(q)
                if not val['out']:
                    fim2.append(q)

        offspring2[0]['comeco'] = comeco2
        offspring2[0]['fim'] = fim2
    else:
        # Cria novos individuos se o crossover não ocorrer
        alfabeto = parent1[0].keys()
        alfabeto = list(alfabeto)
        alfabeto.remove('comeco')
        alfabeto.remove('fim')

        offspring1 = [ind.criarIndividuo(alfabeto), 0]
        offspring2 = [ind.criarIndividuo(alfabeto), 0]

    return [offspring1, offspring2]


def mutationA(individuo, mutation_rate):
    # Mutação mais agressiva, se ocorrer a mutação na tarefa, ocorre pra Input e Output da mesma

    for i, val in individuo.items():
        if (random.random() <= mutation_rate):
            # Mutando o INPUT
            try:
                if len(val['in'] > 1):
                    if isinstance(val['in'][0], list):
                        # if it's a xOR, it becomes a AND
                        val['in'] = val['in'][0]
                    else:
                        # if it's a AND, it becomes a xOR
                        val['in'] = [val['in']]

                if len(val['out'] > 1):
                    if isinstance(val['out'][0], list):
                        val['out'] = val['out'][0]
                    else:
                        val['out'] = [val['out']]

            except:
                if i in ('comeco', 'fim'):
                    if len(individuo[i]) > 1:
                        try:
                            if isinstance(individuo[i][0], list):
                                individuo[i] = individuo[i][0]
                            else:
                                individuo[i] = [individuo[i]]
                        except Exception as e:
                            print(e)
                            print('Erro na mutação do inicio/fim do individuo')

    correct_elements(individuo)
    return individuo


def mutationB(individuo, mutation_rate):
    # Mutação menos agressiva, se ocorrer a mutação na tarefa, pode ocorrer pra Input ou Output, nos dois ou em nenhum

    for i, val in individuo.items():
        if (random.random() <= mutation_rate):
            # Mutando o INPUT
            try:
                if len(val['in'] > 1):
                    if isinstance(val['in'][0], list):
                        # if it's a xOR, it becomes a AND
                        if random.random() <= 0.5:
                            val['in'] = val['in'][0]
                    else:
                        # if it's a AND, it becomes a xOR
                        if random.random() <= 0.5:
                            val['in'] = [val['in']]

                if len(val['out'] > 1):
                    if isinstance(val['out'][0], list):
                        if random.random() <= 0.5:
                            val['out'] = val['out'][0]
                    else:
                        if random.random() <= 0.5:
                            val['out'] = [val['out']]

            except:
                if i in ('comeco', 'fim'):
                    if len(individuo[i]) > 1:
                        try:
                            if isinstance(individuo[i][0], list):
                                if random.random() <= 0.5:
                                    print(individuo[i], 'OR')
                                    individuo[i] = individuo[i][0]
                                    print(individuo[i], 'AND')
                                    #just to see if there's any 'xOR' end laying somewhere in my code
                            else:
                                if random.random() <= 0.5:
                                    individuo[i] = [individuo[i]]

                        except Exception as e:
                            print(e)
                            print('Erro na mutação do inicio/fim do individuo')

    correct_elements(individuo)
    return individuo


def correct_elements(individuo):
    for i, val in individuo.items():

        if i not in ['comeco', 'fim']:
            if val['in']:
                if len(val['in'][0]) <= 1:
                    individuo[i]['in'] = val['in'][0]
            if val['out']:
                if len(val['out'][0]) <= 1:
                    individuo[i]['out'] = val['out'][0]

        else:
            if individuo[i]:
                if len(individuo[i][0]) <= 1:
                    individuo[i] = individuo[i][0]

                    # return individuo
                    # aparently there's no need to return the value, i'm altering the structure directly


def update_elements(individuo, task_set, task_name, operacao):
    if operacao == 'remove':
        # Rotina pra remover a tarefa do input e output das relacionadas
        # task = individuo[tarefa]

        try:
            for j in task_set['in']:
                if isinstance(j, list):
                    for k in j:
                        if k != task_name:
                            try:
                                if isinstance(individuo[k]['out'][0], list):
                                    individuo[k]['out'][0].remove(task_name)
                                else:
                                    individuo[k]['out'].remove(task_name)
                            except IndexError as e:
                                print('valor já apagado/não existe1')
                                print(e)
                else:
                    if j != task_name:
                        try:
                            if isinstance(individuo[j]['out'][0], list):
                                individuo[j]['out'][0].remove(task_name)
                            else:
                                individuo[j]['out'].remove(task_name)
                        except IndexError as e:
                            print('valor já apagado/não existe2')
                            print(e)
        except:
            print('conjunto vazio na entrada')

        try:
            for j in task_set['out']:
                if isinstance(j, list):
                    for k in j:
                        if k != task_name:
                            try:
                                if isinstance(individuo[k]['in'][0], list):
                                    individuo[k]['in'][0].remove(task_name)
                                else:
                                    individuo[k]['in'].remove(task_name)
                            except IndexError:
                                print('valor já apagado/não existe')
                else:
                    if j != task_name:
                        try:
                            if isinstance(individuo[j]['in'][0], list):
                                individuo[j]['in'][0].remove(task_name)
                            else:
                                individuo[j]['in'].remove(task_name)
                        except IndexError:
                            print('valor já apagado/não existe')
        except:
            print('conjunto vazio')
        individuo[task_name]['in'] = []
        individuo[task_name]['out'] = []


    elif operacao == 'add':
        # TODO adicionar um try except pra não dar erro em conjuntos vazios de in/out
        for i in task_set['in']:
            if isinstance(i, list):
                for j in i:
                    if j != task_name:
                        # TODO: aqui eu to tratando como se o conjunto a ser inserido fosse puro OR ou AND, depois tratar os casos mistos
                        try:
                            if isinstance(individuo[j]['out'][0], list):
                                individuo[j]['out'][0].append(task_name)
                            else:
                                individuo[j]['out'].append(task_name)
                        except IndexError:
                            individuo[j]['out'].append(task_name)
            else:
                if i != task_name:
                    try:
                        if isinstance(individuo[i]['out'][0], list):
                            individuo[i]['out'][0].append(task_name)
                        else:
                            individuo[i]['out'].append(task_name)
                    except IndexError:
                        individuo[i]['out'].append(task_name)

        for k in task_set['out']:
            if isinstance(k, list):
                for l in k:
                    if l != task_name:
                        # TODO: aqui eu to tratando como se o conjunto a ser inserido fosse puro OR ou AND, depois tratar os casos mistos
                        try:
                            if isinstance(individuo[l]['in'][0], list):
                                individuo[l]['in'][0].append(task_name)
                            else:
                                individuo[l]['in'].append(task_name)
                        except IndexError:
                            individuo[l]['in'].append(task_name)

            else:
                if k != task_name:
                    try:
                        if isinstance(individuo[k]['in'][0], list):
                            individuo[k]['in'][0].append(task_name)
                        else:
                            individuo[k]['in'].append(task_name)
                    except IndexError:
                        individuo[k]['in'].append(task_name)

                        # individuo[task_name] = task_set
                        # Vou fazer isso no próprio crossover, faz mais sentido

    else:
        print('operação não definida')

    return individuo  # Pra efeitos didáticos, pois o python altera o indivíduo original passado, sem necessidade de reatribuir esse retorno ao original
