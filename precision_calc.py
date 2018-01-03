import trace_maker as trmk


def precision_calc_full(log, ind, set_quant, max_len_trace):
    # TODO i'm making this legacy because the whole diff_size thing is unnecessary by what i can think of it rn
    # This precision calc method works only if set_quant is big enough so i can obtain every possible
    # trace in the log. While this is good for small structured processes (because it's very exact), this makes the
    # calculation too penalizing on performance. The intention of this approach on process precision was to be a heuristic
    # and not a exact method.
    log = log.values()

    # TODO i might need to make the 'log' list be unique if in some occasion the real log have non unique values...

    # This makes a bunch of traces, finished and non-finished ones, accordingly to the amount set
    artf_log = [trmk.trace_maker(ind, max_len_trace) for _ in range(set_quant)]
    # Then i check only the traces finished, that is, if the first position of the entry is true
    # and then i check if the artificial trace is part of the real log
    in_common = [_[1] for _ in artf_log if _[0] and (_[1] in log)]
    unique_in_common = []

    for i in in_common:
        if i not in unique_in_common:
            unique_in_common.append(i)  # 17.56

    # TODO OBs.: this diff_size only works if i generate enough traces so i can reach the same traces in the given log.
    # TODO While this is correct to do, maybe this will not be feasible for processes with too many diff traces
    diff_size = len(unique_in_common) - len(log)
    precision = len(in_common) / len(
        artf_log) + diff_size  # This diff_size catches if the artf_log didn't generated all possible traces
    '''But this also can be a flaw, if the original log have repeated traces'''
    # precision = len(in_common)/ len(artf_log) ... simpler way of calculating
    # return [precision, artf_log, len(artf_log), in_common]
    return precision


def precision_calc_heur(log, ind, set_quant, max_len_trace, ref_pos_dict):
    """This method is more heuristic, and it works with small values for set_quant. The bigger it is, the less false
    positives there'll be"""
    # The set of traces i use as reference
    log = log.values()
    # Creating a set of logs to check the precision
    generated_log = [trmk.trace_maker(ind, max_len_trace) for _ in range(set_quant)]
    # In_common contains only the traces that were finished and that are in the reference log
    in_common = [_[1] for _ in generated_log if _[0] and (_[1] in log)]

    # Calculating the positional precision
    gen_log = [_[1] for _ in generated_log if
               _[0]]  # this gets all traces that were finished, no matter if they're in the log
    if len(gen_log) == 0:  # if the process failed to generate even one valid trace
        positional_prec = 0
    else:
        artf_pos_dict = positional_set(gen_log)
        positional_prec = positional_precision(artf_pos_dict, ref_pos_dict)
    # Calculating the causal precision
    c_precision = causal_precision(ind, ref_pos_dict)

    # TODO i could add a extra punishment by adding the diff between in_common and generated_log
    return [len(in_common) / len(generated_log), positional_prec, c_precision]


def precision_calc_heur_pos_corrected(log, ind, set_quant, max_len_trace, ref_pos_dict):
    """This method is more heuristic, and it works with small values for set_quant. The bigger it is, the less false
    positives there'll be"""
    '''I THINK IT'S OF NO USE, DOING THE POS-PRECISION BY SINGLE TRACE DOESN'T GUIDE IT TO FIT THE WHOLE LOG SET, BUT
    ONLY SINGLE TRACES'''
    # The set of traces i use as reference
    log = log.values()
    # Creating a set of logs to check the precision
    generated_log = [trmk.trace_maker(ind, max_len_trace) for _ in range(set_quant)]
    # In_common contains only the traces that were finished and that are in the reference log
    in_common = [_[1] for _ in generated_log if _[0] and (_[1] in log)]

    # Calculating the positional precision
    gen_log = [_[1] for _ in generated_log if
               _[0]]  # this gets all traces that were finished, no matter if they're in the log

    if len(gen_log) == 0:  # if the process failed to generate even one valid trace
        positional_prec = 0
    else:
        positional_prec = 0
        for trace in gen_log:
            artf_pos_dict = positional_set([trace])  # I had to make it a list of one list
            print(artf_pos_dict)
            aux = positional_precision(artf_pos_dict, ref_pos_dict)  # just not to modify this function
            positional_prec += aux
        positional_prec = positional_prec/len(gen_log)
    # Calculating the causal precision
    c_precision = causal_precision(ind, ref_pos_dict)

    # TODO i could add a extra punishment by adding the diff between in_common and generated_log
    return [len(in_common) / len(generated_log), positional_prec, c_precision]


''' Legacy 
def positional_set(logs): # I coudn't trust the sets it generates
    pos_dict = {}
    for val in logs:
        for i in val:
            if i not in pos_dict.keys():
                pos_dict[i] = {'before': set(), 'after': set()}
            i_index = val.index(i)
            pos_dict[i]['before'].update(val[:i_index])
            pos_dict[i]['after'].update(val[i_index + 1:])
    return pos_dict'''


