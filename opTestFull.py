import cvxpy as cp
import numpy as np
import gdfull



mu = gdfull.m
cov_matrix = gdfull.sigma

# cov_matrix = (cov_matrix + cov_matrix.T) / 2  # Force symmetry
# # cov_matrix = cp.Constant(cov_matrix)    

# Variables
w = cp.Variable(5)

# Constraints
target_return = 0.001
constraints = [
    mu @ w == target_return,
    cp.sum(w) == 1,
    w >= 0
]
# print(cov_matrix)

portfolio_variance = cp.quad_form(w, cov_matrix)
problem = cp.Problem(cp.Minimize(portfolio_variance), constraints)

problem.solve()
print("optimal weights:", w.value)
print("minized risk: ",portfolio_variance.value)
print("return: ",w.value@mu)