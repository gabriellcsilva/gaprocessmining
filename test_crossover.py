import individuo_complex as ind
import copy as copy
import collections as col
import numpy as np
import new_genetic_ops as gops

'''
def crossover(ind1, ind2, crosspoint):
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
        even_set = range(0, len(crom_task_list), 2)
        uneven_set = range(1, len(crom_task_list), 2)
        heritage_set1 = [crom_task_list[i] for i in even_set]
        heritage_set2 = [crom_task_list[j] for j in uneven_set]

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
    # Function that cleans the input, prepping for the crossover to happen
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
    # Second part - filling the input based on the output
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

    # This part fills the inicio set
    # I would use a list comprehension, but with this for loop i both keep the chromossome right and fill the 'inicio'
    for key, value in indiv.items():
        if key not in ('inicio', 'fim'):
            # If it's a simple set but it doesn't have tasks in the task list
            if len(value['in']) == 2 and not value['in'][1]:
                # This would be true both to in = [[],[]] and [['AND'],[]], so i empty the possible logic op
                value['in'][0] = []
                indiv['inicio'][1].append(key)
    # Coolest way to quickly fill the 'inicio': Only the keys where the input[0] is empty will be added
    # indiv['inicio'][1] = [key for key, value in indiv.items() if not value['in'][0]]
    return indiv
'''

# alfabeto1 = ('A1', 'A2', 'A3', 'A4', 'A5')
# alfabeto2 = ('B1', 'B2', 'B3', 'B4', 'B5')
ind1 = col.OrderedDict([
    ('A1', {'in': [['AND', 'AND', 'xOR'], [], ['A1', 'A2', 'A4']], 'out': [['AND'], ['A3', 'A1', 'A4']]}),
    ('A2', {'in': [['xOR'], ['A2', 'A5']], 'out': [['AND', 'xOR', 'AND'], [], ['A3', 'A2', 'A4', 'A1']]}),
    ('A3', {'in': [['AND'], ['A1', 'A2', 'A4', 'A5']], 'out': [[], []]}),
    ('A4', {'in': [['AND', 'xOR', 'AND'], ['A1', 'A2'], ['A4', 'A5']], 'out': [['AND'], ['A3', 'A1', 'A4']]}),
    ('A5', {'in': [[], []], 'out': [['xOR', 'AND', 'AND'], ['A4'], ['A3', 'A2']]}),
    ('inicio', [['AND'], ['A5']]), ('fim', [['AND'], ['A3']])])

ind2 = col.OrderedDict([
    ('A1', {'in': [[], []], 'out': [['xOR', 'AND', 'xOR'], ['A5', 'A2'], ['A4']]}),
    ('A2', {'in': [['xOR', 'AND', 'xOR'], ['A1', 'A5'], []], 'out': [['xOR', 'AND', 'xOR'], ['A5'], ['A4']]}),
    ('A3', {'in': [['AND'], ['A5']], 'out': [[], []]}),
    ('A4', {'in': [['AND', 'xOR', 'xOR'], ['A1', 'A2'], ['A4']], 'out': [['xOR', 'AND', 'xOR'], ['A4'], []]}),
    ('A5', {'in': [['AND', 'xOR', 'xOR'], [], ['A1', 'A2', 'A5']], 'out': [['AND', 'AND', 'AND'], ['A3'], ['A5', 'A2']]}),
    ('inicio', [['xOR'], ['A1']]), ('fim', [['xOR'], ['A3']])])

'''
crosspoint = 99

result = gops.crossover(ind1, ind2, crosspoint)

for k,v in result[0].items():
    print('Tarefa:', k, ' - ', v)

print('_________________')
for k,v in result[1].items():
    print('Tarefa:', k, ' - ', v)

'''


for k,v in ind1.items():
    print('Tarefa:', k, ' - ', v)


# def mutation_logic(indiv):
#     # Chooses a task on the individual and change both input and output logic operators. This method keeps the complexity
#     # of the logic structure
#     logic_alpha = ['AND', 'xOR']
#     # This chooses a task to mutate
#     task_alpha = list(indiv.keys())
#     task_choice = np.random.choice(task_alpha)
#
#     # First case: if i chose the begin or end key
#     if task_choice in ('inicio', 'fim'):
#         new_logic_op = np.random.choice(logic_alpha)
#         indiv[task_choice][0] = new_logic_op
#
#     # Second case: i chose one of the regular keys
#     else:
#         # This is to test if the input/output isn't empty, meaning that it's a beginning task
#         # The first part mutates the input logic only
#         if indiv[task_choice]['in'][0]:
#             # I made this so it automatically chooses the same amount of logic ops present on the in/out
#             len_new_op = len(indiv[task_choice]['in'][0])
#             new_logic_op = list(np.random.choice(logic_alpha, len_new_op, replace=True))
#             indiv[task_choice]['in'][0] = new_logic_op
#
#         # The second part mutates the output logic only
#         if indiv[task_choice]['out'][0]:
#             len_new_op = len(indiv[task_choice]['out'][0])
#             new_logic_op = list(np.random.choice(logic_alpha, len_new_op, replace=True))
#             indiv[task_choice]['out'][0] = new_logic_op
#
#     return indiv

gops.mutation_logic(ind1)


for k,v in ind1.items():
    print('Tarefa:', k, ' - ', v)






