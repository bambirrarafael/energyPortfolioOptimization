import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
from plotScenarios import plot_scenarios
from portfolioParameters import Parameters
from findSolutions import find_solutions
from findSolutions import find_harmonious_solution
from findFunctionValues import find_function_values
from setOptmizationBounds import adjust_bounds
from adjustScenarios import adjust_PLD
from adjustScenarios import adjust_GSF
from normalizeSolutions import normalize_solution
from objectiveFunctions import npv_cost
from objectiveFunctions import vol_cost
from objectiveFunctions import vol_gfis
from objectiveFunctions import res_diversity
from portfolioCharacteristcs import calc_exposure
from portfolioCharacteristcs import calc_res
from portfolioCharacteristcs import calc_req
from buildPayoffMatrixes import build_payoff_cost
from buildPayoffMatrixes import build_payoff_vol_cost
from buildPayoffMatrixes import build_payoff_vol_gfis
from buildPayoffMatrixes import build_payoff_div
from buildPayoffMatrixes import add_sol_nothing
from buildPayoffMatrixes import add_sol_nothing_2_obj
from XFModel import build_regret_matrix
from XFModel import build_choice_criteria_matrix
from XFModel import build_normalized_choice_criteria_matrix


#
# initial parameters
pr = Parameters()
n_var = pr.n * pr.T
#
# number of obj func
n_fo = 4
# number of scenarios
n_scen = 7
pr.p_spott = adjust_PLD(pr.p_spott, n_scen, 2)
pr.GSF = adjust_GSF(pr.GSF, n_scen, 2)
plot_scenarios(n_scen, False, pr.p_spott, pr.GSF)
#
# place to store solutions for each scenario
sol_harmonious = []
for s in range(n_scen):
    #
    # initial optimization parameters
    x0 = np.zeros(n_var)
    bnds = int(n_var/2) * [pr.asset_bounds, pr.asset_bounds]
    bnds = adjust_bounds(bnds)
    #
    # find harmonious solution
    solutions = find_solutions(x0, s, bnds, n_fo)
    vals = find_function_values(solutions)
    harmonious_solution = find_harmonious_solution(x0, s, bnds, vals, pr.lambd, n_fo)
    #
    # update solutions
    solutions.update({'Harmonious Solution': [npv_cost(harmonious_solution.x, s), vol_cost(harmonious_solution.x, s),
                                              vol_gfis(harmonious_solution.x, s), res_diversity(harmonious_solution.x),
                                              harmonious_solution.x]})
    # sol_nothing.append(solutions["Don't do nothing"])
    sol_harmonious.append(solutions['Harmonious Solution'])
#
# build payoffs
if n_fo == 2:
    payoff_cost = build_payoff_cost(sol_harmonious, n_scen)
    payoff_vol_cost = build_payoff_vol_cost(sol_harmonious, n_scen)
    # -------------------------------------------------------------------------------------------------------------------
    #pm_cost, pm_vol_cost = add_sol_nothing_2_obj(payoff_cost, payoff_vol_cost, n_scen)
    pm_cost = payoff_cost
    pm_vol_cost = payoff_vol_cost
elif n_fo == 3:
    payoff_cost = build_payoff_cost(sol_harmonious, n_scen)
    payoff_vol_cost = build_payoff_vol_cost(sol_harmonious, n_scen)
    payoff_vol_gfis = build_payoff_vol_gfis(sol_harmonious, n_scen)
    #-------------------------------------------------------------------------------------------------------------------
    #pm_cost, pm_vol_cost, pm_vol_gfis, pm_divers = add_sol_nothing(payoff_cost, payoff_vol_cost, payoff_vol_gfis,
    #                                                               payoff_divers, n_scen)
    pm_cost = payoff_cost
    pm_vol_cost = payoff_vol_cost
    pm_vol_gfis = payoff_vol_gfis
