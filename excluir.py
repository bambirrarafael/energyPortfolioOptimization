import numpy as np
from scipy.optimize import minimize
import numpy as np
from portfolioParameters import Parameters
from objectiveFunctions import npv_cost
from main import sol_harmonious

pr = Parameters()

a = sol_harmonious[0][4]
a[10:] = 0
print(pr.p_spott[0])
print(pr.GSF[0])
print(a)
print(npv_cost(a, 0))
