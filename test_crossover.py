import individuo_complex as ind
import copy as copy
import timeit as timeit
import collections as col
import numpy as np
import new_genetic_ops as gops

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
ind3 = col.OrderedDict([
    ('A1', {'in': [[], []], 'out': [['xOR', 'AND', 'xOR'], ['A5', 'A2'], ['A4']]}),
    ('A2', {'in': [['xOR', 'AND', 'xOR'], ['A1', 'A5'], []], 'out': [['xOR', 'AND', 'xOR'], ['A5'], ['A4']]}),
    ('A3', {'in': [['AND'], ['A5']], 'out': [[], []]}),
    ('A4', {'in': [['AND', 'xOR', 'xOR'], ['A1', 'A2'], ['A4']], 'out': [['xOR', 'AND', 'xOR'], ['A4'], []]}),
    ('A5', {'in': [['AND', 'xOR', 'xOR'], [], ['A1', 'A2', 'A5']], 'out': [['AND', 'AND', 'AND'], ['A3'], ['A5', 'A2']]}),
    ('inicio', [['xOR'], ['A1']]), ('fim', [['xOR'], ['A3']])])
ind4 = col.OrderedDict([
    ('A1', {'in': [[], []], 'out': [['xOR', 'AND', 'xOR'], ['A5', 'A2'], ['A4']]}),
    ('A2', {'in': [['xOR', 'AND', 'xOR'], ['A1', 'A5'], []], 'out': [['xOR', 'AND', 'xOR'], ['A5'], ['A4']]}),
    ('A3', {'in': [['AND'], ['A5']], 'out': [[], []]}),
    ('A4', {'in': [['AND', 'xOR', 'xOR'], ['A1', 'A2'], ['A4']], 'out': [['xOR', 'AND', 'xOR'], ['A4'], []]}),
    ('A5', {'in': [['AND', 'xOR', 'xOR'], [], ['A1', 'A2', 'A5']], 'out': [['AND', 'AND', 'AND'], ['A3'], ['A5', 'A2']]}),
    ('inicio', [['xOR'], ['A1']]), ('fim', [['xOR'], ['A3']])])

ind2mutated = col.OrderedDict([
    ('A1', {'out': [['xOR', 'AND', 'xOR'], ['A5', 'A2'], ['A4']], 'in': [[], []]}),
    ('A2', {'out': [['xOR', 'AND', 'xOR'], ['A5'], ['A4']], 'in': [['xOR', 'AND', 'xOR'], ['A1'], []]}),
    ('A3', {'out': [[], []], 'in': [['AND'], ['A5']]}),
    ('A4', {'out': [['xOR', 'AND', 'xOR'], ['A4'], []], 'in': [['AND', 'xOR', 'xOR'], ['A1', 'A2'], ['A4']]}),
    ('A5', {'out': [['AND', 'AND', 'AND'], ['A3'], []], 'in': [['AND', 'xOR', 'xOR'], [], ['A1', 'A2']]}),
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



for foo, bar in ind2.items():
    print(foo,' -> ', bar)

for foo, bar in ind2mutated.items():
    print(foo,' -> ', bar)


def compare_processes(indiv1, indiv2):
    ''' TODO to try to make this dynamically, search these two stackoverflow questions:
    Todo https://stackoverflow.com/questions/3844801/check-if-all-elements-in-a-list-are-identical
    Todo https://stackoverflow.com/questions/41705305/simultaneously-iterate-over-multiple-list-and-capture-difference-in-values
    OBS.: x.count() can count dictionaries (in/out sets), so i can count those dicts if i zip them by task'''

    # This function gives back only tasks that have identical in/out sets
    is_equal = []
    key_list = indiv1.keys()
    inout_list = ['in', 'out']
    # I simply compare both keys in each process
    for i in key_list:
        if i in ('inicio', 'fim'):
            if indiv1[i] == indiv2[i]:
                is_equal.append(i)
        else:
            for j in inout_list:
                if indiv1[i][j] == indiv2[i][j]:
                    is_equal.append([i, j])
    return is_equal


def directed_mutation_dataset(indiv1, indiv2):
    is_equal = compare_processes(indiv1, indiv2)
    if is_equal:
        for i in is_equal:
            if i in ('inicio', 'fim'):
                gops.mutation_begin_end(indiv1, i)
                gops.mutation_begin_end(indiv2, i)
            else:
                gops.mutation_taskset(indiv1, i)
                gops.mutation_taskset(indiv2, i)

# print(ind2mutated)

directed_mutation_dataset(ind2, ind3)

for foo, bar in ind2.items():
    print(foo,' -> ', bar)

for foo, bar in ind3.items():
    print(foo,' -> ', bar)
#
# result = compare_processes(ind2, ind2mutated)
# print(result)