# Modern portfolio theory (MPT), 
or mean-variance analysis, is a mathematical framework for assembling a portfolio of assets such that the expected return is maximized for a given level of risk. 
This implementation takes a set of of returns from historical data over some time frame as an input to a quadratic form which can be optimized to minimize risk for a certain target return.
Meant to test theory in practice

### Directions:

Open the main file. This is meant to take csv documents. I used google finance for my datasets with a cell in between each stock's information
1. There are three functions. The first one takes all of the input price data over the given time period, averages the return of each stock and calculates each volatility and pairwise covariance. Using MPT it creates an optimal portfolio allocation based on a percentage towards each asset. This function splits the data set into all reference data and saves the final 2 as a start position and a future position to see how well the position would do based on the formula
2. The second function splits the dataset into as many overlapping 12 months periods as possible. For each period it creates an 'optimal portfolio allocation' and graphs how they change over time
3. The final function just graphs to returns of each asset over time


