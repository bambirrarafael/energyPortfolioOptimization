import numpy as np
from portfolioParameters import Parameters

pr = Parameters()


def calc_res(x, s):
    x = x.reshape([pr.n, pr.T])
    res_t = np.zeros(pr.T)
    for t in range(pr.T):
        sm = 0
        for i in range(pr.n):
            sm += x[i, t] + pr.GSF[i, t, s] * pr.g_it[i, t]
        res_t[t] = sm
    return res_t


def calc_req(x):    # OK!
    x = x.reshape([pr.n, pr.T])
    req_t = np.zeros(pr.T)
    for t in range(pr.T):
        sm = 0
        if x[0, t] < 0:
            sm += x[0, t]
        req_t[t] = pr.v_t[t] + pr.l_t[t] - sm
    return req_t


def calc_exposure(x, s):
    x = x.reshape([pr.n, pr.T])
    exp_t = np.zeros(pr.T)
    for t in range(pr.T):
        sm = 0
        for i in range(pr.n):
            sm += x[i, t] + pr.GSF[i, t, s] * pr.g_it[i, t]
        exp_t[t] = sm - pr.v_t[t] - pr.l_t[t]
    return exp_t


def calc_cost(x, exp, s):
    x = x.reshape([pr.n, pr.T])
    cost_t = np.zeros(pr.T)
    for t in range(pr.T):
        sm = 0
        for i in range(pr.n):
            p_i = pr.IC_i[i]/(pr.CF_i[i] * pr.LS_i[i])/8760 + pr.OM_i[i]
            sm += p_i * x[i, t] + pr.OM_i[i] * pr.GSF[i, t, s] * pr.g_it[i, t]
        cost_t[t] = 8760 * (sm - pr.p_v * pr.v_t[t] - pr.p_spott[s, t] * exp[t])
    return cost_t
