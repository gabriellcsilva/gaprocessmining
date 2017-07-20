import numpy as np
# import collections as col
'''Note to myself: I reused the same search_table and logic_input from firingRule, just changed the names a bit and
changed the variable names to keep the readability in this context'''

def trace_maker (individuo, max_len_trace):
    # This is the main routine that builds the log trace
    # 'trace' keeps the log trace so far, so i go inserting the executed tasks on it while this function runs
    trace = []

    # 'active_tokens' is a list with token logic structures that are the output of a previously executed task
    # TODO i changed it to a dict, to avoid making a token table with every entry. maybe that has consequences to the
    # TODO code...
    active_tokens = {}

    # 'tasks_to_exec' is a scheduler that has a list of tasks to be executed. Denotes the tasks that were enabled by a
    # token logic structure that was chosen in the 'choice_maker' function
    # Obs.: A list keeps insertion order, but a dict doesn't necessarily
    tasks_to_exec = []

    # For now i won't use a token table, apparently would be unnecessary
    # token_table = {x: [] for x in individuo.keys()}

    # Here i begin the trace-making cycle, adding the tokens for the beginning tasks
    active_tokens['inicio'] = individuo['inicio'][:]

    # This is the main loop that builds the trace, it keeps running until active_tokens has no  more token structures
    # or until the 'max_len_trace' has reached zero (to keep from infinite loops)
    while active_tokens and max_len_trace > 0:
        max_len_trace -= 1
        # Choosing one structure on 'active_tokens' to begin the building process
        choice = np.random.choice(active_tokens.keys(), 1, False)
        # Calling the 'choice_maker' routine and extending its output to 'tasks_to_exec's end
        # TODO maybe there's a problem here, because 'choice' is a ndarray
        tasks_to_exec.extend(choice_maker(active_tokens[choice]))

        # This will call the function that searches tokens, in the order that the tasks were added to 'tasks_to_exec'
        for i in tasks_to_exec:
            result = logic_input(i, individuo[i], active_tokens)
            if result[0] is True:
                # TODO these indexes are just mock right now, i'll still define which values to return
                # I append the task as executed in the trace
                trace.append(i)
                # and then add the output of the task to the active_tokens
                if not individuo[i]['out']:
                    # TODO code to add tokens for the ending of the process
                    continue
                else:
                    active_tokens[i] = individuo[i]['out'][:]

    # FINALIZING THE TRACE
    # TODO deal with the end of the process (possibly)
    # TODO like, if max len trace is = 0 or if active tokens is zeroed, then try to execute the end... think about it

    return trace


