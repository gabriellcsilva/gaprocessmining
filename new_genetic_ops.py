import copy as copy
import collections as col
import numpy as np
import firing_rule as fr
import precision_calc as prec


def fitness(individuo, logs, set_quant, max_len_trace, weights):
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

    precisao = prec.precision_calc_heur(logs, individuo, set_quant, max_len_trace)

    completude = ((variaveis['parsed_all'] - punishment) / total_len_traces)

    #finalScore = (score + precisao) / 2
    final_score = (completude*weights['comp']) + (precisao*weights['prec'])

    # Formula do artigo 372: score = (0.4 * (parsed/total_len_traces)) + (0.6 * (parsed_traces/total_traces))
    # score = (0.4 * (parsed / total_len_traces)) + (0.6 * (parsed_traces / total_traces))

    return [resultado, {'f':final_score,'c':completude, 'p':precisao}]

def roulette_selection(pop):
    lista = [ind[-1]['f'] for ind in pop]
    # This is a simple form of getting a proportional minimal positive value to add to each position in a list that has
    # negative elements on it
    fatorPos = abs(min(lista)) + abs(max(lista)) / (abs(min(lista)) + abs(max(lista)))
    i = 0  # Variable used to get the index of the selected position
    aux = 0
    soma = sum(lista) + fatorPos*len(lista)
    # Spinning the wheel
    stop_roulette = np.random.random() * soma
    # This while loop adds each value of the list until i reach the stop_roulette value
    while i < len(lista) and aux < stop_roulette:
        aux += lista[i] + fatorPos
        i += 1
    # I do this because i add 1 to 'i' at the end but the while only fails in the next loop
    i -= 1
    return pop[i]


def tournament_selection(pop):
    try:
        choice = np.random.choice(len(pop), 10, False)
        selection = [pop[x] for x in choice]
        selection = sorted(selection, key=lambda t: t[1]['f'])
    except Exception as e:
        print('deu problema porque: ')
        print(selection)
        print(e)
    return selection[-1]


def crossover(ind1, ind2, crosspoint):
    """ This crossover incorporates one point, two points and uniform crossovers"""
    crom_task_list = ind1.keys() - ('inicio', 'fim')
    crom_task_list = sorted(crom_task_list)

    # Case 1, if it's a single point crossover:
    if crosspoint == 1:
        cross_choice = np.random.randint(1, len(crom_task_list))
        #print('esse foi o ponto de crossover: ', cross_choice)
        heritage_set1 = crom_task_list[:cross_choice]
        heritage_set2 = crom_task_list[cross_choice:]

    # Case 2, if it's a two point crossover
    elif crosspoint == 2:
        aux_choice = range(1, len(crom_task_list) - 1)
        cross_choice = sorted(np.random.choice(aux_choice, 2, False))
        #print('teste pra saber se tá na ordem certa: ', cross_choice)
        heritage_set1 = crom_task_list[:cross_choice[0]] + crom_task_list[cross_choice[1]:]
        heritage_set2 = crom_task_list[cross_choice[0]:cross_choice[1]]
        #print(heritage_set1, 'fatias do inicio ao primeiro ponto, e do segundo ponto ao final')
        #print(heritage_set2,'fatia entre o primeiro ponto e o segundo')

    # Case 3, if it's an uniform crossover
    else:
        # First i choose a random number 'n' of tasks to choose from the task set
        rand_num_task = np.random.randint(1, len(crom_task_list))
        # The first set will have 'n' random chosen tasks
        heritage_set1 = list(np.random.choice(crom_task_list, rand_num_task, replace=False))
        # The second set will have the rest of the tasks
        heritage_set2 = [bar for bar in crom_task_list if bar not in heritage_set1]
        # print(' Uniform crossover ')
        # print('random number of tasks to choose: ', rand_num_task)
        # print('set 1: ', heritage_set1)
        # print('set 2: ', heritage_set2)

    # Trying a fancy new trick, unpacking of dictionaries -> z = {**{'x': 1}, **{'y': 2}}
    first_son = {**{foo: copy.deepcopy(ind1[foo]) for foo in heritage_set1}, **{bar: copy.deepcopy(ind2[bar]) for bar in heritage_set2}}
    second_son = {**{foo: copy.deepcopy(ind2[foo]) for foo in heritage_set1}, **{bar: copy.deepcopy(ind1[bar]) for bar in heritage_set2}}

    # Reassigning the 'inicio' and 'fim'
    first_son['inicio'] = copy.deepcopy(ind1['inicio'])
    first_son['fim'] = copy.deepcopy(ind1['fim'])
    second_son['inicio'] = copy.deepcopy(ind2['inicio'])
    second_son['fim'] = copy.deepcopy(ind2['fim'])

    # Cleaning the inputs and refilling it basend in the output
    clear_input(first_son)
    clear_input(second_son)
    fill_in_by_out(first_son)
    fill_in_by_out(second_son)

    # TODO think how to express the fitness values
    first_son = col.OrderedDict(sorted(first_son.items(), key=lambda l: l[0]))
    second_son = col.OrderedDict(sorted(second_son.items(), key=lambda l: l[0]))

    return [first_son, second_son]


