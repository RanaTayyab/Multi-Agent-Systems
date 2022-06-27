# -*- coding: utf-8 -*-

# !pip install cplex docplex 
# !pip install pulp

# -*- coding: utf-8 -*-

'''
Question is Solved in 2 ways
 1. CPLEX library (as required)
 2. PULP library (easier to interpret)

'''



'''

Solution 1: CPLEX

'''

# !pip install cplex docplex 
# (Installing CPLEX)

import cplex
from cplex.exceptions import CplexError
import sys

# data common to all populatedby functions
my_obj = [0, 0, 0, 0, 0, 1]
my_ub = [1,1,1,1,1, 7]
my_lb = [0,0,0,0,0, -7]
my_colnames = ["x1", "x2", "x3", "x4", "x5","u"]
my_rhs = [0,0,0,0,0,1]
my_rownames = ["c1", "c2","c3", "c4", "c5","c6"]
my_sense = "GGGGGE" 

def populatebyrow(prob):
    prob.objective.set_sense(prob.objective.sense.maximize)
    prob.variables.add(obj = my_obj, ub = my_ub, lb = my_lb, names = my_colnames)

    rows = [[[0, 1, 2, 3 , 4, 5], [5, -3, -3, -3, -3, -1]],
            [[0, 1, 2, 3 , 4, 5], [-4, 7, -4, -4, -4, -1]],
            [[0, 1, 2, 3 , 4, 5], [-2, -2, 3, -2, -2, -1]],
            [[0, 1, 2, 3 , 4, 5], [-7, -7, -7, 6, -7, -1]],
            [[0, 1, 2, 3 , 4, 5], [-5, -5, -5, -5, 4, -1]],
            [[0, 1, 2, 3 , 4, 5], [1, 1, 1, 1, 1, 0]]]

    prob.linear_constraints.add(lin_expr = rows,
                                senses = my_sense,
                                rhs = my_rhs,
                                names = my_rownames)

def lpex1(pop_method):
    try:
        my_prob = cplex.Cplex()
        if pop_method == "r":
            handle = populatebyrow(my_prob)
        my_prob.solve()
    except CplexError as exc:
        raise
    numrows = my_prob.linear_constraints.get_num()
    numcols = my_prob.variables.get_num()
    print()

    print ("Solution value = ", my_prob.solution.get_objective_value())
    slack = my_prob.solution.get_linear_slacks()
    pi = my_prob.solution.get_dual_values()
    x = my_prob.solution.get_values()
    dj = my_prob.solution.get_reduced_costs()
    for i in range(numrows):
        print ("Row %d:  Slack = %10f    Pi = %10f" % (i, slack[i], pi[i]))
    for j in range(numcols):
        print ("Column %d:   Value = %10f    Reduced cost = %10f" % (j, x[j], dj[j]))
    my_prob.write("lpex1.lp")



'''
CPLEX ANSWERS:

Solution value =  -2.0613128155806684

Row 0:  Slack =   0.000000    Pi =  -0.309449
Row 1:  Slack =   0.000000    Pi =  -0.225054
Row 2:  Slack =  -0.061313    Pi =   0.000000
Row 3:  Slack =   0.000000    Pi =  -0.190430
Row 4:  Slack =   0.000000    Pi =  -0.275066
Row 5:  Slack =   0.000000    Pi =  -2.061313

Column 0:   Value =   0.117336    Reduced cost =   0.000000
Column 1:   Value =   0.176244    Reduced cost =   0.000000
Column 2:   Value =   0.000000    Reduced cost =  -2.475595
Column 3:   Value =   0.379899    Reduced cost =   0.000000
Column 4:   Value =   0.326521    Reduced cost =   0.000000
Column 5:   Value =  -2.061313    Reduced cost =   0.000000

'''



'''
SOLUTION 2: PULP Library

'''



# for Jupyter Notebooks
# !pip install pulp 
# (installing pulp)

def pulp_solution():

    from pulp import LpMaximize, LpProblem, LpStatus, LpVariable

    # Create the maximization problem
    model = LpProblem(name='Field Problem', sense=LpMaximize)
    # Initialize the variables
    x1 = LpVariable(name="x1", lowBound=0, upBound=1)
    x2 = LpVariable(name="x2", lowBound=0, upBound=1)
    x3 = LpVariable(name="x3", lowBound=0, upBound=1)
    x4 = LpVariable(name="x4", lowBound=0, upBound=1)
    x5 = LpVariable(name="x5", lowBound=0, upBound=1)
    u = LpVariable(name="u")

    # Add the constraints to the model. Use += to append expressions to the model
    model += (5 * x1 + -3 * x2 + -3 * x3 + -3 * x4 + -3 * x5 >= u, "margin_X1") #it cannot go past the fence
    model += (-4 * x1 + 7 * x2 + -4 * x3 + -4 * x4 + -4 * x5 >= u, "margin_X2") #it cannot go past the fence
    model += (-2 * x1 + -2 * x2 + 3 * x3 + -2 * x4 + -2 * x5 >= u, "margin_X3") #it cannot go past the fence
    model += (-7 * x1 + -7 * x2 + -7 * x3 + 6 * x4 + -7 * x5 >= u, "margin_X4") #it cannot go past the fence
    model += (-5 * x1 + -5 * x2 + -5 * x3 + -5 * x4 + 4 * x5 >= u, "margin_X5") #it cannot go past the fence

    model += ( x1 + x2 + x3 + x4 + x5 == 1, "margin_u")

    # Objective Function
    obj_func = u
    # Add Objective function to the model
    model += obj_func

    print(model)

    '''
    It shows Model before solving which is:

    Field_Problem:
    MAXIMIZE
    1*u + 0
    SUBJECT TO
    margin_X1: - u + 5 x1 - 3 x2 - 3 x3 - 3 x4 - 3 x5 >= 0

    margin_X2: - u - 4 x1 + 7 x2 - 4 x3 - 4 x4 - 4 x5 >= 0

    margin_X3: - u - 2 x1 - 2 x2 + 3 x3 - 2 x4 - 2 x5 >= 0

    margin_X4: - u - 7 x1 - 7 x2 - 7 x3 + 6 x4 - 7 x5 >= 0

    margin_X5: - u - 5 x1 - 5 x2 - 5 x3 - 5 x4 + 4 x5 >= 0

    margin_u: x1 + x2 + x3 + x4 + x5 = 1

    VARIABLES
    u free Continuous
    x1 <= 1 Continuous
    x2 <= 1 Continuous
    x3 <= 1 Continuous
    x4 <= 1 Continuous
    x5 <= 1 Continuous

    '''



    status = model.solve()

    print(f"status: {model.status}, {LpStatus[model.status]}")
    print(f"objective: {model.objective.value()}")
    for var in model.variables():
        print(f"{var.name}: {var.value()}")
    for name, constraint in model.constraints.items():
        print(f"{name}: {constraint.value()}")



    '''
    SOLUTION: 

    status: 1, Optimal

    objective: -2.0613128

    u: -2.0613128
    x1: 0.1173359
    x2: 0.17624429
    x3: 0.0
    x4: 0.37989901
    x5: 0.3265208

    margin_X1: 0.0
    margin_X2: -9.99999993922529e-09
    margin_X3: 0.061312800000000056
    margin_X4: -7.000000001866624e-08
    margin_X5: 4.440892098500626e-16
    margin_u: 0.0

    '''



if __name__ == "__main__":
  print("CPLEX SOLUTION:")
  print("\n")

  lpex1("r")

  print("\n")
  print("PULP SOLUTION:")
  print("\n")

  pulp_solution()

