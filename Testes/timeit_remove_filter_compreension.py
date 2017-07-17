import timeit as timeit


# setup 1, using remove
print('setup 1 ')
print(timeit.timeit('''
token_set_r = ["A1","A2","A3","A4","A5","A6","A7","A8","A9"]
logA = {
    'A': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A9']}

for trace_id, trace in logA.items():
    for task in trace:
        if task in token_set_r:
            token_set_r.remove(task)
''',number = 1000000))


# setup 2, using filter
print('setup 2 ')
print(timeit.timeit('''
token_set_f = ["A1","A2","A3","A4","A5","A6","A7","A8","A9"]
logB = {
    'A': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A9']}

for trace_id, trace in logB.items():
    for task in trace:
        token_set_f = list(filter(lambda l: l != task, token_set_f))

    ''', number= 1000000))


# setup 3, using comprehension:
print('setup 3 ')
print(timeit.timeit('''
token_set_c = ["A1","A2","A3","A4","A5","A6","A7","A8","A9"]
logC = {
    'A': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A9']}

for trace_id, trace in logC.items():
    for task in trace:
        token_set_c = [task_c for task_c in token_set_c if task_c != task]
''', number = 1000000))
