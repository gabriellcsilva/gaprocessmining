import pandas as pd
import openpyxl as oxl


def translate_eventname(ename):
    dict_events = {
        'user logout' : 'A',
        'resource view':'B',
        'url view' : 'C',
        'course view' : 'D',
        'user login' : 'E',
        'page view' : 'F',
        'workshop view' : 'G',
        'assignment view' : 'H',
        'assignment upload' : 'I',
        'blog view' : 'J',
        'user view all' : 'K',
        'user view' : 'L',
        'user change password' : 'M',
        'data view' : 'N',
        'message write' : 'O',
        'user update' : 'P',
        'data add' : 'Q',
        'data update' : 'R',
        'blog update' : 'S',
        'blog add' : 'T',
        'forum view forum' : 'U',
        'assignment view all' : 'V',
        'data record delete' : 'X',
        'library mailer' : 'Y',
        'login error': 'Z'}
    return dict_events[ename]


def preprocess_log(filepath):
    wblog = oxl.load_workbook(filepath)
    wslog = wblog['Sheet1']
    dflog = pd.DataFrame(wslog.values)

    a = len(dflog)
    count = 0
    dict_traces = {}
    current_id_trace = ''
    for i in range(len(dflog)):
        if dflog.iloc[i][4] == 'user login':
            # print('line', i+1, dflog.iloc[i][4])
            current_id_trace = str(i+1)
            dict_traces[current_id_trace] = [translate_eventname(dflog.iloc[i][4])]
        else:
            dict_traces[current_id_trace].append(translate_eventname(dflog.iloc[i][4]))
            # print('naynaynay')
            # print(delta)
    return dict_traces

# def preprocess_log(filepath):
#     wblog = oxl.load_workbook(filepath)
#     wslog = wblog['Sheet1']
#     dflog = pd.DataFrame(wslog.values)
#
#     # How to sort by column and index, when the column doesn't have a key name
#     # dfsorted_datetime = dflog.sort_values(by=1).sort_index(ascending=False) # Not necessary
#     # df_sorted = dflog.sort_index(ascending=False)  # I just need to invert the index
#
#     # writer = pd.ExcelWriter('newevclog-fabio.xlsx')
#     # df_sorted.to_excel(writer, header=False, index=False)
#     # writer.save()
#     a = len(dflog)
#
#     count = 0
#     for i in range(len(dflog)-1):
#         timea = dflog.iloc[i][1]
#         timeb = dflog.iloc[i+1][1]
#         delta = timeb - timea
#         if delta >= pd.Timedelta('3 hours'):
#             count +=1
#             # print(delta)
#             # print(i)
#             # print('the current event is - ', dflog.iloc[i][4])
#             # print('the next event is ')
#             # print(dflog.iloc[i+1][4])
#             if dflog.iloc[i+1][4] != 'user login':
#                 print('line', i+1, dflog.iloc[i+1][4])
#         else:
#             count+=1
#             # print('naynaynay')
#             # print(delta)
#     print(count)

a = preprocess_log('testeFabio.xlsx')

setaux = set()
for trace in a.values():
    setaux.add(tuple(trace))

# print(setaux)


# TODO i need to add the user logout to the end and reacess how many different traces are there

index = 0
newdict = {}
for foo in setaux:
    newdict[index] = list(foo)
    if newdict[index][-1] != 'A':
        newdict[index].append(translate_eventname('user logout'))
    index+=1
print(newdict.items())

# # df2 = pd.DataFrame.from_dict(newdict, orient='index')
# df2 = pd.DataFrame([newdict.values()]).transpose()
# print(df2)
#
#
# dfwriter = pd.ExcelWriter('log-traces-translated-fabio2m.xlsx')
# df2.to_excel(dfwriter, header=False, index=False)
# dfwriter.save()


