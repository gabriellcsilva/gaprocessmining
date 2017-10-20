import trace_maker as tm
import firing_rule as fr
import json as json
import precision_calc as prc
import new_genetic_ops as gops
import timeit

ind_teste_complex = {
    'A1': {'in': [[], []], 'out': [['AND', 'AND', 'AND'], ['A6'], []]},
    'A2': {'in': [['AND'], ['A2', 'A4']], 'out': [['AND', 'AND', 'AND'], ['A6'], ['A2']]},
    'A3': {'in': [['AND', 'xOR', 'xOR'], ['A4'], []], 'out': [['xOR'], ['A5', 'A6']]},
    'A4': {'in': [[], []], 'out': [['AND', 'AND', 'AND'], ['A2'], ['A6', 'A3']]},
    'A5': {'in': [['AND'], ['A3']], 'out': [[], []]},
    'A6': {'in': [['AND', 'xOR', 'xOR'], ['A1', 'A2'], ['A3', 'A4', 'A6']], 'out': [['AND', 'xOR', 'AND'], ['A6'], []]},
    'inicio': [['xOR'], ['A1', 'A4']],
    'fim': [['AND'], ['A5']]
    }

CMArtigo28 = {
    'A1': {'in':[[],[]], 'out':[['AND'],['A2']]},
    'A2': {'in':[['AND'],['A1']], 'out':[['AND'],['A3', 'A4']]},
    'A3': {'in':[['AND'],['A2']], 'out':[['AND'],['A5']]},
    'A4': {'in':[['AND'],['A2']], 'out':[['AND'],['A5']]},
    'A5': {'in':[['AND'],['A3', 'A4']], 'out':[['AND'],['A6']]},
    'A6': {'in':[['AND'],['A5']], 'out':[['xOR'],['A7','A8']]},
    'A7': {'in':[['AND'],['A6']], 'out':[['AND'],['A9']]},
    'A8': {'in':[['AND'],['A6']], 'out':[['AND'],['A9']]},
    'A9': {'in':[['xOR'],['A7','A8']], 'out':[[],[]]},
    'inicio': [['AND'],['A1']],
    'fim': [['AND'],['A9']]
}
CMArtigo28ALT = {
    'A1': {'in':[[],[]], 'out':[['AND'],['A2']]},
    'A2': {'in':[['AND'],['A1']], 'out':[['AND'],['A3', 'A4']]},
    'A3': {'in':[['AND'],['A2']], 'out':[['AND'],['A5']]},
    'A4': {'in':[['AND'],['A2']], 'out':[['AND'],['A5']]},
    'A5': {'in':[['AND'],['A3', 'A4']], 'out':[['AND'],['A6']]},
    'A6': {'in':[['AND'],['A5']], 'out':[['xOR'],['A7','A8']]},
    'A7': {'in':[['AND'],['A6']], 'out':[['AND'],['A9']]},
    'A8': {'in':[['AND'],['A6']], 'out':[[],[]]},
    'A9': {'in':[['xOR'],['A7']], 'out':[[],[]]},
    'inicio': [['AND'],['A1']],
    'fim': [['XOR'],['A9', 'A8']]
}


ind_teste_complex2 = {
    'A1': {'in': [[], []], 'out': [['AND', 'xOR', 'xOR'], ['A2', 'A4'], ['A3', 'A5']]},
    'A2': {'in': [['AND'], ['A1']], 'out': [['AND'], ['A6']]},
    'A3': {'in': [['AND'], ['A1']], 'out': [['AND'], ['A8']]},
    'A4': {'in': [['AND'], ['A1']], 'out': [['AND'], ['A7']]},
    'A5': {'in': [['AND'], ['A1']], 'out': [['AND'], ['A8']]},
    'A6': {'in': [['AND'], ['A2']], 'out': [['AND'], ['A8']]},
    'A7': {'in': [['AND'], ['A4']], 'out': [['AND'], ['A8']]},
    'A8': {'in': [['AND', 'xOR', 'xOR'], ['A6', 'A7'], ['A3', 'A5']], 'out': [[], []]},
    'inicio': [['xOR'],['A1']],
    'fim': [['xOR'],['A8']]
}

