import numpy as np
import pandas as pd


class Parameters:
    T = 10          # number of years
    n = 5           # number of assets
    b_t = []        # energy bought contracts
    v_t = []        # energy contract sales over time
    g_it = []       # generation of asset i
    l_t = []        # load over time
    OM_i = []
    IC_i = []
    CF_i = []
    LS_i = []
    theta_i = []
    sigma_c = 0
    sigma_spot = 0
    p_b = 0
    p_v = 0
    rate = 0
    varepsilon = 0  # Maximum exposure
    #
    GSF = []
    p_spott = []
    lambd = []
    alpha = 0

    def __init__(self):
        #
        # Parameter definition
        self.T = 10         # number of years
        self.n = 5          # number of assets
        #
        # self.lambd = [0.5, 0.3, 0.10, 0.10]
        self.lambd = [1, 1, 1, 1]
        # self.lambd = [0.25, 0.25, 0.25, 0.25]
        # self.lambd = [0.8, 0.10, 0.05, 0.05]
        self.alpha = 0.25
        #
        en_data = np.array(pd.read_excel('./data/PORTFOLIO_DATA.xlsx', 'energy_data'))
        self.v_t = en_data[:, 1]
        self.l_t = en_data[:, 2]
        self.g_it = np.array(pd.read_excel('./data/PORTFOLIO_DATA.xlsx', 'gFIS'))     # generation of asset i
        data = np.array(pd.read_excel('./data/PORTFOLIO_DATA.xlsx', 'asset_data'))
        self.IC_i = data[:, 1]
        self.OM_i = data[:, 2]
        self.LS_i = data[:, 3]
        self.CF_i = data[:, 4]
        self.theta_i = data[:, 5]
        self.sigma_c = 35
        self.sigma_spot = 130
        self.p_v = 180
        self.varepsilon = 5  # Maximum exposure
        self.asset_bounds = [-self.varepsilon, self.varepsilon]
        #
        self.p_spott = np.array(pd.read_excel('./data/SCENARIO_DATA.xlsx', 'PLD', header=None))
        self.GSF = np.ones([self.n, self.T, np.shape(self.p_spott)[0]])
        aux = np.array(pd.read_excel('./data/SCENARIO_DATA.xlsx', 'GSF', header=None))
        self.GSF[4, :, :] = aux.swapaxes(0, 1)
        #