def clear_input(indiv):
    """Support function that cleans the input, prepping for the crossover to happen"""
    for key, value in indiv.items():
        # If it's the beginning or end, since it's a different structure, i empty it here keeping the logic ops
        if key in ('inicio', 'fim'):
            value[1] = []
        # If it's a complex structure - AND of xOR's, etc..., I empty the first and second indexes
        elif len(value['in'][0]) == 3:
            value['in'][1] = []
            value['in'][2] = []
        # If it's a simple structure - AND, xOR
        else:
            value['in'][1] = []


def fill_in_by_out(indiv):
    """Support function that fills the input based on the output"""
    # Going through every task in the individual
    for key, value in indiv.items():
        if key not in ('inicio', 'fim'):
            # Deciding how many task lists i have in the output
            to_fill = []
            if len(value['out'][0]) == 3:
                # If the output has two lists of tasks, i put them in a unique list
                # using the iterable unpacking magic to unite both lists
                to_fill.extend([*value['out'][1], *value['out'][2]])
            elif len(value['out'][0]) == 1:
                # In case it's just one list, passing it to 'to_fill'
                to_fill.extend(value['out'][1])
            else:
                # In case the output is empty - output to the process' end
                indiv['fim'][1].append(key)

            # Filling the input with the 'to_fill' list
            for i in to_fill:
                # First case - The input structure is complex
                if len(indiv[i]['in'][0]) == 3:
                    # I generate a random number to decide in which side to add the key task
                    rand_aux = np.random.rand()
                    if rand_aux >= 0.5:
                        indiv[i]['in'][1].append(key)
                    else:
                        indiv[i]['in'][2].append(key)

                # Second case - the structure is simple
                elif len(indiv[i]['in'][0]) == 1:
                    indiv[i]['in'][1].append(key)

                # In case it tries adding a task to a input that was previously a 'inicio' task
                else:
                    #print('Tried to add to a inicio task, think if this is fucking up the chromossome')
                    # It'll only come here the fist time, then it'll fall on the previous case
                    operator = np.random.choice(['AND', 'xOR'])
                    indiv[i]['in'][0].append(operator)
                    indiv[i]['in'][1].append(key)

    # This part fills the 'inicio' set
    # I would use a list comprehension, but with this for loop i both keep the chromossome right and fill the 'inicio'
    for key, value in indiv.items():
        if key not in ('inicio', 'fim'):
            # If it's a simple set but it doesn't have tasks in the task list
            if len(value['in']) == 2 and not value['in'][1]:
                # This would be true both to in = [[],[]] and [['AND'],[]], so i empty the possible logic op
                value['in'][0] = []
                indiv['inicio'][1].append(key)

    # Making sure the individual have a beginning and ending
    if not indiv['inicio'][1]:
        mutation_begin_end(indiv, 'inicio')
    if not indiv['fim'][1]:
        mutation_begin_end(indiv, 'fim')
    # Coolest way to quickly fill the 'inicio': Only the keys where the input[0] is empty will be added
    # indiv['inicio'][1] = [key for key, value in indiv.items() if not value['in'][0]]
    return indiv


