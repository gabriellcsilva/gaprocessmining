import matplotlib.pyplot as plt
def plot_evolution(vetor_fitness, exec_id_name):
# Plotting stuff
    v_max = [i[1] for i in vetor_fitness]
    v_min = [i[0] for i in vetor_fitness]
    v_avg = [i[2] for i in vetor_fitness]
    plt.plot(v_avg, label="Média", linewidth=2.0, color="orange")
    plt.plot(v_max, label="Maior fitness", linewidth=2.0, color="green")
    plt.plot(v_min, label="Menor Fitness", linestyle=':', linewidth=1.0, color="red")
    plt.ylabel("Fitness")
    plt.xlabel("Gerações")
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=4, ncol=2, mode="expand", borderaxespad=0., prop={'size': 10})
    plt.ylim([-20, 1])

    # plt.savefig(exec_id_name)
    plt.show()
    plt.clf()
