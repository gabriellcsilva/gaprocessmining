import traceMaker as trmk
import numpy as np

def precisionCalc(log, ind, set_quant):
    log = log.values()

    artf_log = [trmk.traceMaker(ind, log) for _ in range(set_quant)]

    in_common = [_ for _ in artf_log if _ in log]
    diff_size = len(in_common) - len(log)

    precision = len(in_common)/(len(artf_log) + diff_size)
    #precision = len(in_common)/ len(artf_log) ... forma anterior de calcular
    return [precision, artf_log, len(artf_log), in_common]


def precisionCalc2(log, ind, set_quant):
    log = log.values()
    artf_log = []
    aux_precision = 0
    for i in range(set_quant):
        result = trmk.traceMaker(ind, log)
        artf_log.append(result)

    for j in artf_log:
        if j in log:
            aux_precision += 1
    precision = aux_precision/len(artf_log)
    return [precision, artf_log, len(artf_log), aux_precision]


#Consider only unique values in the artificial log
def precisionCalcUnique(log, ind, set_quant):
    log = log.values()
    log = set(map(tuple,log))

    artf_log = [trmk.traceMaker(ind, log) for _ in range(set_quant)]

    artf_log = set(map(tuple,artf_log))

    in_common = [_ for _ in artf_log if _ in log]

    precision = len(in_common)/len(artf_log)
    return [precision, artf_log, len(artf_log), in_common]