def mutation_logic(indiv):
    """
    :type indiv: dict of dicts
    """
    # Chooses a task on the individual and change both input and output logic operators. This method keeps the complexity
    # of the logic structure
    logic_alpha = ['AND', 'xOR']
    # This chooses a task to mutate
    task_alpha = list(indiv.keys())
    task_choice = np.random.choice(task_alpha)

    # First case: if i chose the begin or end key
    if task_choice in ('inicio', 'fim'):
        new_logic_op = np.random.choice(logic_alpha)
        indiv[task_choice][0] = [new_logic_op]

    # Second case: i chose one of the regular keys
    else:
        # This is to test if the input/output isn't empty, meaning that it's a beginning task
        # The first part mutates the input logic only
        if indiv[task_choice]['in'][0]:
            # I made this so it automatically chooses the same amount of logic ops present on the in/out
            len_new_op = len(indiv[task_choice]['in'][0])
            new_logic_op = list(np.random.choice(logic_alpha, len_new_op, replace=True))
            indiv[task_choice]['in'][0] = new_logic_op

        # The second part mutates the output logic only
        if indiv[task_choice]['out'][0]:
            len_new_op = len(indiv[task_choice]['out'][0])
            new_logic_op = list(np.random.choice(logic_alpha, len_new_op, replace=True))
            indiv[task_choice]['out'][0] = new_logic_op

    # Doesn't need a return apparently
    #return indiv


def mutation_complexity(indiv):
    """Obs.: I chose to tame this operator to affect only in or out sets, because it has a way more aggressive aproach
    to the mutations possible."""
    # Chooses a task and changes the complexity of either input or output. Since i change the structure, i either keep
    # only the first logic op or complete it with two new logic ops.
    logic_alpha = ['AND', 'xOR']
    aux_alpha = ['in', 'out']
    task_alpha = list(indiv.keys() - ('inicio', 'fim'))
    # This chooses a task to mutate
    task_choice = np.random.choice(task_alpha)
    # then i choose if i'll mutate input or output
    set_choice = np.random.choice(aux_alpha)

    # This tests if it's not empty (inicio/fim)
    if indiv[task_choice][set_choice][0]:
        # Case 01: Complexify - i have a simple structure and i change it to a complex one
        if len(indiv[task_choice][set_choice][0]) == 1:
            # Choosing two random new logic ops to add to the new struct
            new_logic_ops = np.random.choice(logic_alpha, 2, True)
            # adding it to the structure
            indiv[task_choice][set_choice][0].extend(new_logic_ops)
            # Copying the tasks to redistribute on the new struct
            taskset = indiv[task_choice][set_choice][1][:]
            # choosing a random point to split the set
            rand_index = np.random.randint(len(taskset))
            sidea_tasks = taskset[0:rand_index]
            sideb_tasks = taskset[rand_index:]
            # Assigning the sets to each side
            indiv[task_choice][set_choice][1] = sidea_tasks
            indiv[task_choice][set_choice].append(sideb_tasks)

        # Case 02: Simplify - i have a complex struct and i change it to a simple one
        else:
            # Getting the root logic op
            logic_op = indiv[task_choice][set_choice][0][0]
            # Putting every task in the same set
            taskset = []
            taskset.extend(indiv[task_choice][set_choice][1])
            taskset.extend(indiv[task_choice][set_choice][2])
            # Deleting the last position
            del indiv[task_choice][set_choice][2]
            # Reassigning logic op and tasks
            indiv[task_choice][set_choice][0] = [logic_op]
            indiv[task_choice][set_choice][1] = taskset

    #return indiv


