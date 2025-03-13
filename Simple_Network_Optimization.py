# Simple Network Optimization
# Author: Ha Lam Bao Minh
# Date: 11/03/2025

# Import packages
import gurobipy as gp
from gurobipy import *
import numpy as np

# Setup sets and parameters
I = 5 # Set of source (San Diego,...)
J = 3 # Set of destination (Seattle,...)
# Parameters
transport_cost = [
    [5,7,8],
    [10,8,6],
    [9,4,3],
    [12,6,2],
    [4,10,11]
    ]
open_cost = [0,0,350000,200000,480000]
demand = [3000,8000,9000]
supply = [2500,2500,10000,10000,10000]
# Setup model
model = gp.Model("Simple_Network_Optimization")
# Create variables
x = model.addVars(I, J, lb=0, vtype=GRB.CONTINUOUS, name="quantity_shipped")
y = model.addVars(I,vtype=GRB.BINARY,name = "open or not")
# Constraints
objective = gp.quicksum(transport_cost[i][j]*x[i,j] for i in range(I) for j in range(J)) + gp.quicksum(open_cost[i]*y[i] for i in range (I))

model.setObjective(objective,GRB.MINIMIZE)

# Constraints
model.addConstrs((gp.quicksum(x[i,j] for j in range(J)) <= y[i]*supply[i] for i in range(I)), name = "supply constraintconstraint")
model.addConstrs((gp.quicksum(x[i,j] for i in range(I)) >= demand[j] for j in range(J)), name = "demand constraint")

# Solve model
model.optimize()
# Visualize solution
import matplotlib.pyplot as plt

# Extract solution
solution_x = np.zeros((I, J))
for i in range(I):
    for j in range(J):
        solution_x[i, j] = x[i, j].X

# Plot the solution
fig, ax = plt.subplots()
cax = ax.matshow(solution_x, cmap='viridis')
fig.colorbar(cax)

# Set axis labels
ax.set_xticks(np.arange(J))
ax.set_yticks(np.arange(I))
ax.set_xticklabels([f'Destination {j+1}' for j in range(J)])
ax.set_yticklabels([f'Source {i+1}' for i in range(I)])

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="left", rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(I):
    for j in range(J):
        text = ax.text(j, i, f'{solution_x[i, j]:.1f}', ha="center", va="center", color="w")

plt.xlabel('Destinations')
plt.ylabel('Sources')
plt.title('Optimal Quantity Shipped from Sources to Destinations')
plt.show()