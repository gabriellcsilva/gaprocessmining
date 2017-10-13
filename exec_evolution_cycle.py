import evolution_cycle as evol


alphabetCM28 = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
logCM28 = {
        'A': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A9'],
        'B': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A8', 'A9'],
        'C': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A8', 'A9'],
        'D': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A7', 'A9']}
reference_pos_dict = {'A4': {'before': {'A2', 'A1', 'A3'}, 'after': {'A3', 'A5', 'A9', 'A6', 'A8', 'A7'}}, 'A3': {'before': {'A2', 'A1', 'A4'}, 'after': {'A5', 'A9', 'A4', 'A6', 'A8', 'A7'}}, 'A8': {'before': {'A3', 'A5', 'A2', 'A6', 'A4', 'A1'}, 'after': {'A9'}}, 'A5': {'before': {'A2', 'A1', 'A3', 'A4'}, 'after': {'A6', 'A9', 'A8', 'A7'}}, 'A6': {'before': {'A2', 'A1', 'A3', 'A4', 'A5'}, 'after': {'A8', 'A9', 'A7'}}, 'A2': {'before': {'A1'}, 'after': {'A3', 'A5', 'A9', 'A4', 'A6', 'A8', 'A7'}}, 'A1': {'before': set(), 'after': {'A3', 'A5', 'A9', 'A2', 'A6', 'A4', 'A8', 'A7'}}, 'A9': {'before': {'A3', 'A5', 'A2', 'A6', 'A4', 'A8', 'A1', 'A7'}, 'after': set()}, 'A7': {'before': {'A3', 'A5', 'A2', 'A6', 'A4', 'A1'}, 'after': {'A9'}}}

size_pop = 100
pop_exchange = 'cohab' # c - cohab, k - kill ancestors
max_generations = 100
weights_fit = {'comp': 0.5, 'prec': 0.5}
crossover_setup = {'points': 4, 'chance': 0.5}
mutation_setup = {'logic':1, 'complex':0, 'taskset': 1, 'begin-end': 0.1, 'directed':0.3}  # each key holds the percent of chance that each mutation has of taking place
selection_setup = {'tournament':0, 'roulette':1}
elitism = 0.1
max_len_trace = max([len(foo) for foo in logCM28.values()]) * 4
set_quant = len(logCM28) * 8
exec_id = 'lol'

#todo i need to compare the reference pos set with the individual

result = evol.evolution_cycle(alphabetCM28, logCM28, size_pop, pop_exchange, max_generations, weights_fit, crossover_setup, mutation_setup, selection_setup, elitism, max_len_trace, set_quant, reference_pos_dict, exec_id)


print('best of first gen: ',result[0][0])
print('best of last gen: ',result[0][-1])


# TODO Stopped here, need to fix the taskset mutation to ensure the individual always have a beginning/ending'''