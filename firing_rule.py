# Script that contains all functions that perform the firing semantics for petrinets (causal matrixes)

def firingRule(individuo, logs):
    vetor_tabelas = {}

    # Initializing some variables to measure the good execution of the process
    dict_variaveis = {'parsed_all':0,
                      'parsed_traces_all':0,
                      'missing_tokens_all':0,
                      'traces_tokens_left_all':0,
                      'soma_tabela_tokens_all':0,
                      'penal_ini_all':0,
                      'penal_fim_all':0,}

    for trace_id, trace in logs.items():

        tabela_token = {task: [] for task in individuo.keys()}

        # Defining the number of tokens to begin the process
        '''instead of doing like this, i'll just put the whole begin condition in the table no matter what it is
        and here i'll just decide the lenght of the initial portion of the log'''

        if individuo['inicio'][0][0] == 'xOR':
            lenght_inicio = 1
        elif individuo['inicio'][0][0] == 'AND':
            lenght_inicio = len(individuo['inicio'][1])
        else:
            print('failure on determining initial lenght of log to begin process')
        '''OBS.: Não faz sentido um slice pro fim do processo, simplesmente deve-se pegar o conjunto de fim e ver se tem
                 tokens suficientes no fim pra fechar a execução'''
        inicio_log = trace[:lenght_inicio]
        resto_log = trace[lenght_inicio:]

        # Initializing the tokens in the beggining
        inicio = individuo['inicio'][:]
        tabela_token['inicio'].append(inicio)
        # tabela_token['inicio'][:] = individuo['inicio'][:] see if this works (Nope)
        # For some reason, the tabela_token and individuo are sharing references for the same objects

        parsed = 0
        missing_tokens = 0
        parsed_trace = 0
        trace_tokens_left = 0
        penal_ini = 0
        penal_fim = 0

        ####    TRATANDO O COMECO   ####
        try:
            # No need to differentiate AND and xOR here, the inicio_log will have only the right amount of events for
            # each case
            for i in inicio_log:
                # in the xOR case, it will only do one check and exit. If not, penalized.
                # in the AND case, if one of the tasks on the inicio_log isn't on the beginning set, it'll be penalized
                # progressively
                if i in tabela_token['inicio'][0][1]:
                    # obs.: Could i just call the input function i made instead of doing this?
                    # TODO already created the empty input case inside of the function, now need to see if makes sense
                    parsed += 1
                    #print(tabela_token['inicio'])
                    tabela_token['inicio'][0][1] = [foo for foo in tabela_token['inicio'][0][1] if foo != i ]
                    # print(tabela_token['inicio'])
                    # print(individuo['inicio'])
                    # exit()

                else:
                    # In case the task isn't in the begining of the individual
                    # this is the case if nothing is parsed
                    # in the case of a and, the accumulated penal_ini will be enough
                    penal_ini += 1000
                    # Penalizing for the worst case, assuming there's a AND of ANDs (so the total of missing tokens is
                    # the length of ['in'][1] and [2]
                    missing_tokens += sum(len(f) for f in individuo[i]['in'][1:])

                # criando os tokens para as tafefas do conjunto de saída
                if not individuo[i]['out'][0]:
                    #caso a tarefa vá pro fim do processo (conjunto de saída vazio)
                    tabela_token['fim'].append(i)
                else:
                    #For now, i'll just put them entirely
                    tabela_token[i].append(individuo[i]['out'][:])

            # checking to delete the condition if one task of the xOR was exec or if the AND was complete.
            if parsed >= 1 and tabela_token['inicio'][0][0][0] == 'xOR':
                #Remove the xOR initial condition and stuff
                del tabela_token['inicio'][0]

            elif parsed >= 1 and not tabela_token['inicio'][0][1]:
                #if it's an AND and every task was executed, remove the empty structure
                del tabela_token['inicio'][0]

                #print(individuo['inicio'], 'to aqui')
                #break

        except Exception as exept:
            #print(str(individuo['comeco']))
            #print(individuo)
            #exit()
            print(exept)
            penal_ini += 10000000
            #TODO: Tem mais algo pra tratar aqui? nesse caso o indivíduo provavelmente não tem nenhum inicio

        ####    TRATANDO O RESTO DO LOG    ####

        for j in resto_log:
            #here i use the input function i created to deal with the simple & complex inputs
            #basically what it does here is passing the task name i'm looking for, the task's input and the token table
            #where i'll look in for tokens to parse the given task

            result = logicInput(tabela_token,individuo[j]['in'],j)
            #updating the table after i tried to parse the task
            tabela_token = result[2]

            # TODO put some ifs when testing, to make sure every variable is working as expected (specially between them)
            # TODO like, if result[1] is 1, then result[0] should have 0 tokens missing

            #if the task is parsed, this will add +1 to parsed, if not parsed, +0
            parsed += result[1]
            #if parsed, missing tokens will be added +0, but if not, the value of result[0] is the # of missing tokens
            missing_tokens += result[0]

            #Adding the output, dealing with the special case (fim)
            if not individuo[j]['out'][0]:
                tabela_token['fim'].append(j)
            else:
                tabela_token[j].append(individuo[j]['out'][:])

            # TODO End of the middle section of the log. If needed, i'll put a try/except to handle with begin tasks that
            # TODO eventually find their way to here (they shoudn't). I can do it inside the Input function, or filter it
            # TODO here with a if statement

        # Dealing with the process's end
        try:
            # Like the beginning, the end only have simple logic structures, so there's just two cases here
            miss_end_tokens = 0
            if individuo['fim'][0][0] == "AND":
                for i in individuo['fim'][1]:
                    if i in tabela_token['fim']:
                        #print(tabela_token['fim'], 'tktable and antes')
                        tabela_token['fim'] = [_ for _ in tabela_token['fim'] if _ != i]
                        #print(tabela_token['fim'], 'tktable and depois')
                    else:
                        miss_end_tokens += 1
                if not miss_end_tokens:
                    parsed += 1
                else:
                    missing_tokens += miss_end_tokens

            elif individuo['fim'][0][0] == "xOR":
                for j in individuo['fim'][1]:
                    if j in tabela_token['fim']:
                        #print(tabela_token['fim'], 'tktable xor antes')
                        tabela_token['fim'] = []
                        #print(tabela_token['fim'], 'tktable xor depois')
                        end_parsed = 1
                        break
                if end_parsed == 1:
                    parsed += 1
                else:
                    missing_tokens += 1
            else:
                print('Mistakes were made here...')


        except Exception as e:
            # Probably only happens if the individual doesn't have an ending
            print(e)
            penal_fim += 10000000

        # Some variables for the fitness calcs.
        # if there was no single missing token during all the trace execution, i consider the trace parsed
        if missing_tokens == 0:
            parsed_trace += 1

        # Estimating # of tokens in the table. Since some structures are more complex, i'll just add the amount of tasks
        # in both task sets, no matter what the logic set says
        # fim_set is the ending of the process, i separate it to avoid some inconsistencies with len()
        aux_table_token = tabela_token.copy()
        fim_set = aux_table_token.pop('fim')
        # That's a "double" comprehension, the structure is this:
        # [ (statement) (optional(if statement else statement) (outter for loop (inner for loop)) ]
        # basically, the if separates complex structures from simple ones, so i know what index to apply len()
        aux_sum_table = [len(j[2]) + len(j[1]) if len(j[0]) == 3 else len(j[-1]) for i in aux_table_token.values() for j in i]
        sum_token_table = sum(aux_sum_table) + len(fim_set)

        if sum_token_table > 0:
            trace_tokens_left += 1

        # Wrapping everything in variables to return
        vetor_tabelas.update({trace_id: [tabela_token, parsed, parsed_trace, missing_tokens, trace_tokens_left,
                                  sum_token_table, penal_ini, penal_fim]})
        #Summing everything
        dict_variaveis['parsed_all'] += parsed
        dict_variaveis['parsed_traces_all'] += parsed_trace
        dict_variaveis['missing_tokens_all'] += missing_tokens
        dict_variaveis['traces_tokens_left_all'] += trace_tokens_left
        dict_variaveis['soma_tabela_tokens_all'] += sum_token_table
        dict_variaveis['penal_ini_all'] += penal_ini
        dict_variaveis['penal_fim_all'] += penal_fim

    return [vetor_tabelas, dict_variaveis]

