import trace_maker as trmk
import numpy as np


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
            unique_in_common.append(i) #17.56

    # TODO OBs.: this diff_size only works if i generate enough traces so i can reach the same traces in the given log.
    # TODO While this is correct to do, maybe this will not be feasible for processes with too many diff traces
    diff_size = len(unique_in_common) - len(log)
    print(diff_size)
    precision = len(in_common)/len(artf_log) + diff_size
    print(precision)

    #precision = len(in_common)/ len(artf_log) ... forma anterior de calcular
    return [precision, artf_log, len(artf_log), in_common]

def precision_calc_heur(log, ind, set_quant, max_len_trace):
    """This method is more heuristic, and it works with small values for set_quant. The bigger it is, the less false
    Tpositives there'll be"""
    # The set of traces i use as reference
    log = log.values()
    # Creating a set of logs to check the precision
    generated_log = [trmk.trace_maker(ind, max_len_trace) for _ in range(set_quant)]
    # In_common contains only the traces that were finished and that are in the reference log
    in_common = [_[1] for _ in generated_log if _[0] and (_[1] in log)]
    print(in_common)
    # I could also be radical and set precision to 0 if at least one of the traces wasn't on the log
    return len(in_common)/len(generated_log)


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