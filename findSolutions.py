import scipy.optimize as opt
import numpy as np
from objectiveFunctions import npv_cost
from objectiveFunctions import vol_cost
from objectiveFunctions import vol_gfis
from objectiveFunctions import res_diversity
from objectiveFunctions import npv_cost_max
from objectiveFunctions import vol_cost_max
from objectiveFunctions import vol_gfis_max
from objectiveFunctions import res_diversity_max
from objectiveFunctions import max_min
from constrains import constrain1
from constrains import constrain2


def find_solutions(x0, s, bnds, n_fo):
    if n_fo == 2:
        #con = {'type': 'ineq', "fun": constrain1}
        #
        # dont do nothing solution
        f1 = npv_cost(x0, s)
        f2 = vol_cost(x0, s)
        f3 = vol_gfis(x0, s)
        f4 = res_diversity(x0)
        solutions = {"Don't do nothing": [f1, f2, f3, f4, x0]}
        #
        # min cost
        min_npv_cost = opt.minimize(npv_cost, x0, args=s, bounds=bnds)#, constraints=con)
        x = min_npv_cost.x
        solutions.update({'Minimum Cost': [min_npv_cost.fun, vol_cost(x, s), vol_gfis(x, s), res_diversity(x), x]})
        #
        # min vol cost
        min_vol_cost = opt.minimize(vol_cost, x0, args=s, bounds=bnds)
        x = min_vol_cost.x
        solutions.update(
            {'Minimum Cost Volatility': [npv_cost(x, s), min_vol_cost.fun, vol_gfis(x, s), res_diversity(x), x]})
        # ==================================================================================================================
        # max cost
        max_npv_cost = opt.minimize(npv_cost_max, x0, args=s, bounds=bnds)
        x = max_npv_cost.x
        solutions.update({'Maximum Cost': [-max_npv_cost.fun, vol_cost(x, s), vol_gfis(x, s), res_diversity(x), x]})
        #
        # max vol cost
        max_vol_cost = opt.minimize(vol_cost_max, x0, args=s, bounds=bnds)
        x = max_vol_cost.x
        solutions.update(
            {'Maximum Cost Volatility': [npv_cost(x, s), -max_vol_cost.fun, vol_gfis(x, s), res_diversity(x), x]})

        return solutions
    elif n_fo == 3:
        # con = {'type': 'ineq', "fun": constrain1}
        #
        # dont do nothing solution
        f1 = npv_cost(x0, s)
        f2 = vol_cost(x0, s)
        f3 = vol_gfis(x0, s)
        f4 = res_diversity(x0)
        solutions = {"Don't do nothing": [f1, f2, f3, f4, x0]}
        #
        # min cost
        min_npv_cost = opt.minimize(npv_cost, x0, args=s, bounds=bnds)  # , constraints=con)
        x = min_npv_cost.x
        solutions.update({'Minimum Cost': [min_npv_cost.fun, vol_cost(x, s), vol_gfis(x, s), res_diversity(x), x]})
        #
        # min vol cost
        min_vol_cost = opt.minimize(vol_cost, x0, args=s, bounds=bnds)
        x = min_vol_cost.x
        solutions.update(
            {'Minimum Cost Volatility': [npv_cost(x, s), min_vol_cost.fun, vol_gfis(x, s), res_diversity(x), x]})
        #
        # min vol gfis
        min_vol_gfis = opt.minimize(vol_gfis, x0, args=s, bounds=bnds)
        x = min_vol_gfis.x
        solutions.update({'Minimum Resources Volatility': [npv_cost(x, s), vol_cost(x, s), min_vol_gfis.fun,
                                                           res_diversity(x), x]})
        # ==================================================================================================================
        # max cost
        max_npv_cost = opt.minimize(npv_cost_max, x0, args=s, bounds=bnds)
        x = max_npv_cost.x
        solutions.update({'Maximum Cost': [-max_npv_cost.fun, vol_cost(x, s), vol_gfis(x, s), res_diversity(x), x]})
        #
        # max vol cost
        max_vol_cost = opt.minimize(vol_cost_max, x0, args=s, bounds=bnds)
        x = max_vol_cost.x
        solutions.update(
            {'Maximum Cost Volatility': [npv_cost(x, s), -max_vol_cost.fun, vol_gfis(x, s), res_diversity(x), x]})
        #
        # max vol gfis
        max_vol_gfis = opt.minimize(vol_gfis_max, x0, args=s, bounds=bnds)
        x = max_vol_gfis.x
        solutions.update({'Maximum Resources Volatility': [npv_cost(x, s), vol_cost(x, s), -max_vol_gfis.fun,
                                                           res_diversity(x), x]})

        return solutions
    else:
        # con = {'type': 'ineq', "fun": constrain1}
        #
        # dont do nothing solution
        f1 = npv_cost(x0, s)
        f2 = vol_cost(x0, s)
        f3 = vol_gfis(x0, s)
        f4 = res_diversity(x0)
        solutions = {"Don't do nothing": [f1, f2, f3, f4, x0]}
        #
        # min cost
        min_npv_cost = opt.minimize(npv_cost, x0, args=s, bounds=bnds)  # , constraints=con)
        x = min_npv_cost.x
        solutions.update({'Minimum Cost': [min_npv_cost.fun, vol_cost(x, s), vol_gfis(x, s), res_diversity(x), x]})
        #
        # min vol cost
        min_vol_cost = opt.minimize(vol_cost, x0, args=s, bounds=bnds)
        x = min_vol_cost.x
        solutions.update(
            {'Minimum Cost Volatility': [npv_cost(x, s), min_vol_cost.fun, vol_gfis(x, s), res_diversity(x), x]})
        #
        # min vol gfis
        min_vol_gfis = opt.minimize(vol_gfis, x0, args=s, bounds=bnds)
        x = min_vol_gfis.x
        solutions.update({'Minimum Resources Volatility': [npv_cost(x, s), vol_cost(x, s), min_vol_gfis.fun,
                                                           res_diversity(x), x]})
        #
        # min Resources Diversity
        min_res_div = opt.minimize(res_diversity, x0, bounds=bnds)
        x = min_res_div.x
        solutions.update({'Minimum Resources Diversity': [npv_cost(x, s), vol_cost(x, s), vol_gfis(x, s),
                                                          min_res_div.fun, x]})
        # ==================================================================================================================
        # max cost
        max_npv_cost = opt.minimize(npv_cost_max, x0, args=s, bounds=bnds)
        x = max_npv_cost.x
        solutions.update({'Maximum Cost': [-max_npv_cost.fun, vol_cost(x, s), vol_gfis(x, s), res_diversity(x), x]})
        #
        # max vol cost
        max_vol_cost = opt.minimize(vol_cost_max, x0, args=s, bounds=bnds)
        x = max_vol_cost.x
        solutions.update(
            {'Maximum Cost Volatility': [npv_cost(x, s), -max_vol_cost.fun, vol_gfis(x, s), res_diversity(x), x]})
        #
        # max vol gfis
        max_vol_gfis = opt.minimize(vol_gfis_max, x0, args=s, bounds=bnds)
        x = max_vol_gfis.x
        solutions.update({'Maximum Resources Volatility': [npv_cost(x, s), vol_cost(x, s), -max_vol_gfis.fun,
                                                           res_diversity(x), x]})
        #
        # max Resources Diversity
        max_res_div = opt.minimize(res_diversity_max, x0, bounds=bnds)
        x = max_res_div.x
        solutions.update({'Maximum Resources Diversity': [npv_cost(x, s), vol_cost(x, s), vol_gfis(x, s),
                                                          -max_res_div.fun, x]})

        return solutions

def find_harmonious_solution(x0, s, bnds, vals, lambd, n_fo):
    harm_sol = opt.minimize(max_min, x0, args=(s, vals, lambd, n_fo), bounds=bnds)
    return harm_sol
