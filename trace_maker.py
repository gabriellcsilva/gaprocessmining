import numpy as np

def trace_maker (individuo, max_len_trace):
    trace = []
    active = []
    # token_table = {x: [] for x in individuo.keys()}

    active.append(individuo['inicio'][:])

    while active and max_len_trace > 0:
        max_len_trace -= 1
        choice = np.random.choice(active, 1, False)
        result = choice_maker()



    return trace

def search_table():
    exit()
    return

def choice_maker(logic_struct):
    if len(logic_struct[0]) == 1:

