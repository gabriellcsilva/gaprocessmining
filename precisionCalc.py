import traceMaker as trmk

def precisionCalc(log, ind, set_quant):
    log = log.values()
    artf_log = []
    aux_precision = 0
    for i in range(set_quant):
        result = trmk.traceMaker(ind)
        artf_log.append(result)

    for j in artf_log:
        if j in log:
            aux_precision += 1
    precision = aux_precision/len(artf_log)
    return [precision, artf_log, len(artf_log), aux_precision]