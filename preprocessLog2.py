import openpyxl as oxl
import pandas as pd

def preprocess_log_general(filepath):
    wblog = oxl.load_workbook(filepath)
    wslog = wblog.worksheets[0]
    dflog = pd.DataFrame(wslog.values)

    a = len(dflog)
    count = 0
    dict_traces = {}
    for k,i in dflog.iterrows():
        if i[0] not in dict_traces.keys():
            dict_traces[i[0]] = [i[1]]
        else:
            dict_traces[i[0]].append(i[1])

    return dict_traces


a = preprocess_log_general('ETM_Configuration1.xlsx')

setaux = set()
for trace in a.values():
    setaux.add(tuple(trace))

a = {i: val for i, val in enumerate(setaux)}
print(a)