def searchTable(task, index_tabela_token):
    #input of this function is the name of the task being searched, and not the whole table but only the index where
    # i'm looking
    #this will implement the logic to know when to delete a logic set, especially when dealing with complex xORs
    bool_parsed = False
    for token_logic_str in index_tabela_token:
        # case 1: if the token logic structure is a simple AND or xOR
        if len(token_logic_str) == 2:
            # if the task is in the token structure
            if task in token_logic_str[1]:
                # if i found a token in the simple struct, i set the bool to true
                bool_parsed = True
                # case 1.1 - it's an AND
                if token_logic_str[0][0] == 'AND':
                    # delete only the token for the task, and keep the rest of the struct.
                    #token_logic_str[1].remove(task)
                    #print(index_tabela_token, 'tabela no indice x, antes')
                    token_logic_str[1] = [task_aux for task_aux in token_logic_str[1] if task_aux != task]
                    # the case when i removed a token from an AND that had only one last token
                    if not token_logic_str[1]:
                        # then i delete the whole structure from the list of token structures
                        index_tabela_token.remove(token_logic_str)

                    #print(index_tabela_token, 'tabela no indice x, depois')

                # case 1.2 - it's an xOR
                else:
                    #print(index_tabela_token)
                    #print(index_tabela_token, 'tabela no indice x, antes')
                    # delete the whole xOR structure, since the token goes for the task parsed first
                    index_tabela_token.remove(token_logic_str)
                    #print(index_tabela_token, 'tabela no indice x, depois')

                # since i found a token in the simple struct, i break the for loop
                break
            else:
                # the case if the structure doesn't have the token needed, dunno if should penalize already here
                # (prob not)
                continue

        #case 2: the structure is a complex one
        elif len(token_logic_str) == 3:
            #checking if it is in the left leaf structure
            if task in token_logic_str[1]:
                #make a recursive call. this keeps me from having to rewrite the simple cases again here
                sub_table_list1 = [[[token_logic_str[0][1]], token_logic_str[1]]]
                subsearch_1 = searchTable(task, sub_table_list1)
                #if it's in the structure, i set the bool to True (parsed)
                bool_parsed = True

                # if the root node is a AND, the recursive call will have already decided if this leaf was a AND or xOR
                # and will already have deleted the token accordingly
                if token_logic_str[0][0] == 'AND':
                    # if the leaf returned a empty token list (either was the last token in a AND or it was a xOR)
                    if not subsearch_1[1]:
                        # checking if the second set is empty too
                        if not token_logic_str[2]:
                            index_tabela_token.remove(token_logic_str)
                        # if not, i just empty the current side
                        else:
                            token_logic_str[1] = []

                    # if the leaf was a AND that had more than one token
                    else:
                        #the subsearch_1[1][0][1]: [1] - last position of the searchTable output. [0] - the first
                        #position of that list (is a list of token structs, but this only have one struct since i
                        #derivated it in the recursive call. [1] - the last index on the structure i got, the one
                        #who has the set of tasks. TL;DR - this updates the task set minus the consumed token
                        token_logic_str[1] = subsearch_1[1][0][1]

                # if the root is a xOR, then i must deal with it thoroughly. in this case, if the root is a xOR and
                # the leaf is also a xOR, i won't add it back in the token list as a simple token struct
                elif token_logic_str[0][0] == 'xOR':
                    # if the leaf returned a empty token list (either was the last token in an AND or it was a xOR)
                    if not subsearch_1[1]:
                        index_tabela_token.remove(token_logic_str)
                    # if it returned a AND that had more tokens to it
                    else:
                        # by my logic this generates a simple AND
                        # then, instead of keeping the complex structure, i add the derivated AND to the list
                        index_tabela_token.append(subsearch_1[1][0])

            # if the token was on the second leaf - task set
            elif task in token_logic_str[2]:
                # make a recursive call
                sub_table_list2 = [[[token_logic_str[0][2]], token_logic_str[2]]]
                subsearch_2 = searchTable(task, sub_table_list2)
                # since it is in the second set, i mark the bool as True(parsed)
                bool_parsed = True

                # if the root node is a AND, the recursive call will have already decided if this leaf was a AND or xOR
                # and will already have deleted the token accordingly
                if token_logic_str[0][0] == 'AND':
                    # if the leaf returned a empty token list (either was the last token in a AND or it was a xOR)
                    if not subsearch_2[1]:
                        # i test to see if the other leaf is empty too
                        if not token_logic_str[1]:
                            # then it means i can delete, there's no more tokens on the structure
                            index_tabela_token.remove(token_logic_str)
                        # if not, i just empty the current leaf
                        else:
                            token_logic_str[2] = []

                    # if the leaf was a AND that had more than one token
                    else:
                        # the subsearch_2[1][0][1]: [1] - last position of the searchTable output. [0] - the first
                        # position of that list (is a list of token structs, but this only have one struct since i
                        # derivated it in the recursive call. [1] - the last index on the structure i got, the one
                        # who has the set of tasks. TL;DR - this updates the task set minus the consumed token
                        token_logic_str[2] = subsearch_2[1][0][1]

                # if the root is a xOR, then i must deal with it thoroughly. in this case, if the root is a xOR and
                # the leaf is also a xOR, i won't add it back in the token list as a simple token struct
                elif token_logic_str[0][0] == 'xOR':
                    # if the leaf returned a empty token list (either was the last token in an AND or it was a xOR)
                    if not subsearch_2[1]:
                        index_tabela_token.remove(token_logic_str)
                    # if it returned a AND that had more tokens to it
                    else:
                        # by my logic this generates a simple AND
                        # then, instead of keeping the complex structure, i add the derivated AND to the list
                        index_tabela_token.append(subsearch_2[1][0])

            else:
                # in case it's not in the current structure
                continue

    # if there was not a single struct with the token i'm looking for, it will leave the bool_parsed with a False value
    return [bool_parsed, index_tabela_token]