ind_teste_complex3 = {
    'A1': {'in': [[], []], 'out': [['AND','xOR','xOR'], ['A2', 'A4', 'A6'], ['A3', 'A5']]},
    'A2': {'in': [['AND'], ['A1']], 'out': [['AND'], ['A8']]},
    'A3': {'in': [['AND'], ['A1']], 'out': [['AND'], ['A10']]},
    'A4': {'in': [['AND'], ['A1']], 'out': [['AND'], ['A8']]},
    'A5': {'in': [['AND'], ['A1']], 'out': [['AND'], ['A10']]},
    'A6': {'in': [['AND'], ['A1']], 'out': [['AND'], ['A7', 'A9']]},
    'A7': {'in': [['AND'], ['A6']], 'out': [['AND'], ['A11']]},
    'A8': {'in': [['xOR'], ['A2', 'A4']], 'out': [['AND'], ['A17']]},
    'A9': {'in': [['AND'], ['A6']], 'out': [['xOR'], ['A11']]},
    'A10': {'in': [['xOR'], ['A3', 'A5']], 'out': [['AND', 'xOR', 'xOR'], ['A12', 'A13'], ['A14', 'A15']]},
    'A11': {'in': [['AND'], ['A7', 'A9']], 'out': [['AND'], ['A17']]},
    'A12': {'in': [['AND'], ['A10']], 'out': [['AND'], ['A16']]},
    'A13': {'in': [['AND'], ['A10']], 'out': [['AND'], ['A16']]},
    'A14': {'in': [['AND'], ['A10']], 'out': [['AND'], ['A16']]},
    'A15': {'in': [['AND'], ['A10']], 'out': [['AND'], ['A16']]},
    'A16': {'in': [['AND', 'xOR', 'xOR'], ['A12', 'A13'], ['A14', 'A15']], 'out': [['AND'], ['A17']]},
    'A17': {'in': [['AND', 'xOR', 'AND'], ['A8', 'A11'], ['A16']], 'out': [[], []]},
    'inicio': [['AND'], ['A1']],
    'fim': [['AND'], ['A17']]
}

ind_teste_complex3altered = {
    'A1': {'in': [[], []], 'out': [['AND','xOR','xOR'], ['A4', 'A6'], ['A3', 'A5']]},
    'A2': {'in': [[], []], 'out': [['AND'], ['A8']]},
    'A3': {'in': [['AND'], ['A1']], 'out': [['AND'], ['A10']]},
    'A4': {'in': [['AND'], ['A1']], 'out': [['AND'], ['A8']]},
    'A5': {'in': [['AND'], ['A1']], 'out': [['AND'], ['A10']]},
    'A6': {'in': [['AND'], ['A1']], 'out': [['AND'], ['A7', 'A9']]},
    'A7': {'in': [['AND'], ['A6']], 'out': [['AND'], ['A11']]},
    'A8': {'in': [['xOR'], ['A2', 'A4']], 'out': [['AND'], ['A17']]},
    'A9': {'in': [['AND'], ['A6']], 'out': [['xOR'], ['A11']]},
    'A10': {'in': [['xOR'], ['A3', 'A5']], 'out': [['AND', 'xOR', 'xOR'], ['A12', 'A13'], ['A14', 'A15']]},
    'A11': {'in': [['AND'], ['A7', 'A9']], 'out': [['AND'], ['A17']]},
    'A12': {'in': [['AND'], ['A10']], 'out': [['AND'], ['A16']]},
    'A13': {'in': [['AND'], ['A10']], 'out': [['AND'], ['A16']]},
    'A14': {'in': [['AND'], ['A10']], 'out': [['AND'], ['A16']]},
    'A15': {'in': [['AND'], ['A10']], 'out': [['AND'], ['A16']]},
    'A16': {'in': [['AND', 'xOR', 'xOR'], ['A12', 'A13'], ['A14', 'A15']], 'out': [['AND'], ['A17']]},
    'A17': {'in': [['AND', 'xOR', 'AND'], ['A8', 'A11'], ['A16']], 'out': [[], []]},
    'inicio': [['AND'], ['A1','A2']],
    'fim': [['AND'], ['A17']]
}

