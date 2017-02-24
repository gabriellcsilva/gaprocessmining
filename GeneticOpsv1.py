def Fitness(ind, traces, alfabeto):

    enabled = []
    or_enabled = []
    token_table = {x: 0 for x in alfabeto}
    parsed = 0
    penalty = 0
    score = 0

    for i, val in traces.items():
        #Idéia: talvez separar o caso inicial, fazendo um slice no traço de eventos
        #Obs.: Talvez esvaziar o or_enabled não seja uma boa idéia, caso por exemplo sejam acumuladas saídas OR de nós
        #diferentes, esvaziar tudo eliminaria os tokens dos ORs anteriores
        for j in val:
            ##pra simplificar, vou considerar que as relações de in/out são 'puras' (OR ou AND/Seq)

            #caso o evento atual seja o inicio - input vazio
            if not ind[j]['in']:
                parsed +=1

                try:
                    if isinstance(ind[j]['out'][0], list):
                        #print('não devia entrar aqui')
                        or_enabled.extend(ind[j]['out'][0])
                    else:
                        #print('devia entrar aqui')
                        enabled.extend(ind[j]['out'])
                except:
                    print('fimSEQ')
                    #enabled.extend(ind[j]['out'])

            #Caso o input do evento atual seja um OR
            elif isinstance(ind[j]['in'][0],list):
                print('aqui')
                #print(ind[j]['in'])

                flag_or = 0
                for k in ind[j]['in'][0]:
                    #se eu achar pelo menos um do input na lista dos possivelmente habilitados
                    if k in or_enabled:
                        #print(k)
                        #print(or_enabled)
                        parsed += 1
                        flag_or = 1
                        #or_enabled = []
                        or_enabled.remove(k)

                        #habilitando o output da tarefa
                        try:
                            if isinstance(ind[j]['out'][0], list):
                                or_enabled.extend(ind[j]['out'][0])
                            else:
                                enabled.extend(ind[j]['out'])
                        except:
                            print('fimOR')
                        break
                        #testar se está mesmo quebrando o for

                #Se não entrar no if, ou seja, nenhuma tarefa do OR estiver habilitada, é aplicada a punição
                if flag_or==0:
                    #print('aqui não deveria entrar')
                    #print(penalty,'penalidade MÁXIMA')
                    penalty += len(ind[j]['in'])
                    parsed += 1
                    #or_enabled = []

                    # habilitando o output da tarefa
                    try:
                        if isinstance(ind[j]['out'][0], list):
                            or_enabled.extend(ind[j]['out'][0])
                        else:
                            enabled.extend(ind[j]['out'])
                    except:
                        print('fimOR')

            #caso o input do evento seja um AND ou uma sequência
            else:
                #print(ind[j]['in'])
                aux = 0
                for k in ind[j]['in']:
                    if k in enabled:
                        print(k)
                        print(enabled)
                        enabled.remove(k)
                        print(enabled)
                        aux += 1
                penalty += len(ind[j]['in']) - aux
                #print(penalty)
                parsed += 1

                try:
                    if isinstance(ind[j]['out'][0], list):
                        or_enabled.extend(ind[j]['out'][0])
                    else:
                        enabled.extend(ind[j]['out'])
                except:
                    print('fimAnd')

        '''limpando as listas auxiliares'''

        enabled = []
        or_enabled = []


    total_len_traces = sum([len(x) for x in traces.values()])


    return [parsed, total_len_traces, penalty]