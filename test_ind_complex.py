'''a = [['AND', 'OR', 'OR'],['t','f'],['f','f']]

b = [['AND'],[True, False]]

c = [['OR'], [False, True]]


if a[0][0] = 'AND':'''


import individuo_complex as indc
alfabeto_tasks = ('A1', 'B2', 'C3', 'D4', 'E5', 'F6')
test = ('A1','A2','A3','A4','A5','A6')
teste = indc.criarIndividuo(test)

for i, val in teste.items():
    print('Tarefa ', i, ' ---> ', val)


if teste['inicio'][0][0] == 'xOR':
    print('success xor')
elif teste['inicio'][0][0] == 'AND':
    print('sucess and')
else:
    print('fail')