logTraces = {
    'A': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A9'],
    'B': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A8', 'A9'],
    'C': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A8', 'A9'],
    'D': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A7', 'A9']}

logs_art_process02 = {
    'A': ['A1', 'A5', 'A4', 'A7', 'A8'],
    'B': ['A1', 'A4', 'A5', 'A7', 'A8'],
    'C': ['A1', 'A3', 'A2', 'A6', 'A8'],
    'D': ['A1', 'A5', 'A2', 'A6', 'A8'],
    'E': ['A1', 'A2', 'A3', 'A6', 'A8'],
    'F': ['A1', 'A3', 'A4', 'A7', 'A8'],
    'G': ['A1', 'A4', 'A3', 'A7', 'A8'],
    'H': ['A1', 'A2', 'A5', 'A6', 'A8']}

with open('my_jsonprocess03.txt') as fp:
    logs_art_process03 = json.load(fp)

'''setquant = int(len(logs_art_process03) * 1)
max_len_trace = max([len(x) for x in logs_art_process03.values()]) * 4
weights = {'comp': 0.8, 'prec': 0.2}

#result = prc.precision_calc_full(logs_art_process03, ind_teste_complex3altered, setquant, max_len_trace)

result = gops.fitness(CMArtigo28, logTraces, setquant, max_len_trace, weights)

print(result)'''


logTraces = {
    'A': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A9'],
    'B': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A8', 'A9'],
    'C': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A8', 'A9'],
    'D': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A7', 'A9']}


def positional_dict(logs):
    pos_dict = {}
    for key,val in logs.items():
        for i in val:
            if i not in pos_dict.keys():
                pos_dict[i] = {'before':[], 'after':[]}
            i_index = val.index(i)
            pos_dict[i]['before'].extend([boo for boo in val[:i_index] if boo not in pos_dict[i]['before']])
            pos_dict[i]['after'].extend([bar for bar in val[i_index+1:] if bar not in pos_dict[i]['after']])
    return pos_dict

def positional_set(logs):
    # It ends with some extra stuff on the sets when i have concurrent structures, like a and of xORs. Think if there's
    # Some way to correct that
    pos_dict = {}
    for trace in logs:
        for i in trace:
            if i not in pos_dict.keys():
                pos_dict[i] = {'before':set(), 'after':set()}
            i_index = trace.index(i)
            if i_index ==0:
                pos_dict[i]['after'].add(trace[i_index + 1])
            elif 0 < i_index < len(trace)-1:
                pos_dict[i]['before'].add(trace[i_index-1])
                pos_dict[i]['after'].add(trace[i_index+1])
            else:
                pos_dict[i]['before'].add(trace[i_index - 1])
    for foo, bar in pos_dict.items():
        intersect = bar['before'] & bar['after']
        if intersect:
            continue
            # todo for task in that intersection
            # do a symetrical diff between these tasks
            # bar-before =  that diff
        bar['before'] -= intersect # and that intersection
        bar['after'] -= intersect   # and that intersection
    return pos_dict


def positional_precision(artf_pos_dict, ref_pos_dict):
    aux = 0
    for key, value in artf_pos_dict.items():
        # Chose to make a intersection instead if a symmetrical difference
        intersection_af = value['after'] & ref_pos_dict[key]['after']
        # Measuring the length of the intersection
        len_int_af = len(intersection_af)
        # Total length of both sets
        lenght_af_total = len(ref_pos_dict[key]['after']) + len(value['after'])
        # formula: what it got right
        aux += 1 if lenght_af_total == 0 else len_int_af / (lenght_af_total - len_int_af)

        intersection_bf = value['before'] & ref_pos_dict[key]['before']
        len_int_bf = len(intersection_bf)
        lenght_bf_total = len(ref_pos_dict[key]['before']) + len(value['before'])
        aux += 1 if lenght_bf_total == 0 else len_int_bf / (lenght_bf_total - len_int_bf)
    return (aux)/(2*len(artf_pos_dict))

'''uniao entre os sets/total-uniao'''


# reference_pos_dict = positional_set(logTraces)


# for k, t in testedict.items():
#      print(k, '-', t)

artf_pos_dict = {
'A4': {'before': {'A9', 'A7', 'A6'}, 'after': {'A9', 'A4', 'A6'}},
'A6': {'before': {'A9', 'A4', 'A7'}, 'after': {'A9', 'A4', 'A6'}},
'A7': {'before': set(), 'after': {'A6', 'A4', 'A9'}},
'A9': {'before': {'A6', 'A4', 'A7'}, 'after': {'A4', 'A6'}},
}

reference_pos_dict = {}
# todo recalcular o ref dict

max_len = max([len(x) for x in logTraces.values()]) * 4
set_quant = len(logTraces)
art_logs = []
for i in range(set_quant):
    trace = tm.trace_maker(CMArtigo28, max_len)
    if trace[0]:
        art_logs.append(trace[1])


# a_p_d = positional_set(logs_art_process03.values())
# for i, val in sorted(a_p_d.items()):
#     print(i,'-', val)
# result = positional_precision(a_p_d, reference_pos_dict)
# print(result)
reference_pos_dict = {'A7': {'before': {'A6'}, 'after': {'A9'}}, 'A9': {'before': {'A7', 'A8'}, 'after': set()}, 'A8': {'before': {'A6'}, 'after': {'A9'}}, 'process': {'end': {'A9'}, 'start': {'A1'}}, 'A1': {'before': set(), 'after': {'A2'}}, 'A5': {'before': {'A4', 'A3'}, 'after': {'A6'}}, 'A6': {'before': {'A5'}, 'after': {'A7', 'A8'}}, 'A4': {'before': {'A3', 'A2'}, 'after': {'A3', 'A5'}}, 'A3': {'before': {'A4', 'A2'}, 'after': {'A4', 'A5'}}, 'A2': {'before': {'A1'}, 'after': {'A4', 'A3'}}}

# print(prc.causal_precision(CMArtigo28, reference_pos_dict))

for i, k in CMArtigo28.items():
    print(i, k)
print('-----------------------')
result = gops.full_mutation(CMArtigo28, 1)
for i, k in CMArtigo28.items():
    print(i, k)