else:
    payoff_cost = build_payoff_cost(sol_harmonious, n_scen)
    payoff_vol_cost = build_payoff_vol_cost(sol_harmonious, n_scen)
    payoff_vol_gfis = build_payoff_vol_gfis(sol_harmonious, n_scen)
    payoff_divers = build_payoff_div(sol_harmonious, n_scen)
    #-------------------------------------------------------------------------------------------------------------------
    #pm_cost, pm_vol_cost, pm_vol_gfis, pm_divers = add_sol_nothing(payoff_cost, payoff_vol_cost, payoff_vol_gfis,
    #                                                               payoff_divers, n_scen)
    pm_cost = payoff_cost
    pm_vol_cost = payoff_vol_cost
    pm_vol_gfis = payoff_vol_gfis
    pm_divers = payoff_divers
#
# build regret matrix
if n_fo == 2:
    r_cost = build_regret_matrix(pm_cost)
    r_vol_cost = build_regret_matrix(pm_vol_cost)
    #
    cc_cost = build_choice_criteria_matrix(pm_cost, pr.alpha)
    cc_vol_cost = build_choice_criteria_matrix(pm_vol_cost, pr.alpha)
    #
    ncc_cost = build_normalized_choice_criteria_matrix(cc_cost)
    ncc_vol_cost = build_normalized_choice_criteria_matrix(cc_vol_cost)
    #
    result = np.zeros([n_scen, 4])
    for i in range(n_scen):
        for j in range(4):
            result[i, j] = np.min([ncc_cost[i, j], ncc_vol_cost[i, j]])
elif n_fo == 3:
    r_cost = build_regret_matrix(pm_cost)
    r_vol_cost = build_regret_matrix(pm_vol_cost)
    r_vol_gfis = build_regret_matrix(pm_vol_gfis)
    #
    cc_cost = build_choice_criteria_matrix(pm_cost, pr.alpha)
    cc_vol_cost = build_choice_criteria_matrix(pm_vol_cost, pr.alpha)
    cc_vol_gfis = build_choice_criteria_matrix(pm_vol_gfis, pr.alpha)
    #
    ncc_cost = build_normalized_choice_criteria_matrix(cc_cost)
    ncc_vol_cost = build_normalized_choice_criteria_matrix(cc_vol_cost)
    ncc_vol_gfis = build_normalized_choice_criteria_matrix(cc_vol_gfis)
    #
    result = np.zeros([n_scen, 4])
    for i in range(n_scen):
        for j in range(4):
            result[i, j] = np.min([ncc_cost[i, j], ncc_vol_cost[i, j], ncc_vol_gfis[i, j]])
else:
    r_cost = build_regret_matrix(pm_cost)
    r_vol_cost = build_regret_matrix(pm_vol_cost)
    r_vol_gfis = build_regret_matrix(pm_vol_gfis)
    r_divers = build_regret_matrix(pm_divers)
    #
    cc_cost = build_choice_criteria_matrix(pm_cost, pr.alpha)
    cc_vol_cost = build_choice_criteria_matrix(pm_vol_cost, pr.alpha)
    cc_vol_gfis = build_choice_criteria_matrix(pm_vol_gfis, pr.alpha)
    cc_divers = build_choice_criteria_matrix(pm_divers, pr.alpha)
    #
    ncc_cost = build_normalized_choice_criteria_matrix(cc_cost)
    ncc_vol_cost = build_normalized_choice_criteria_matrix(cc_vol_cost)
    ncc_vol_gfis = build_normalized_choice_criteria_matrix(cc_vol_gfis)
    ncc_divers = build_normalized_choice_criteria_matrix(cc_divers)
    #
    result = np.zeros([n_scen, 4])
    for i in range(n_scen):
        for j in range(4):
            result[i, j] = np.min([ncc_cost[i, j], ncc_vol_cost[i, j], ncc_vol_gfis[i, j], ncc_divers[i, j]])
#
print(result)
#
# plot results
d = np.zeros([5, 10])
a = calc_exposure(d, 0)
b = calc_res(d, 0)
c = calc_req(d)
plt.plot(np.arange(0, pr.T), a, label='exposure')
plt.plot(np.arange(0, pr.T), b, label='resources')
plt.plot(np.arange(0, pr.T), c, label='requirements')
plt.legend()
plt.show()