def search_table(task, index_active_token):
    #input of this function is the name of the task being searched, and not the whole table but only the index where
    # i'm looking
    #this will implement the logic to know when to delete a logic set, especially when dealing with complex xORs
    bool_parsed = False
    for token_logic_str in index_active_token:
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
                    #print(index_active_token, 'tabela no indice x, antes')
                    token_logic_str[1] = [task_aux for task_aux in token_logic_str[1] if task_aux != task]
                    # the case when i removed a token from an AND that had only one last token
                    if not token_logic_str[1]:
                        # then i delete the whole structure from the list of token structures
                        index_active_token.remove(token_logic_str)

                    #print(index_active_token, 'tabela no indice x, depois')

                # case 1.2 - it's an xOR
                else:
                    #print(index_active_token)
                    #print(index_active_token, 'tabela no indice x, antes')
                    # delete the whole xOR structure, since the token goes for the task parsed first
                    index_active_token.remove(token_logic_str)
                    #print(index_active_token, 'tabela no indice x, depois')

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
                subsearch_1 = search_table(task, sub_table_list1)
                #if it's in the structure, i set the bool to True (parsed)
                bool_parsed = True

                # if the root node is a AND, the recursive call will have already decided if this leaf was a AND or xOR
                # and will already have deleted the token accordingly
                if token_logic_str[0][0] == 'AND':
                    # if the leaf returned a empty token list (either was the last token in a AND or it was a xOR)
                    if not subsearch_1[1]:
                        # checking if the second set is empty too
                        if not token_logic_str[2]:
                            index_active_token.remove(token_logic_str)
                        # if not, i just empty the current side
                        else:
                            token_logic_str[1] = []

                    # if the leaf was a AND that had more than one token
                    else:
                        #the subsearch_1[1][0][1]: [1] - last position of the search_table output. [0] - the first
                        #position of that list (is a list of token structs, but this only have one struct since i
                        #derivated it in the recursive call. [1] - the last index on the structure i got, the one
                        #who has the set of tasks. TL;DR - this updates the task set minus the consumed token
                        token_logic_str[1] = subsearch_1[1][0][1]

                # if the root is a xOR, then i must deal with it thoroughly. in this case, if the root is a xOR and
                # the leaf is also a xOR, i won't add it back in the token list as a simple token struct
                elif token_logic_str[0][0] == 'xOR':
                    # if the leaf returned a empty token list (either was the last token in an AND or it was a xOR)
                    if not subsearch_1[1]:
                        index_active_token.remove(token_logic_str)
                    # if it returned a AND that had more tokens to it
                    else:
                        # by my logic this generates a simple AND
                        # then, instead of keeping the complex structure, i add the derivated AND to the list
                        index_active_token.append(subsearch_1[1][0])

            # if the token was on the second leaf - task set
            elif task in token_logic_str[2]:
                # make a recursive call
                sub_table_list2 = [[[token_logic_str[0][2]], token_logic_str[2]]]
                subsearch_2 = search_table(task, sub_table_list2)
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
                            index_active_token.remove(token_logic_str)
                        # if not, i just empty the current leaf
                        else:
                            token_logic_str[2] = []

                    # if the leaf was a AND that had more than one token
                    else:
                        # the subsearch_2[1][0][1]: [1] - last position of the search_table output. [0] - the first
                        # position of that list (is a list of token structs, but this only have one struct since i
                        # derivated it in the recursive call. [1] - the last index on the structure i got, the one
                        # who has the set of tasks. TL;DR - this updates the task set minus the consumed token
                        token_logic_str[2] = subsearch_2[1][0][1]

                # if the root is a xOR, then i must deal with it thoroughly. in this case, if the root is a xOR and
                # the leaf is also a xOR, i won't add it back in the token list as a simple token struct
                elif token_logic_str[0][0] == 'xOR':
                    # if the leaf returned a empty token list (either was the last token in an AND or it was a xOR)
                    if not subsearch_2[1]:
                        index_active_token.remove(token_logic_str)
                    # if it returned a AND that had more tokens to it
                    else:
                        # by my logic this generates a simple AND
                        # then, instead of keeping the complex structure, i add the derivated AND to the list
                        index_active_token.append(subsearch_2[1][0])

            else:
                # in case it's not in the current structure
                continue

    # if there was not a single struct with the token i'm looking for, it will leave the bool_parsed with a False value
    return [bool_parsed, index_active_token]

