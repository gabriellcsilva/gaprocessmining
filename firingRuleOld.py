def firingRule(individuo, logs):
    vetor_tabelas = {}
    dict_variaveis = {'parsed_all':0, 'parsed_traces_all':0, 'missing_tokens_all':0, 'traces_tokens_left_all':0, 'soma_tabela_tokens_all':0, 'penal_ini_all':0, 'penal_fim_all':0}

    for h, traco in logs.items():

        tabela_token = {x: 0 for x in individuo.keys()}
        comeco = len(individuo['comeco'])
        tabela_token['comeco'] = comeco

        parsed = 0
        missing_tokens = 0
        parsed_trace = 0
        trace_tokens_left = 0
        penal_ini = 0
        penal_fim = 0

        comeco_log = traco[:comeco]
        resto_log = traco[comeco:]

        '''OBS.: Não faz sentido um slice pro fim do processo, simplesmente deve-se pegar o conjunto de fim e ver se tem tokens suficientes no fim pra fechar a execução'''

        ####    TRATANDO O COMECO   ####
        try:
            if isinstance(individuo['comeco'][0], str):
                conj_comeco = individuo['comeco']
            else:
                conj_comeco = individuo['comeco'][0]

            for i in comeco_log:
                if i in conj_comeco:
                    if tabela_token['comeco'] >= 1:
                        # caso de execução perfeito - a task está no conjunto de começo e está habilitada pra executar
                        #provavelmente não precisa desse if. Se a tarefa tá no começo, tem token pra ela (e comecoLog é no maximo do tamanho da qtd de tokens de inicio)
                        tabela_token['comeco'] -= 1
                        parsed += 1
                    else:
                        print("teste pra ver se existem casos onde a tarefa está no começo, mas não há tokens pra executar")
                        print("se acontecer esse caso, acrescer 1 na var penalidade")

                else:
                    # caso a tarefa não esteja no começo
                    penal_ini += 1000
                    missing_tokens += len(individuo[i]['in'])
                # criando os tokens para as tafefas do conjunto de saída
                if not individuo[i]['out']:
                    #caso a tarefa vá pro fim do processo (conjunto de saída vazio)
                    tabela_token['fim'] += 1
                else:
                    tabela_token[i] += len(individuo[i]['out'])

        except:
            #print(str(individuo['comeco']))
            #print(individuo)
            #exit()
            penal_ini += 10000000000
            #TODO: Tem mais algo pra tratar aqui? nesse caso o indivíduo provavelmente não tem nenhum inicio

        ####    TRATANDO O RESTO DO LOG    ####

        for j in resto_log:
            #print(tabela_token)
            #print('j', j)
            try:
                if isinstance(individuo[j]['in'][0], str):
                    #se for um AND
                    flag_pen_AND = 0
                    for k in individuo[j]['in']:
                        #pra cada atividade no conjunto de entrada (pré-requisitos)
                        if tabela_token[k] >= 1:
                            #todas as tarefas k tem que ter um token, se ao menos uma não tiver, j não é executada corretamente (penalidade+1)
                            tabela_token[k] -= 1
                        else:
                            #print('k',k)
                            #print('token de k', tabela_token[k] )
                            flag_pen_AND += 1

                    if flag_pen_AND == 0:
                        parsed += 1
                    else:
                        missing_tokens += flag_pen_AND
                        #print('aqui1')

                elif isinstance(individuo[j]['in'][0], list):
                    #se for um xOR
                    flag_pen_OR = 1
                    for k in individuo[j]['in'][0]:
                        if tabela_token[k] >= 1:
                            tabela_token[k] -= 1
                            flag_pen_OR = 0
                            break
                    if flag_pen_OR == 0:
                        parsed += 1
                    else:
                        missing_tokens += 1

                # criando os tokens pro conjunto de saída da atividade j
                if not individuo[j]['out']:
                    #caso a tarefa vá pro fim do processo (conjunto de saída vazio)
                    tabela_token['fim'] += 1
                else:
                    tabela_token[j] += len(individuo[j]['out'])
            except:
                #### Exceção que dispara se houver uma tarefa com input vazio (tarefa de 'início') durante a semântica de execução - na etapa do resto do log #####
                penal_ini +=1000

                if not individuo[j]['out']:
                    #caso a tarefa vá pro fim do processo (conjunto de saída vazio)
                    tabela_token['fim'] += 1
                else:
                    tabela_token[j] += len(individuo[j]['out'])

            #if j == 'A2': DEBUG
            #    print(tabela_token)

        #print(tabela_token)
        #### Lidando com o fim do processo
        try:
            if isinstance(individuo['fim'][0], str):
                if tabela_token['fim'] == len(individuo['fim']):
                    tabela_token['fim'] = 0

                else:
                    penal_fim += 1000

            elif isinstance(individuo['fim'][0], list):
                if tabela_token['fim'] == 1:
                    tabela_token['fim'] = 0
                else:
                    penal_fim += 1000
        except:
            #print(str(individuo['fim']))
            penal_fim += 10000000000

        #### Algumas variáveis pro cálculo do fitness #####

        if missing_tokens == 0:
            parsed_trace += 1

        soma_tabela_tokens = sum([m for l, m in tabela_token.items()])

        if soma_tabela_tokens > 0:
            trace_tokens_left += 1

        vetor_tabelas.update({h: [tabela_token, parsed, parsed_trace, missing_tokens, trace_tokens_left, soma_tabela_tokens, penal_ini, penal_fim]})
        dict_variaveis['parsed_all']+= parsed
        dict_variaveis['parsed_traces_all'] += parsed_trace
        dict_variaveis['missing_tokens_all'] += missing_tokens
        dict_variaveis['traces_tokens_left_all'] += trace_tokens_left
        dict_variaveis['soma_tabela_tokens_all'] += soma_tabela_tokens
        dict_variaveis['penal_ini_all'] += penal_ini
        dict_variaveis['penal_fim_all'] += penal_fim

    return [vetor_tabelas,dict_variaveis]

'''
def fitnessNew(individuo, logs):
    resultado = firingRule(individuo, logs)
    variaveis = resultado[-1]
    total_len_traces = sum([len(x) for x in logs.values()])
    total_traces = len(logs)

    # Na formula, no lugar de parsed_traces tem o numero de traços no log menos os que não foram totalmente executados (onde ocorreu
    # punição por faltar tokens. Como eu já tinha calculado o numero de traços executados corretamente, dá na mesma.


    punishment = (variaveis['missing_tokens_all'] / (variaveis['parsed_traces_all'] + 1)) + \
                 (variaveis['soma_tabela_tokens_all'] / (total_traces - variaveis['traces_tokens_left_all'] + 1)) +\
                 variaveis['penal_ini_all'] + variaveis['penal_fim_all']
    # print(punishment)

    # TODO SOMAR O BEGIN PUNISHMENT E VER SE TÁ FAZENDO DIFERENÇA

    score = ((variaveis['parsed_all'] - punishment) / total_len_traces)
    # Formula do artigo 372: score = (0.4 * (parsed/total_len_traces)) + (0.6 * (parsed_traces/total_traces))
    # score = (0.4 * (parsed / total_len_traces)) + (0.6 * (parsed_traces / total_traces))

    return [score, resultado]
'''