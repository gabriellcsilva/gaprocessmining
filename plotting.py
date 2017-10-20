import matplotlib.pyplot as plt
def plot_evolution(vetor_fitness, exec_id_name):
    # Plotting stuff
    v_min = [i[0] for i in vetor_fitness]
    v_max = [i[1] for i in vetor_fitness]
    v_avg = [i[2] for i in vetor_fitness]

    # Figure for the maximum fitness evolution
    plt.figure(1)
    plt.plot(v_max, label="Maior fitness", linewidth=2.0, color="green")
    plt.ylabel("Fitness")
    plt.xlabel("Gerações")
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=4, ncol=2, mode="expand", borderaxespad=0., prop={'size': 10})
    plt.ylim([-20, 1])
    plt.draw()
    name = exec_id_name + '-maior-fit.png'
    plt.savefig(name)
    plt.clf()

    # Figure for the minimum fitness evolution
    plt.figure(2)
    plt.plot(v_min, label="Menor Fitness", linestyle=':', linewidth=1.0, color="red")
    plt.ylabel("Fitness")
    plt.xlabel("Gerações")
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=4, ncol=2, mode="expand", borderaxespad=0., prop={'size': 10})
    # plt.ylim([-20, 1])
    plt.draw()
    name = exec_id_name + '-pior-fit.png'
    plt.savefig(name)
    plt.clf()

    # Figure for the average fitness evolution
    plt.figure(3)
    plt.plot(v_avg, label="Média", linewidth=2.0, color="orange")
    plt.ylabel("Fitness")
    plt.xlabel("Gerações")
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=4, ncol=2, mode="expand", borderaxespad=0., prop={'size': 10})
    # plt.ylim([-20, 1])
    plt.draw()
    name = exec_id_name + '-media-fit.png'
    plt.savefig(name)
    plt.clf()

    return