def logicInput(tabela_token, task_input, task):
    # OBS.: The task_input is the same as if i used 'indiv[task]['in']'
    # I'm doing this because of the recursivity, if i keep using the immutable structure of the individual i can't
    # break the complex inputs to more simplistic ones.
    missing_tokens = 0
    parsed = 0

    # Case 0: a beggining task was found in the middle of the parsing
    # A penal_ini would have been applied if a non beginning task was executed before the begin ones, so this will
    # either add a parsed task or a missing token, and possibly a few unused tokens to be left
    if not task_input[0]:

        # print(task_input, task, tabela_token)
        result = searchTable(task, tabela_token['inicio'])
        if result[0] is True:
            parsed = 1
        else:
            missing_tokens = 1
        # print(task_input, task, tabela_token)

    # Case 1: if the input condition is a simple AND or xOR
    elif len(task_input[0]) == 1:
        # just for readability
        logic_op = task_input[0][0]
        # Case 1.1 - simple & AND
        if logic_op == 'AND':
            for x in task_input[1]:
                result = searchTable(task, tabela_token[x])
                # updating the token table on the 'x' index
                #tabela_token[x] = result[1] nem precisa, aparentemente eu compartilhei só uma referencia
                # if there wasn't a token on that x's token list
                if result[0] is False:
                    missing_tokens += 1
            if missing_tokens == 0:
                # only is parsed if no missing token was created
                parsed += 1

        # Case 1.2 - simple & xOR
        elif logic_op == 'xOR':

            parsed_xor = 0
            for x in task_input[1]:
                result = searchTable(task, tabela_token[x])
                # updating the token table on the 'x' index
                #tabela_token[x] = result[1] nem precisa, aparentemente eu compartilhei só uma referencia
                # if there was at least one token
                if result[0] is True:
                    # only 1 token is necessary to parse
                    parsed_xor += 1
                    break

            if parsed_xor == 0:
                # only misses if not a single token was found. only one, since one is the least needed
                missing_tokens = 1
            else:
                parsed = parsed_xor


    # Case 2: if the input is complex
    elif len(task_input[0]) == 3:
        # Special case, when one of the leafs in the input is empty but the structure is complex'''
        root_logic_op = task_input[0][0]
        if not task_input[1] or not task_input[2]:
            # here i simply use a comprehension to pick only the non empty side of the struct
            simplified_input = [[task_input[0][1]],task_input[1]] if not task_input[2] else [[task_input[0][2]],task_input[2]]
            simp_result = logicInput(tabela_token, simplified_input, task)
            # if the result is positive
            if simp_result[1] == 1:
                parsed = 1
                missing_tokens = 0
            else:
                parsed = 0
                missing_tokens = simp_result[0]

        # case 2.1: the root logic op is a AND
        elif root_logic_op == 'AND':
            # this gets the first logic leaf and the first task list
            # TODO maybe there's a missing or extra [] in this subinput, like what was happening in the SUBSEARCHS
            sub_input1 = [[task_input[0][1]],task_input[1]]
            subresult_1 = logicInput(tabela_token, sub_input1, task)
            # this is needed in order to keep the table consistant between the two recursive calls
            tabela_token = subresult_1[2]
            # and this gets the second leaf and tasks
            sub_input2 = [[task_input[0][2]],task_input[2]]
            subresult_2 = logicInput(tabela_token, sub_input2, task)
            #Now doing the root AND
            #basically i'm testing if the variable parsed was set 1 in both (successful)
            if subresult_1[1] == 1 and subresult_2[1] == 1:
                missing_tokens = 0
                parsed = 1
            else:
                missing_tokens = subresult_1[0] + subresult_2[0]
                parsed = 0
            # then i update the token table no matter what
            tabela_token = subresult_2[2]

        # Case 2.2: the root logic op is a xOR
        elif root_logic_op == 'xOR':
            # this gets the first logic leaf and the first task list
            sub_input1 = [[task_input[0][1]], task_input[1]]
            subresult_1 = logicInput(tabela_token, sub_input1, task)
            ''' TODO do i need to pass the modified tabela_token? cuz i still modify it if there was a AND where some of
            it's tasks weren't parsed, but since the root node is a XOR, for now i'm passing the intact table
            to the next leaf node. Maybe ask Fantinato'''
            if subresult_1[1] == 1:
                # the case when it parsed
                parsed = 1
                missing_tokens = 0
                tabela_token = subresult_1[2]

            else:
                # If it didn't parse, i try the second leaf node
                sub_input2 = [[task_input[0][2]], task_input[2]]
                subresult_2 = logicInput(tabela_token, sub_input2, task)

                if subresult_2[1] == 1:
                    # the case when it parsed
                    parsed = 1
                    missing_tokens = 0
                else:
                    # the last case, when neither parsed
                    parsed = 0
                    missing_tokens = subresult_1[0] + subresult_2[0]
                # No matter if it parses or not, i return the altered tabeka_token of the last try
                tabela_token = subresult_2[2]

    return [missing_tokens, parsed, tabela_token]

