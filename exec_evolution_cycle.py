import evolution_cycle as evol
import plotting as p
import csv
import pandas as pd
import openpyxl as xlsx


alphabetCM28 = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
logCM28 = {
        'A': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A9'],
        'B': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A8', 'A9'],
        'C': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A8', 'A9'],
        'D': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A7', 'A9']}

reference_pos_dict = {
        'A7': {'before': {'A6'}, 'after': {'A9'}},
        'A9': {'before': {'A7', 'A8'}, 'after': set()},
        'A8': {'before': {'A6'}, 'after': {'A9'}},
        'process': {'end': {'A9'}, 'start': {'A1'}},
        'A1': {'before': set(), 'after': {'A2'}},
        'A5': {'before': {'A4', 'A3'}, 'after': {'A6'}},
        'A6': {'before': {'A5'}, 'after': {'A7', 'A8'}},
        'A4': {'before': {'A3', 'A2'}, 'after': {'A3', 'A5'}},
        'A3': {'before': {'A4', 'A2'}, 'after': {'A4', 'A5'}},
        'A2': {'before': {'A1'}, 'after': {'A4', 'A3'}}}
# experiments = [{'comp': 1, 'prec':0, 'crosspoint':1, 'mutac':0.05, 'tax_cross':0.95},
#         {'comp': 1, 'prec': 0, 'crosspoint': 99, 'mutac': 0.3, 'tax_cross':0.7},
#         {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.05, 'tax_cross':0.95},
#         {'comp': 0, 'prec': 1, 'crosspoint': 99, 'mutac': 0.3, 'tax_cross':0.7},
#         {'comp': 0.5, 'prec': 0.5, 'crosspoint': 1, 'mutac': 0.05, 'tax_cross':0.95},
#         {'comp': 0.5, 'prec': 0.5, 'crosspoint': 99, 'mutac': 0.3, 'tax_cross':0.7}]
# experiments2 = [{'comp': 1, 'prec':0, 'crosspoint':1, 'mutac': 0.3, 'tax_cross':0.7},
#         {'comp': 1, 'prec': 0, 'crosspoint': 99, 'mutac': 0.05, 'tax_cross':0.95},
#         {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross':0.7},
#         {'comp': 0, 'prec': 1, 'crosspoint': 99, 'mutac': 0.05, 'tax_cross':0.95},
#         {'comp': 0.5, 'prec': 0.5, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross':0.7},
#         {'comp': 0.5, 'prec': 0.5, 'crosspoint': 99, 'mutac': 0.05, 'tax_cross':0.95}]

# experiments3 = [{'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross':0.7, 'pop_ex': 'cohab', 'elitism':0.5, 'muta_dir': 0.3},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross':0.7, 'pop_ex': 'kill', 'elitism':0.5, 'muta_dir': 0.3},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'cohab', 'elitism': 1, 'muta_dir': 0.05},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'kill', 'elitism': 1, 'muta_dir': 0.05},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'cohab', 'elitism': 1, 'muta_dir': 0.3},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'kill', 'elitism': 0.5, 'muta_dir': 0.05},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'kill', 'elitism': 1, 'muta_dir': 0.3},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'cohab', 'elitism': 0.5, 'muta_dir': 0.05}]
experiments4 = [{'comp': 0.5, 'prec': 0.5, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'cohab', 'elitism': 1, 'muta_dir': 0}]

for count in range(1):
    print('R O U N D - ' + str(count))
    for conf in experiments4:

        size_pop = 100
        pop_exchange = conf['pop_ex'] # c - cohab, k - kill ancestors
        max_generations = 2000
        weights_fit = {'comp': conf['comp'], 'prec': conf['prec']}
        crossover_setup = {'points': conf['crosspoint'], 'chance': conf['tax_cross']}
        mutation_setup = {'logic': conf['mutac'], 'complex': 0, 'taskset': conf['mutac'], 'begin-end': 0, 'directed': conf['muta_dir']}  # each key holds the percent of chance that each mutation has of taking place
        selection_setup = {'tournament': 0, 'roulette': 1}
        elitism = conf['elitism']
        max_len_trace = max([len(foo) for foo in logCM28.values()]) * 4
        set_quant = len(logCM28) * 5
        exec_id = 'completude-' + str(conf['comp']) + '-precisao-' + str(conf['prec']) + '-crosspoint-' + str(conf['crosspoint']) + '-mutac-' + str(conf['mutac']) + '-tax_cross-' + str(conf['tax_cross']) + '-pop_ex-' + str(conf['pop_ex']) + '-elit-' + str(conf['elitism']) + 'dir_mut' + str(conf['muta_dir']) + 'pc0exec' + str(count)
        # exec_id = 'lol1'
        #todo i need to compare the reference pos set with the individual

        result = evol.evolution_cycle(alphabetCM28, logCM28, size_pop, pop_exchange, max_generations, weights_fit, crossover_setup, mutation_setup, selection_setup, elitism, max_len_trace, set_quant, reference_pos_dict, exec_id)


        p.plot_evolution(result[1], exec_id)

        # # Writing stuff to a dataframe
        # df1_dict = {'Exec ID': exec_id, 'Last Best Ind': [result[0][-1]] }#, 'Fitness evolution (worst-avg-best)': result[1], 'Best Inds - all generations':result[0]}
        # df1 = pd.DataFrame(df1_dict)


        # try:
        #     writer = xlsx.load_workbook('output.xlsx')
        # except:
        #     writer = pd.ExcelWriter('output.xlsx', engine='openpyxl')
        #
        # last_row = writer.sheets
        # print(last_row)
        # exit()
        # df1.to_excel(writer, 'Main', index=False, startrow=last_row)
        # writer.save()

        # # Writing stuff on a xlsx
        # fields = [exec_id, result[0][-1], result[1], result[0]]
        # with open('param_results.xlsx', 'a', newline='') as f:
        #         writer = csv.writer(f, delimiter=',')
        #         writer.writerow(fields)
        fields = [exec_id, result[0][-1], result[1]]
        with open("output.csv", "a", newline='') as csvfile:
            writer = csv.writer(csvfile, dialect='excel', delimiter=',')
            writer.writerow(fields)
            csvfile.close()
