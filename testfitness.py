import collections as col
import new_genetic_ops as ngops
import numpy as np
import precision_calc as prc
a = col.OrderedDict([('A', {'out': [['AND'], ['D', 'C', 'B']], 'in': [[], []]}), ('B', {'out': [['xOR'], ['F', 'E']], 'in': [['AND'], ['A']]}), ('C', {'out': [['xOR'], ['E']], 'in': [['xOR'], ['A']]}), ('D', {'out': [['xOR'], ['E']], 'in': [['xOR'], ['A']]}), ('E', {'out': [['xOR'], ['G']], 'in': [['AND'], ['B', 'C', 'D']]}), ('F', {'out': [['AND'], ['G']], 'in': [['AND'], ['B']]}), ('G', {'out': [[], []], 'in': [['xOR'], ['F', 'E']]}), ('fim', [['AND'], ['G']]), ('inicio', [['xOR'], ['A']])])

ETM_Configuration1 = col.OrderedDict({0: ('A', 'B', 'C', 'D', 'E', 'G'), 1: ('A', 'D', 'B', 'C', 'E', 'G'), 2: ('A', 'B', 'C', 'F', 'G'), 3: ('A', 'C', 'B', 'F', 'G'), 4: ('A', 'B', 'D', 'C', 'F', 'G'), 5: ('A', 'C', 'D', 'B', 'F', 'G'), 6: ('A', 'B', 'D', 'C', 'E', 'G'), 7: ('A', 'B', 'C', 'D', 'F', 'G'), 8: ('A', 'D', 'B', 'C', 'F', 'G'), 9: ('A', 'D', 'C', 'B', 'F', 'G'), 10: ('A', 'C', 'B', 'E', 'G')})
amtlog = len(ETM_Configuration1)
sublog_evc_keys = np.random.choice(list(ETM_Configuration1.keys()), amtlog, False)  # Choosing an amount of traces
sublog_evc = {key: ETM_Configuration1[key] for key in sublog_evc_keys}
rpdict_sublog_evc = prc.positional_set(sublog_evc.values())

max_len_trace = max([len(foo) for foo in sublog_evc.values()]) * 1
set_quant = len(sublog_evc) * 50

fitness = ngops.fitness(individuo=a, logs=sublog_evc, max_len_trace=max_len_trace, set_quant=set_quant, weights={'comp': 0, 'prec': 1}, pos_dict = rpdict_sublog_evc)

print(fitness)