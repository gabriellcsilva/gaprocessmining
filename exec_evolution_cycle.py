import new_genetic_ops as gops
import individuo_complex as ind
import numpy as np
import copy as copy

def evolution_cycle(alphabet, logs, size_pop, pop_exchange, max_generations, weights_fit, crossover_setup,
                    mutation_setup, selection_setup, elitism, max_len_trace, set_quant, exec_id):

    # First i create the initial population
    pop = [[ind.criarIndividuo(alphabet), {'f':0,'c':0,'p':0}] for _ in range(size_pop)]
    # Calculating the fitness for the first population
    for individual in pop:
        individual[1] = gops.fitness(individuo=individual[0], logs=logs, max_len_trace=max_len_trace, set_quant=set_quant, weights=weights_fit)[1]

    # Some lists to keep the evolution of the run
    fit_evol = []
    best_ind_evol = []
    # Calculando os dados de fitness pros gráficos
    aux = [val[1]['f'] for val in pop]
    min_fit = min(aux)
    max_fit = max(aux)
    average = sum(aux) / len(aux)
    max_index = aux.index(max_fit)
    # Sorting the population so i can get the best fitness
    # sorted_pop = sorted(initial_pop, key=lambda t: t[1]['f'])
    # Keeping the evolution stats
    best_ind_evol.append(pop[max_index])
    fit_evol.append([min_fit, max_fit, average])

    # Beginning of the evolution cycle
    aux_gen = 0
    while max_generations > aux_gen:
        print('Geração ', aux_gen)
        new_pop = []
        # Elitism of the previous population
        if np.random.random() <= elitism:
            # A way to get the max fitness individual without sorting
            aux = [foo[1]['f'] for foo in pop]
            max_aux = max(aux)
            max_index = aux.index(max_aux)
            new_pop.append(pop[max_index])
        # Filling the new pop
        while len(new_pop) < len(pop):
            # Selection
            if selection_setup['tournament']==1:
                dad = gops.tournament_selection(pop)
                mom = gops.tournament_selection(pop)
            elif selection_setup['roulette']==1:
                dad = gops.roulette_selection(pop)
                mom = gops.roulette_selection(pop)
            else:
                print('incorrect setup for selection')
                exit()
            # Crossover
            if np.random.random() <= crossover_setup['chance']:
                result = gops.crossover(dad[0], mom[0], crossover_setup['points'])
                son_1 = [result[0], {'f':0,'c':0,'p':0}]
                son_2 = [result[1], {'f':0,'c':0,'p':0}]
            else:
                son_1 = copy.deepcopy(dad)
                son_2 = copy.deepcopy(mom)
            # Mutation
            if np.random.random() <= mutation_setup['logic']:
                gops.mutation_logic(son_1[0])
                gops.mutation_logic(son_2[0])
            if np.random.random() <= mutation_setup['complex']:
                gops.mutation_complexity(son_1[0])
                gops.mutation_complexity(son_2[0])
            if np.random.random() <= mutation_setup['taskset']:
                gops.mutation_taskset(son_1[0])
                gops.mutation_taskset(son_2[0])
            if np.random.random() <= mutation_setup['begin-end']:
                gops.mutation_begin_end(son_1[0])
                gops.mutation_begin_end(son_2[0])

            # Calculating fitness to the newborn
            son_1[1] = gops.fitness(individuo=son_1[0], logs=logs, max_len_trace=max_len_trace, set_quant=set_quant, weights=weights_fit)[1]
            son_2[1] = gops.fitness(individuo=son_2[0], logs=logs, max_len_trace=max_len_trace, set_quant=set_quant, weights=weights_fit)[1]
            # Adding the new children to the new pop
            new_pop.append(son_1)
            new_pop.append(son_2)
            if pop_exchange=='cohab':
                new_pop.append(dad)
                new_pop.append(mom)

        # Doing the directed mutation
        if mutation_setup['directed'] and (aux_gen > max_generations//2):
            if np.random.random() <= mutation_setup['directed']:
                indiv01 = gops.roulette_selection(new_pop)
                indiv02 = gops.roulette_selection(new_pop)
                gops.directed_mutation_dataset(indiv01[0], indiv02[0])

        # Losing the reference to the old pop and keeping the new one
        pop = new_pop
        aux_gen += 1

        # Collecting the data for the graphs
        bar = [val[1]['f'] for val in pop]
        min_fit = min(bar)
        max_fit = max(bar)
        average = sum(bar) / len(bar)
        max_index = bar.index(max_fit)
        # Sorting the population so i can get the best fitness
        # sorted_pop = sorted(initial_pop, key=lambda t: t[1]['f'])
        # Keeping the evolution stats
        best_ind_evol.append(pop[max_index])
        fit_evol.append([min_fit, max_fit, average])

    return [best_ind_evol, fit_evol, pop]
























alphabetCM28 = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
logCM28 = {
        'A': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A9'],
        'B': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A8', 'A9'],
        'C': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A8', 'A9'],
        'D': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A7', 'A9']}
size_pop = 100
pop_exchange = 'cohab' # c - cohab, k - kill ancestors
max_generations = 10
weights_fit = {'comp': 0.8, 'prec': 0.2}
crossover_setup = {'points': 2, 'chance': 0.8}
mutation_setup = {'logic':0.5, 'complex':0.5, 'taskset': 1, 'begin-end': 0, 'directed':0}  # each key holds the percent of chance that each mutation has of taking place
selection_setup = {'tournament':0, 'roulette':1}
elitism = 0.1
max_len_trace = max([len(foo) for foo in logCM28.values()]) * 4
set_quant = len(logCM28) * 4
exec_id = 'lol'

result = evolution_cycle(alphabetCM28, logCM28, size_pop, pop_exchange, max_generations, weights_fit, crossover_setup, mutation_setup, selection_setup, elitism, max_len_trace, set_quant, exec_id)


print(result[0][0], result[0][-1])

# TODO Stopped here, need to fix the taskset mutation to ensure the individual always have a beginning/ending