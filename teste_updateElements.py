import GeneticOps as gops

CMArtigo28 = {
    'A1': {'in':[], 'out':['A2']},
    'A2': {'in':['A1'], 'out':['A3', 'A4']},
    'A3': {'in':['A2'], 'out':['A5']},
    'A4': {'in':['A2'], 'out':['A5']},
    'A5': {'in':['A3', 'A4'], 'out':['A6']},
    'A6': {'in':['A5'], 'out':[['A7','A8']]},
    'A7': {'in':['A6'], 'out':['A9']},
    'A8': {'in':['A6'], 'out':['A9']},
    'A9': {'in':[['A7','A8']], 'out':[]}
}
task_name = 'A1'
#task = CMArtigo28[task_name].copy()
task = {'in':[], 'out':['A2']}

print('esse é o set escolhido', task)

for i, val in CMArtigo28.items():
    print(i, '\t', val)

print('\n')
ind = gops.update_elements(CMArtigo28, task, task_name, 'remove')

for j, val in CMArtigo28.items():
    print(j,'\t',val)

print('esse é o set escolhido de novo', task)

print('\n')
ind = gops.update_elements(CMArtigo28, task, task_name, 'add')

for j, val in CMArtigo28.items():
    print(j,'\t',val)