def mutation_taskset(indiv, task_choice_preset=None):
    # TODO think if i wanna make the number of tasks raffled dynamic or just keep adding one task mutation per time
    # First i set the tasks that i can choose to work on for the mutation
    task_alpha = list(indiv.keys() - ('inicio', 'fim'))
    # Setting this alphabet to help with the handling of the input/output sets
    set_alpha = ['in', 'out']
    # This is to allow to change a specific task in the process model
    if task_choice_preset == None:  # Case 1 - the mutation happens randomly
        # Then i choose one task to add or remove tasks to it's in/out sets
        task_choice = np.random.choice(task_alpha)
        # The choice between in/out sets determine if the chosen task will be added to the beginning or ending of the process
        set_choice = np.random.choice(set_alpha)
    else:   # Case 2 - if i specify the task to mutate
        task_choice = task_choice_preset[0]
        set_choice = task_choice_preset[1]

    # set of tasks that i have to exclude from the raffle to chose the in/out tasks to include on the task's in/out sets
    existing_tasks = []
    if indiv[task_choice][set_choice][0]:   # This only mutates sets with tasks
        # I get all the tasks that already are in, to keep from repeating them
        existing_tasks.extend(indiv[task_choice][set_choice][1])
        if len(indiv[task_choice][set_choice][0]) == 3:
            existing_tasks.extend(indiv[task_choice][set_choice][2])

        # print(existing_tasks, 'tasks that are already in')
        # Set of tasks that i can choose
        del_or_insert = np.random.randint(1,3)
        # del_or_insert = 2 - was testing the task deleting
        # Deciding if i'll add or remove a task from the raffled set
        if del_or_insert == 1:
            leftover_alpha = [i for i in task_alpha if i not in existing_tasks]
            # print(leftover_alpha, 'tasks that can be raffled')
            mutation_task = np.random.choice(leftover_alpha, 1)[0]
            # print(mutation_task, 'task chosen to mutate (add) the \'',set_choice,'\' set')

            # Deciding where i'll insert the task
            index = np.random.randint(1, 3) if len(indiv[task_choice][set_choice][0]) == 3 else 1
            # Adding it to the chosen index
            indiv[task_choice][set_choice][index].append(mutation_task)

            aux = 'in' if set_choice == 'out' else 'out'
            if indiv[mutation_task][aux][0]:
                index2 = np.random.randint(1, 3) if len(indiv[mutation_task][aux][0]) == 3 else 1
                indiv[mutation_task][aux][index2].append(task_choice)
            else:
                new_logic = np.random.choice(a=('AND', 'xOR'), size=1)[0]
                indiv[mutation_task][aux][0].append(new_logic)
                indiv[mutation_task][aux][1].append(task_choice)
                if aux == 'in':
                    indiv['inicio'][1].remove(mutation_task)
                else:
                    indiv['fim'][1].remove(mutation_task)
        else:
            # Choosing the task to remove from the chosen set
            mutation_task = np.random.choice(existing_tasks, 1)[0]
            # print(mutation_task, 'task chosen to mutate (remove) the \'', set_choice, '\' set')

            if mutation_task in indiv[task_choice][set_choice][1]:
                indiv[task_choice][set_choice][1].remove(mutation_task)
            else:
                indiv[task_choice][set_choice][2].remove(mutation_task)
            # Checking if after the removal the set isn't empty
            if len(indiv[task_choice][set_choice][0])==3:
                if not indiv[task_choice][set_choice][1] and not indiv[task_choice][set_choice][2]:
                    indiv[task_choice][set_choice] = [[], []]
                    if set_choice == 'in':
                        indiv['inicio'][1].append(task_choice)
                    else:
                        indiv['fim'][1].append(task_choice)
            else:
                if not indiv[task_choice][set_choice][1]:
                    indiv[task_choice][set_choice] = [[], []]
                    if set_choice == 'in':
                        indiv['inicio'][1].append(task_choice)
                    else:
                        indiv['fim'][1].append(task_choice)

            # Removing the chosen task from the mutated task respective set
            aux = 'in' if set_choice == 'out' else 'out'
            if task_choice in indiv[mutation_task][aux][1]:
                indiv[mutation_task][aux][1].remove(task_choice)
            else:
                indiv[mutation_task][aux][2].remove(task_choice)

            # Checking if after the removal the set isn't empty
            if len(indiv[mutation_task][aux])==3:
                if not indiv[mutation_task][aux][1] and not indiv[mutation_task][aux][2]:
                    indiv[mutation_task][aux] = [[],[]]
                    if aux == 'in':
                        indiv['inicio'][1].append(mutation_task)
                    else:
                        indiv['fim'][1].append(mutation_task)
            else:
                if not indiv[mutation_task][aux][1]:
                    indiv[mutation_task][aux] = [[], []]
                    if aux == 'in':
                        indiv['inicio'][1].append(mutation_task)
                    else:
                        indiv['fim'][1].append(mutation_task)
    # Doesn't need return, mutates it in loco


