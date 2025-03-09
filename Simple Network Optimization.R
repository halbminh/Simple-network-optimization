# Install library
install.packages("lpSolve")
installed.packages("lpSolve")
library(lpSolve)

# Decision variable coefficients
cost <- c(5,7,8,10,8,6,9,4,3,12,6,2,4,10,11,0,0,350000,200000,480000)

# Contraint matrics
lhs <- matrix(c(
  rep(1, 3), rep(0, 12), -2500, rep(0, 4), #Supply constraint 1
  rep(0, 3), rep(1, 3), rep(0, 10), -2500, rep(0, 3), #Supply constraint 2
  rep(0, 6), rep(1, 3), rep(0, 8), -10000,rep(0, 2), #Supply constraint 3
  rep(0, 9), rep(1, 3), rep(0, 6), -10000, 0, #Supply constraint 4
  rep(0, 12), rep(1, 3), rep(0, 4), -10000, #Supply constraint 5
  1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,rep(0, 5), #Demand constraint 1
  0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,rep(0, 5), #Demand constraint 2
  0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,rep(0, 5)  #Demand constraint 3
  ),nrow= 8,ncol= 20,byrow= TRUE)
print(lhs)

direction <-c(rep('<=', 5),rep('=', 3))

rhs <- c(rep(0,5),3000,8000,9000)

# Model
model <- lp(
  direction = "min",
  objective.in = cost,
  const.mat = lhs,
  const.dir = direction,
  const.rhs = rhs,
  bin = 16:20
)
model$solution
model$objval

