from portfolioParameters import Parameters
import matplotlib.pyplot as plt
import numpy as np

pr = Parameters()
markers = ['o', 'D', 's', 'X', '*', '^', '>', '<', 'P', '1', '2', 'v', '3', '4', '+']
lines = ['-', '--', '-.', ':']
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']


def plot_scenarios(n_scen, plot_together, p_spot, GSF):
    """

    :param n_scen:
    :param plot_together: True or False
    :return:
    """
    possible_prices = np.zeros([n_scen, pr.T])
    possible_GSF_asset = np.zeros([pr.n, n_scen, pr.T])
    for s in range(n_scen):
        possible_prices[s, :] = p_spot[s, :]
        for i in range(pr.n):
            possible_GSF_asset[i, s, :] = GSF[i, :, s]
    x_axis = np.arange(pr.T)+1
    #
    # plot scenarios
    if plot_together:
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        aux = 0
        aux_line = 0
        for s in range(n_scen):

            color = 'tab:blue'
            ax1.set_xlabel('time (years)')
            ax1.set_ylabel('spot price', color=color)
            ax1.plot(x_axis, possible_prices[s, :], color=color, label='scenario '+str(s), ls=lines[aux_line],
                     marker=markers[aux])
            ax1.tick_params(axis='y', labelcolor=color)

            color = 'tab:red'
            ax2.set_ylabel('GSF', color=color)  # we already handled the x-label with ax1
            ax2.plot(x_axis, possible_GSF_asset[i, s, :], color=color, label='scenario '+str(s), ls=lines[aux_line],
                     marker=markers[aux])
            ax2.tick_params(axis='y', labelcolor=color)

            fig.tight_layout()  # otherwise the right y-label is slightly clipped
            aux_line += 1
            if aux_line == 4:
                aux_line = 0
                aux += 1
        plt.legend()
        plt.show()
    else:
        aux = 0
        aux_line = 0
        for s in range(n_scen):
            #
            # price
            color = colors[aux]
            plt.xlabel('time (years)')
            plt.ylabel('spot price ($/MWh)')
            plt.plot(x_axis, possible_prices[s, :], color=color, label='scenario ' + str(s), ls=lines[aux_line],
                     marker=markers[aux])
            aux += 1
            if aux == 7:
                aux = 0
                aux_line += 1
        plt.legend()
        plt.show()
        aux = 0
        aux_line = 0
        for s in range(n_scen):
            #
            # GSF
            color = colors[aux]
            plt.ylabel('GSF Hydro')  # we already handled the x-label with ax1
            plt.plot(x_axis, possible_GSF_asset[i, s, :], color=color, label='scenario ' + str(s),
                     ls=lines[aux_line],
                     marker=markers[aux])
            aux += 1
            if aux == 7:
                aux = 0
                aux_line += 1
        plt.legend()
        plt.show()