def positional_set(logs):
    # It ends with some extra stuff on the sets when i have concurrent structures, like a and of xORs. Think if there's
    # Some way to correct that
    pos_dict = {'process': {'start': set(), 'end': set()}}
    for trace in logs:
        for k, i in enumerate(trace):
            if i not in pos_dict.keys():
                pos_dict[i] = {'before': set(),
                               'after': set()}  # Inicializing the sets for given task if it's not already
            i_index = k  # Getting the position of the task in the trace
            if i_index == 0:
                # This extra condition is when i have a trace with only one task
                if i_index == len(trace) - 1:
                    pos_dict['process']['start'].add(i)
                    pos_dict['process']['end'].add(i)
                else:
                    pos_dict[i]['after'].add(trace[i_index + 1])
                    pos_dict['process']['start'].add(i)

            elif i_index < len(trace) - 1:
                pos_dict[i]['before'].add(trace[i_index - 1])
                pos_dict[i]['after'].add(trace[i_index + 1])
            else:
                pos_dict[i]['before'].add(trace[i_index - 1])
                pos_dict['process']['end'].add(i)
    '''for foo, bar in pos_dict.items():
        intersect = bar['before'] & bar['after']
        bar['before'] -= intersect
        bar['after'] -= intersect'''
    return pos_dict


def positional_precision(artf_pos_dict, ref_pos_dict):
    aux = 0
    for key, value in artf_pos_dict.items():
        after,before = ('start','end') if key == 'process' else ('after', 'before')

        # Chose to make a intersection instead if a symmetrical difference
        intersection_af = value[after] & ref_pos_dict[key][after]
        # Measuring the length of the intersection
        len_int_af = len(intersection_af)
        # Total length of both sets
        length_af_total = len(ref_pos_dict[key][after]) + len(value[after])
        # formula: what it got right
        aux += 1 if length_af_total == 0 else len_int_af / (length_af_total - len_int_af)

        intersection_bf = value[before] & ref_pos_dict[key][before]
        len_int_bf = len(intersection_bf)
        length_bf_total = len(ref_pos_dict[key][before]) + len(value[before])
        aux += 1 if length_bf_total == 0 else len_int_bf / (length_bf_total - len_int_bf)

    # this task ration penalizes if the individual have less tasks than it should have
    task_ratio = (len(artf_pos_dict)-1) / (len(ref_pos_dict)-1)
    pos_precision = (aux) / (2 * len(artf_pos_dict))
    # TODO Deveria ser pos_precision = (aux) / (2 * len(artf_pos_dict)), porque eu percorro artf_pos_dict
    # No entanto devido as circunstâncias em que eu programei, aparentemente não deve fazer diferença

    return pos_precision * task_ratio


def causal_precision(ind, ref_pos_dict):
    # In this method i wanna allow the individual to have in it's in/out sets only tasks that he is related on the logs
    # But not all, i wanna penalize if it has tasks unrelated, but not to force all tasks related to be there
    # I only wanna penalize if it has no tasks (and the reference has) or if it has tasks non present in the set
    aux = 0
    for task, value in ind.items():
        if task not in ('inicio', 'fim'):
            set_input = set()
            set_input.update(*value['in'][1:]) # passing the input to a set so i can operate
            intersect_in = set_input & ref_pos_dict[task]['before'] # Catching the tasks that are in both sets
            if len(set_input) and len(ref_pos_dict[task]['before']) == 0: # if the task is in the beginning and the process got it right (no tasks)
                aux+=1
            elif len(set_input)>0:
                aux+=len(intersect_in)/len(set_input)
            # Same thing for output
            set_output = set()
            set_output.update(*value['out'][1:])  # passing the input to a set so i can operate
            intersect_out = set_output & ref_pos_dict[task]['after']  # Catching the tasks that are in both sets
            if len(set_output) and len(ref_pos_dict[task]['after']) == 0:
                aux += 1
            elif len(set_output) > 0:
                aux += len(intersect_out) / len(set_output)
        else:
            compare_to = 'start' if task == 'inicio' else 'end'
            set_process = set()
            set_process.update(value[1])
            # passing the input to a set so i can operate
            intersect = set_process & ref_pos_dict['process'][compare_to]  # Catching the tasks that are in both sets
            aux += len(intersect) / len(set_process) # Since i'll always have a beginning in the process and in the
            # Reference set, no need to test the length of them
    c_precision = (aux) / (2 * (len(ref_pos_dict)-1))
    return c_precision

    # def precisionCalc2(log, ind, set_quant):
    #     log = log.values()
    #     artf_log = []
    #     aux_precision = 0
    #     for i in range(set_quant):
    #         result = trmk.trace_maker(ind, max_len_trace)
    #         artf_log.append(result)
    #
    #     for j in artf_log:
    #         if j in log:
    #             aux_precision += 1
    #     precision = aux_precision/len(artf_log)
    #     return [precision, artf_log, len(artf_log), aux_precision]
    #
    #
    # #Consider only unique values in the artificial log
    # def precisionCalcUnique(log, ind, set_quant):
    #     log = log.values()
    #     log = set(map(tuple,log))
    #
    #     artf_log = [trmk.trace_maker(ind, max_len_trace) for _ in range(set_quant)]
    #
    #     artf_log = set(map(tuple,artf_log))
    #
    #     in_common = [_ for _ in artf_log if _ in log]
    #
    #     precision = len(in_common)/len(artf_log)
    #     return [precision, artf_log, len(artf_log), in_common]
