import cvxpy as cp
import numpy as np
import gdfull
import pandas as pd

# df = pd.read_csv("Data\Weekly24-25.csv")
# df=df.iloc[lambda x: x.index % 4 == 0]

# variables = gdfull.getMatrix(df)
# mu = variables[0]
# cov_matrix = variables[1]

def getWeights(mu, cov_matrix):
    # cov_matrix = (cov_matrix + cov_matrix.T) / 2  # Force symmetry
    # # cov_matrix = cp.Constant(cov_matrix)    

    # Variables
    w = cp.Variable(5)

    # Constraints
    target_return = 0.05
    constraints = [
        mu @ w == target_return,
        cp.sum(w) == 1,
        w>=0
    ]
    print(cov_matrix)
    print(f"mu: {mu}")
    print(f"w: {np.array(w)}")

    portfolio_variance = cp.quad_form(w, cov_matrix)
    problem = cp.Problem(cp.Minimize(portfolio_variance), constraints)


    problem.solve()
    print("optimal weights:", w.value.round(4))
    print("minized risk: ",portfolio_variance.value)
    print("return: ",w.value@mu)

    print("Solver status:", problem.status)

    opweights = w.value
    expectedrisk=portfolio_variance.value
    ret = w.value@mu

    return [opweights, expectedrisk, ret]
