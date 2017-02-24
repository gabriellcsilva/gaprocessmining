def Fitness(ind, traces, alfabeto):

    enabled = []
    or_enabled = []
    token_table = {x: 0 for x in alfabeto}
    #OBS.: Faz sentido zerar a tabela de tokens de um traço pra outro?
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
                        #or_enabled.extend(ind[j]['out'][0])
                        token_table[j] += 1
                    else:
                        #print('devia entrar aqui')
                        #enabled.extend(ind[j]['out'])
                        token_table[j] += len(ind[j]['out'])
                except:
                    True
                    #enabled.extend(ind[j]['out'])

            #Caso o input do evento atual seja um OR
            elif isinstance(ind[j]['in'][0],list):
                print('Caso 2')
                #print(ind[j]['in'])

                flag_or = 0
                for k in ind[j]['in'][0]:
                    #se eu achar pelo menos um do input na lista dos possivelmente habilitados
                    if token_table[k] >= 1:
                        #print(k)
                        #print(or_enabled)
                        parsed += 1
                        flag_or = 1
                        #or_enabled = []
                        # or_enabled.remove(k)
                        #print(token_table)
                        token_table[k] -= 1

                        #habilitando o output da tarefa
                        try:
                            if isinstance(ind[j]['out'][0], list):
                                #or_enabled.extend(ind[j]['out'][0])
                                token_table[j] += 1
                            else:
                                #enabled.extend(ind[j]['out'])
                                token_table[j] += len(ind[j]['out'])
                        except:
                            print('fimOR2')
                        break
                        #testar se está mesmo quebrando o for

                #Se não entrar no if, ou seja, nenhuma tarefa do OR estiver habilitada, é aplicada a punição
                if flag_or==0:
                    #print('aqui não deveria entrar')
                    #print(penalty,'penalidade MÁXIMA')
                    #penalty += len(ind[j]['in'])
                    penalty += 1
                    parsed += 1
                    #or_enabled = []

                    # habilitando o output da tarefa
                    try:
                        if isinstance(ind[j]['out'][0], list):
                            #or_enabled.extend(ind[j]['out'][0])
                            token_table[j] += 1
                        else:
                            #enabled.extend(ind[j]['out'])
                            token_table[j] += len(ind[j]['out'])
                    except:
                        print('fimOR1')

            #caso o input do evento seja um AND ou uma sequência
            else:
                #print(ind[j]['in'])
                aux = 0
                for k in ind[j]['in']:
                    if token_table[k] >= 1:

                        token_table[k] -= 1
                        aux += 1
                print(aux)
                penalty += len(ind[j]['in']) - aux
                #print(penalty)
                parsed += 1

                try:
                    if isinstance(ind[j]['out'][0], list):
                        #or_enabled.extend(ind[j]['out'][0])
                        token_table[j] += 1
                    else:
                        #enabled.extend(ind[j]['out'])
                        token_table[j] += len(ind[j]['out'])
                except:
                    print('fimAnd')

        '''limpando as listas auxiliares'''

        enabled = []
        or_enabled = []
        print('end')


    total_len_traces = sum([len(x) for x in traces.values()])


    return [parsed, total_len_traces, penalty, token_table]