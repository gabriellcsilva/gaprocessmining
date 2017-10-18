from numpy import random
import collections as col
import copy as copy

def criarIndividuo(alfabetoTarefas):
    matrizInd = {tarefa: {"in": [[],[]], "out": [[],[]]} for tarefa in alfabetoTarefas}
    matrizInd = col.OrderedDict(sorted(matrizInd.items(), key=lambda t: t[0]))

    #Choosing two tasks to be the beginning and ending of the whole process, and removing them from the inner in/out sets
    sorteioIO = random.choice(alfabetoTarefas, 2, False)
    # removing the task that'll be the input
    alfabeto = list(alfabetoTarefas)
    alfabeto.remove(sorteioIO[0])

    for tarefa, conj in matrizInd.items():
        if tarefa == sorteioIO[1]:
            continue
        else:
            '''Does makes sense to draw 0 tasks for a set?'''
            #TODO: Discuss this with the professor
            #I draw a random integer that will be the amount of tasks in the set
            numTasks = random.randint(1, len(alfabeto)+1)
            #Then i draw #numTasks of tasks in the given alphabet
            draw_set = list(random.choice(alfabeto,numTasks,replace=False))
            #the draw set becomes temporally the output until i sort the logic operators
            conj['out'][1] = draw_set
            #then i fill the causal dependencies between input/output
            for i in draw_set:
                matrizInd[i]['in'][1].append(tarefa)

    #second for loop to decide the logical operators
    alfabeto_logico = ['xOR', 'AND']
    # test_simple_complex = [1,3]
    simple_or_complex = [1]
    for tarefa, conj in matrizInd.items():
        #TODO Put an if statement to filter the empty input case here
        if conj['in'][1]:
            #First i draw the logic operators for the inputs
            choice_in = random.choice(simple_or_complex)
            if choice_in == 1:
                draw_in = random.choice(alfabeto_logico)
                conj['in'][0].append(draw_in)
            elif choice_in == 3:
                draw_in = list(random.choice(alfabeto_logico, 3, replace=True))
                #TODO Test this later, and decide if makes sense to have three equal logic ops or if i shoud sort the first separately.
                #TODO also, if it has replacement of elements
                conj['in'][0].extend(draw_in)

                ###Splitting the task set between the two last logic operators
                #set low and high limits
                low = 0
                high = len(conj['in'][1]) + 1
                #choosing where to split the set
                choice_split = random.randint(low, high)
                #making the left (a) and right (b) sets
                split_a = conj['in'][1][:choice_split]
                split_b = conj['in'][1][choice_split:]
                conj['in'][1] = split_a
                conj['in'].append(split_b)

        #Then for the outputs
        # TODO Put an if statement to filter the empty output here
        if conj['out'][1]:
            choice_out = random.choice(simple_or_complex)
            if choice_out == 1:
                draw_out = random.choice(alfabeto_logico)
                conj['out'][0].append(draw_out)
            elif choice_out == 3:
                draw_out = list(random.choice(alfabeto_logico, 3, replace=True))
                # TODO Test this later, and decide if makes sense to have three equal logic ops or if i shoud sort the first separately.
                # TODO also, if it has replacement of elements
                conj['out'][0].extend(draw_out)

                ###Splitting the task set between the two last logic operators
                # set low and high limits
                low = 0
                high = len(conj['out'][1]) + 1
                # choosing where to split the set
                choice_split = random.randint(low, high)
                # making the left (a) and right (b) sets
                split_a = conj['out'][1][:choice_split]
                split_b = conj['out'][1][choice_split:]
                conj['out'][1] = split_a
                conj['out'].append(split_b)
        """PROBLEMA: COMO CONSTRUIR OS INDIVIDUOS COM CONJUNTOS DE TRÊS OPERADORES LÓGICOS NO IN/OUT, FAZER O SORTEIO E
        DEPOIS DECIDIR OS OPERADORES OU O INVERSO DISSO?"""

    #Filling the process begin and end sets

    begin_set = [[],[]]
    end_set = [[],[]]

    # Reading the matrix to find the tasks that have their input;output empty (therefore they are respectively begin;end
    # Of the process

    for tarefa, conj in matrizInd.items():
        #  the logic here is that if a task's in/out set doesn't have a logic operator on its first position, then there's
        #  no tasks on the given set (in the second and third position)
        if not conj['in'][0]:
            begin_set[1].append(tarefa)

        if not conj['out'][0]:
            end_set[1].append(tarefa)

    # Choosing two logic operations for the begin/end of the process
    begin_end_logic = random.choice(alfabeto_logico,2)
    begin_set[0] = [begin_end_logic[0]]
    end_set[0] = [begin_end_logic[1]]
    # Assigning the begin/end sets to the matrix structure
    # Think on what's the best notation, this way:
    #matrizInd['processo'] = {'inicio': begin_set, 'fim': end_set}
    # Or this way:
    matrizInd['inicio'] = begin_set
    matrizInd['fim'] = end_set


    return matrizInd

# TODO problem: when a complex structure has tasks in one side but nothing in the other side, the other side is not
# TODO pointing to the end right now. Question is, it should? Do i want this? What would be the consequences if it does
# TODO or don't ?