def mutation_begin_end(indiv, inout_task_preset=None):
    # First i set the tasks that i can choose to work on for the mutation
    task_alpha = list(indiv.keys() - ('inicio', 'fim'))
    # Setting this alphabet to help with the handling of the input/output sets
    set_alpha = ['in', 'out']
    # Then i choose one task to add to the beginning/ending of the process
    task_choice = np.random.choice(task_alpha)
    # The choice between in/out sets determine if the chosen task will be added to the beginning or ending of the process
    if inout_task_preset == None:
        set_choice = np.random.choice(set_alpha)
    else:
        set_choice = 'in' if inout_task_preset == 'inicio' else 'out'
    # print(task_choice, 'task choice to add to begin/end,', set_choice, ' set choice')
    # set of tasks that i have to delete the chosen task from it's in/out sets
    toclear = []
    if indiv[task_choice][set_choice][0]:  # If it's not empty
        if len(indiv[task_choice][set_choice][0]) == 3:
            toclear.extend(indiv[task_choice][set_choice][1])
            toclear.extend(indiv[task_choice][set_choice][2])
        else:
            toclear = indiv[task_choice][set_choice][1][:]

        indiv[task_choice][set_choice] = [[],[]]
        # This is just to manipulate accordingly the correspondent sets between the tasks on the process
        aux = 'in' if set_choice == 'out' else 'out'
        for i in toclear:   # Percorring the sets of tasks to clean the chosen from
            if len(indiv[i][aux][0]) == 3:  # If i need to search the chosen task in a complex struct
                if task_choice in indiv[i][aux][1]: # If it's in the left side
                    indiv[i][aux][1].remove(task_choice)
                else:   # If it's in the right side
                    indiv[i][aux][2].remove(task_choice)

                if not indiv[i][aux][1] and not indiv[i][aux][2]:   # This is to correct the process if some set ended empty
                    indiv[i][aux] = [[],[]]
                    # Then i'll end with another task on the beginning/ending of the process
                    if aux == 'in':
                        indiv['inicio'][1].append(i)
                    else:
                        indiv['fim'][1].append(i)

            else:
                indiv[i][aux][1].remove(task_choice)
                if not indiv[i][aux][1]:   # This is to correct the process if some set ended empty
                    indiv[i][aux] = [[],[]]
                    # Then i'll end with another task on the beginning/ending of the process
                    if aux == 'in':
                        indiv['inicio'][1].append(i)
                    else:
                        indiv['fim'][1].append(i)

        # Then i finalize putting the cleared task in the respective beginning/ending set
        if set_choice == 'in':
            indiv['inicio'][1].append(task_choice)
        else:
            indiv['fim'][1].append(task_choice)

    return indiv


def compare_processes(indiv1, indiv2):
    ''' TODO to try to make this dynamically, search these two stackoverflow questions:
    Todo https://stackoverflow.com/questions/3844801/check-if-all-elements-in-a-list-are-identical
    Todo https://stackoverflow.com/questions/41705305/simultaneously-iterate-over-multiple-list-and-capture-difference-in-values
    OBS.: x.count() can count dictionaries (in/out sets), so i can count those dicts if i zip them by task'''

    # This function gives back only tasks that have identical in/out sets
    set_equal = []
    key_list = indiv1.keys()
    inout_list = ['in', 'out']
    # I simply compare both keys in each process
    for i in key_list:
        if i in ('inicio', 'fim'):
            if indiv1[i] == indiv2[i]:
                set_equal.append(i)
        else:
            for j in inout_list:
                if indiv1[i][j] == indiv2[i][j]:
                    set_equal.append([i, j])
    return set_equal


def directed_mutation_dataset(indiv1, indiv2):
    set_equal = compare_processes(indiv1, indiv2)
    print(set_equal, ' isequalpo')
    # gives me every task and in/out set that is equal between the process models compared
    if set_equal: # If they have something in common
        for i in set_equal:
            if i in ('inicio', 'fim'): # If i'm dealing with the extremities of the process
                mutation_begin_end(indiv1, i)
                mutation_begin_end(indiv2, i)
            else: # if i'm dealing with a task/in-out pair
                mutation_taskset(indiv1, i)
                mutation_taskset(indiv2, i)
    # point of no return