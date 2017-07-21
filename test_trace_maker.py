import trace_maker as tm

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


result = tm.trace_maker(CMArtigo28, 9)

print(result)

