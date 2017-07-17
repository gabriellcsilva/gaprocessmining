import itertools as itertools
import evolCicle as evolc

alfa = ["A1","A2","A3","A4","A5","A6","A7","A8","A9"]

logs = {
        'A': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A9'],
        'B': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A8', 'A9'],
        'C': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A8', 'A9'],
        'D': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A7', 'A9']}

params = [
    [1500]
    ,[60]
    ,[0.2, 0.4, 0.6, 0.8, 1]
    ,[0.2, 0.4, 0.6, 0.8, 1]
    ,[0.2, 0.4, 0.6, 0.8, 1]
    ]

list_params = list(itertools.product(*params))
count = 100
for i in list_params[:100]:
    print(count)
    for j in range(5):
        #print(str(i) + '_' + str(j))
        evolc.evolCicle(*i,alfa, logs, j)
    count-=1
#for i in range(5):
#    evolc.evolCicle()

#unique_data = [list(x) for x in set(tuple(x) for x in a)]
