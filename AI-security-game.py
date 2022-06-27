
import sys

'''

Using PULP Library

'''

# for Jupyter Notebooks
#!pip install pulp

from pulp import LpMaximize, LpProblem, LpStatus, LpVariable

alpha = 0.1

inp = float(input("Enter the value of alpha number: "))

alpha = inp

# Create the maximization problem
model = LpProblem(name='Field Problem', sense=LpMaximize)
# Initialize the variables
x1 = LpVariable(name="x1", lowBound=0, upBound=1)
x2 = LpVariable(name="x2", lowBound=0, upBound=1)
x3 = LpVariable(name="x3", lowBound=0, upBound=1)
x4 = LpVariable(name="x4", lowBound=0, upBound=1)
x5 = LpVariable(name="x5", lowBound=0, upBound=1)


Vdef = LpVariable(name="Vdef", lowBound=-3, upBound=7)

Vatt = LpVariable(name="Vatt", lowBound=-3, upBound=6)

#M = LpVariable(name="M", lowBound=1000000, upBound=1000000)


z1 = LpVariable(name="z1", lowBound=0, upBound=1, cat="Integer")
z2 = LpVariable(name="z2", lowBound=0, upBound=1, cat="Integer")
z3 = LpVariable(name="z3", lowBound=0, upBound=1, cat="Integer")
z4 = LpVariable(name="z4", lowBound=0, upBound=1, cat="Integer")
z5 = LpVariable(name="z5", lowBound=0, upBound=1, cat="Integer")

#K = 2
#N = 5

# Add the constraints to the model. Use += to append expressions to the model

xt1 = (alpha * (2/5)) + ((1 - alpha)*x1)
xt2 = (alpha * (2/5)) + ((1 - alpha)*x2)
xt3 = (alpha * (2/5)) + ((1 - alpha)*x3)
xt4 = (alpha * (2/5)) + ((1 - alpha)*x4)
xt5 = (alpha * (2/5)) + ((1 - alpha)*x5)

model += ( (Vatt - (0*(xt1) + 2*(1-xt1))) <= (1-z1)*100000000 , "a1") 

model += ( (Vatt - (-1*(xt2) + 3*(1-xt2))) <= (1-z2)*100000000 , "a2") 

model += ( (Vatt - (-2*(xt3) + 5*(1-xt3))) <= (1-z3)*100000000 , "a3") 

model += ( (Vatt - (-1*(xt4) + 4*(1-xt4))) <= (1-z4)*100000000 , "a4") 

model += ( (Vatt - (-3*(xt5) + 6*(1-xt5))) <= (1-z5)*100000000 , "a5") 

model += ( Vatt - ( 0 * xt1 + 2 * (1 - xt1)) >= 0, "a6") 
model += ( Vatt - ( -1 * xt2 + 3 * (1 - xt2)) >= 0, "a7") 
model += ( Vatt - ( -2 * xt3 + 5 * (1 - xt3)) >= 0, "a8") 
model += ( Vatt - ( -1 * xt4 + 4 * (1 - xt4)) >= 0, "a9") 
model += ( Vatt - ( -3 * xt5 + 6 * (1 - xt5)) >= 0, "a10") 



model += ( (Vdef - (4*(x1) + -1*(1-x1))) <= (1-z1)*100000000 , "d1") 

model += ( (Vdef - (5*(x2) + -2*(1-x2))) <= (1-z2)*100000000 , "d2") 

model += ( (Vdef - (3*(x3) + 0*(1-x3))) <= (1-z3)*100000000 , "d3") 

model += ( (Vdef - (6*(x4) + -3*(1-x4))) <= (1-z4)*100000000 , "d4") 

model += ( (Vdef - (7*(x5) + -3*(1-x5))) <= (1-z5)*100000000 , "d5") 


model += ( x1 + x2 + x3 + x4 + x5 <= 2, "defender_max1")

model += ( z1 + z2 + z3 + z4 + z5 <= 1, "am1")
model += ( z1 + z2 + z3 + z4 + z5 >= 1, "am2")

# Objective Function
obj_func = Vdef
# Add Objective function to the model
model += obj_func

model

status = model.solve()

print(f"status: {model.status}, {LpStatus[model.status]}")
print(f"objective: {model.objective.value()}")
for var in model.variables():
    print(f"{var.name}: {var.value()}")
for name, constraint in model.constraints.items():
    print(f"{name}: {constraint.value()}")


'''

IF ALPHA = 0.4

status: 1, Optimal
objective: 2.4744013
Vatt: 1.6038233
Vdef: 2.4744013
x1: 0.063480553
x2: 0.31507361
x3: 0.54194682
x4: 0.53205889
x5: 0.54744013
z1: 0.0
z2: 0.0
z3: 0.0
z4: 0.0
z5: 1.0
a1: -100000000.00000004
a2: -100000000.00000003
a3: -100000000.00000004
a4: -100000000.00000003
a5: 0.0
a6: -3.640000000026955e-08
a7: -3.599999998105119e-08
a8: -5.599999930439026e-08
a9: -3.0000000039720476e-08
a10: 2.000000609569952e-09
d1: -99999996.84300147
d2: -99999997.73111397
d3: -99999999.15143916
d4: -99999999.31412871
d5: 0.0
defender_max1: 3.0000001371988105e-09
am1: 0.0
am2: 0.0

'''