def logic_input(active_tokens, task_input, task):
    # OBS.: The task_input is the same as if i used 'indiv[task]['in']'
    # I'm doing this because of the recursivity, if i keep using the immutable structure of the individual i can't
    # break the complex inputs to more simplistic ones.
    missing_tokens = 0
    parsed = 0

    # Case 0: a beggining task was found in the middle of the parsing
    # A penal_ini would have been applied if a non beginning task was executed before the begin ones, so this will
    # either add a parsed task or a missing token, and possibly a few unused tokens to be left
    if not task_input[0]:

        # print(task_input, task, active_tokens)
        result = search_table(task, active_tokens['inicio'])
        if result[0] is True:
            parsed = 1
        else:
            missing_tokens = 1
        # print(task_input, task, active_tokens)

    # Case 1: if the input condition is a simple AND or xOR
    elif len(task_input[0]) == 1:
        # just for readability
        logic_op = task_input[0][0]
        # Case 1.1 - simple & AND
        if logic_op == 'AND':
            for x in task_input[1]:
                result = search_table(task, active_tokens[x])
                # updating the token table on the 'x' index
                #active_tokens[x] = result[1] nem precisa, aparentemente eu compartilhei só uma referencia
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
                result = search_table(task, active_tokens[x])
                # updating the token table on the 'x' index
                #active_tokens[x] = result[1] nem precisa, aparentemente eu compartilhei só uma referencia
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
            simp_result = logic_input(active_tokens, simplified_input, task)
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
            subresult_1 = logic_input(active_tokens, sub_input1, task)
            # this is needed in order to keep the table consistant between the two recursive calls
            active_tokens = subresult_1[2]
            # and this gets the second leaf and tasks
            sub_input2 = [[task_input[0][2]],task_input[2]]
            subresult_2 = logic_input(active_tokens, sub_input2, task)
            #Now doing the root AND
            #basically i'm testing if the variable parsed was set 1 in both (successful)
            if subresult_1[1] == 1 and subresult_2[1] == 1:
                missing_tokens = 0
                parsed = 1
            else:
                missing_tokens = subresult_1[0] + subresult_2[0]
                parsed = 0
            # then i update the token table no matter what
            active_tokens = subresult_2[2]

        # Case 2.2: the root logic op is a xOR
        elif root_logic_op == 'xOR':
            # this gets the first logic leaf and the first task list
            sub_input1 = [[task_input[0][1]], task_input[1]]
            subresult_1 = logic_input(active_tokens, sub_input1, task)
            ''' TODO do i need to pass the modified active_tokens? cuz i still modify it if there was a AND where some of
            it's tasks weren't parsed, but since the root node is a XOR, for now i'm passing the intact table
            to the next leaf node. Maybe ask Fantinato'''
            if subresult_1[1] == 1:
                # the case when it parsed
                parsed = 1
                missing_tokens = 0
                active_tokens = subresult_1[2]

            else:
                # If it didn't parse, i try the second leaf node
                sub_input2 = [[task_input[0][2]], task_input[2]]
                subresult_2 = logic_input(active_tokens, sub_input2, task)

                if subresult_2[1] == 1:
                    # the case when it parsed
                    parsed = 1
                    missing_tokens = 0
                else:
                    # the last case, when neither parsed
                    parsed = 0
                    missing_tokens = subresult_1[0] + subresult_2[0]
                # No matter if it parses or not, i return the altered tabeka_token of the last try
                active_tokens = subresult_2[2]

    return [missing_tokens, parsed, active_tokens]


def choice_maker(logic_struct):
    # TODO put a case 0 just like i did on the firingRule script
    # Case 1: if the structure is SIMPLE
    if len(logic_struct[0]) == 1:
        logic_op = logic_struct[0][0]
        # Case 1.1: Simple and AND
        if logic_op == 'AND':
            # This will choose a random order to execute the tasks in this AND
            task_set = np.random.choice(a=logic_struct[1], size=len(logic_struct[1]), replace=False)
            #tasks_to_exec.extend(task_set)

        # Case 1.2: Simple and xOR
        elif logic_op == 'xOR':
            # This will choose just one random task to execute
            task_set  = np.random.choice(a=logic_struct[1], size=1)
            #tasks_to_exec.extend(task_set)

    # Case 2: if the structure is COMPLEX (recursivity applied)
    elif len(logic_struct[0]) == 3:
        # Just for convenience
        root_logic_op = logic_struct[0][0]
        # Special case, if one side of the complex structure is empty (i just treat like a simple structure)
        if not logic_struct[1] or not logic_struct[2]:
            # here i simply use a comprehension to pick only the non empty side of the struct
            simplified_logic_struct = [[logic_struct[0][1]],logic_struct[1]] if not logic_struct[2] else [[logic_struct[0][2]],logic_struct[2]]
            task_set = choice_maker(simplified_logic_struct)

        # Case 2.1: root leaf is an AND
        elif root_logic_op == 'AND':
            # Calling this same function recursively, passing the substructures on the left side
            left_logic_struct = [[logic_struct[0][1]],logic_struct[1]]
            left_tasks = choice_maker(left_logic_struct)
            # Now doing the right side
            right_logic_struct = [[logic_struct[0][2]], logic_struct[2]]
            right_tasks = choice_maker(right_logic_struct)
            if np.random.random() <= 0.5:
                task_set = np.concatenate([left_tasks, right_tasks])
            else:
                task_set = np.concatenate([right_tasks, left_tasks])

        elif root_logic_op == 'xOR':
            aux_random = np.random.random()
            if aux_random <= 0.5:
                left_logic_struct = [[logic_struct[0][1]], logic_struct[1]]
                task_set = choice_maker(left_logic_struct)
            else:
                right_logic_struct = [[logic_struct[0][2]], logic_struct[2]]
                task_set = choice_maker(right_logic_struct)
        else:
            print('ENOUGH IS ENOUGH!')
            print('I HAVE HAD IT WITH THESE MOTHERFUCKING SNAKES ON THIS MOTHERFUCKING PLANE!')

    return task_set


