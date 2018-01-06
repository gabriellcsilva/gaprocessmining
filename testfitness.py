import collections as col
import new_genetic_ops as ngops
import numpy as np
import precision_calc as prc
a = col.OrderedDict([('A', {'out': [['AND'], ['D', 'C', 'B']], 'in': [[], []]}), ('B', {'out': [['xOR'], ['F', 'E']], 'in': [['AND'], ['A']]}), ('C', {'out': [['xOR'], ['E']], 'in': [['xOR'], ['A']]}), ('D', {'out': [['xOR'], ['E']], 'in': [['xOR'], ['A']]}), ('E', {'out': [['xOR'], ['G']], 'in': [['AND'], ['B', 'C', 'D']]}), ('F', {'out': [['AND'], ['G']], 'in': [['AND'], ['B']]}), ('G', {'out': [[], []], 'in': [['xOR'], ['F', 'E']]}), ('fim', [['AND'], ['G']]), ('inicio', [['xOR'], ['A']])])

ETM_Configuration1 = col.OrderedDict({0: ('A', 'B', 'C', 'D', 'E', 'G'), 1: ('A', 'D', 'B', 'C', 'E', 'G'), 2: ('A', 'B', 'C', 'F', 'G'), 3: ('A', 'C', 'B', 'F', 'G'), 4: ('A', 'B', 'D', 'C', 'F', 'G'), 5: ('A', 'C', 'D', 'B', 'F', 'G'), 6: ('A', 'B', 'D', 'C', 'E', 'G'), 7: ('A', 'B', 'C', 'D', 'F', 'G'), 8: ('A', 'D', 'B', 'C', 'F', 'G'), 9: ('A', 'D', 'C', 'B', 'F', 'G'), 10: ('A', 'C', 'B', 'E', 'G')})

# # a = {
#     'A1': {'in':[[],[]], 'out':[['AND'],['A2']]},
#     'A2': {'in':[['AND'],['A1']], 'out':[['AND'],['A3', 'A4']]},
#     'A3': {'in':[['AND'],['A2']], 'out':[['AND'],['A5']]},
#     'A4': {'in':[['AND'],['A2']], 'out':[['AND'],['A5']]},
#     'A5': {'in':[['AND'],['A3', 'A4']], 'out':[['AND'],['A6']]},
#     'A6': {'in':[['AND'],['A5']], 'out':[['xOR'],['A7','A8']]},
#     'A7': {'in':[['AND'],['A6']], 'out':[['AND'],['A9']]},
#     'A8': {'in':[['AND'],['A6']], 'out':[['AND'],['A9']]},
#     'A9': {'in':[['xOR'],['A7','A8']], 'out':[[],[]]},
#     'inicio': [['AND'],['A1']],
#     'fim': [['AND'],['A9']]
# }
# logTraces = {
#     'A': ('A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A9'),
#     'B': ('A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A8', 'A9'),
#     'C': ('A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A8', 'A9'),
#     'D': ('A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A7', 'A9')}

amtlog = len(ETM_Configuration1)
sublog_evc_keys = np.random.choice(list(ETM_Configuration1.keys()), amtlog, False)  # Choosing an amount of traces
sublog_evc = {key: ETM_Configuration1[key] for key in sublog_evc_keys}
rpdict_sublog_evc = prc.positional_set(sublog_evc.values())

max_len_trace = max([len(foo) for foo in sublog_evc.values()]) * 1
set_quant = len(sublog_evc) * 50

fitness = ngops.fitness(individuo=a, logs=sublog_evc, max_len_trace=max_len_trace, set_quant=set_quant, weights={'comp': 0, 'prec': 1}, pos_dict = rpdict_sublog_evc)

print(fitness)