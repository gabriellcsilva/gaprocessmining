import evolution_cycle as evol


alphabetCM28 = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
logCM28 = {
        'A': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A9'],
        'B': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A8', 'A9'],
        'C': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A8', 'A9'],
        'D': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A7', 'A9']}
size_pop = 100
pop_exchange = 'cohab' # c - cohab, k - kill ancestors
max_generations = 1000
weights_fit = {'comp': 0.8, 'prec': 0.2}
crossover_setup = {'points': 2, 'chance': 1}
mutation_setup = {'logic':1, 'complex':1, 'taskset': 1, 'begin-end': 1, 'directed':1}  # each key holds the percent of chance that each mutation has of taking place
selection_setup = {'tournament':0, 'roulette':1}
elitism = 0.1
max_len_trace = max([len(foo) for foo in logCM28.values()]) * 4
set_quant = len(logCM28) * 10
exec_id = 'lol'

result = evol.evolution_cycle(alphabetCM28, logCM28, size_pop, pop_exchange, max_generations, weights_fit, crossover_setup, mutation_setup, selection_setup, elitism, max_len_trace, set_quant, exec_id)


print(result[0][0], result[0][-1])

# TODO Stopped here, need to fix the taskset mutation to ensure the individual always have a beginning/ending'''