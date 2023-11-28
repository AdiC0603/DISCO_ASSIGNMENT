""" 
Discret Structure of Computer Science Assignment 
(Faculty-Course Assignment Problem)
Group Members:
Pray Raskapoorwala (2022A7PS1239G)
Aditya Chaudhary (2022A7PS0622G)
Aditya Gupta (2022A7PS0090G)

Disclaimer: Kindly Download All the libraries required for the proper functioning of the code

User Input Instruction :
The Code is made friendly for for user
For Proff of category x1 please input 1
For Proff of category x2 please input 2
For Proff of category x3 please input 3
this is done so as to avoid conversion of floating point numbers and integer number
    This code works for CDC's
    We made one assumption such that:
    no.of courses = no of proff = (n)
"""

from ortools.sat.python import cp_model
import numpy as np
from sympy import symbols
import sys
from contextlib import redirect_stdout

n = int(input("Enter the value for n: "))

#Variables
variables = symbols('a1:%d' % (n**2 + 1))

#Array declaration for parameters of Faculty
faculty_id = []
faculty_Courselimit = []
faculty_preferences = np.zeros((n, n), dtype=int)
my_matrix = []

for i in range(n):
    row = []
    for j in range(n):
        if(faculty_preferences[i,j]!=0):
            row.append(variables[i * n + j])
        else:
            row.append(0)
    my_matrix.append(row)

# # TO PRINT THE INTIAL MATRIX
# print("Initial my_matrix:")
# print(my_matrix)

# print("Faculty Preferences:")
# print(faculty_preferences)


# This is whole user inputed at run-time
Courses = []
for i in range(n):
    Courses.append(input(f"Enter course number {i}: "))

for i in range(n):
    faculty_id.append(input("Enter faculty ID: "))
    faculty_Courselimit.append(int(input("Enter faculty course limit: ")))
    for j in range(n):
        preference_input = input(f"Does faculty {faculty_id[i]} prefer course {j+1}? (Y/N): ")
        if preference_input.upper() == "Y":
            faculty_preferences[i, j] = faculty_Courselimit[i]


# This is a class defined to print all the possible outcome for the Problem Statement

# CP-SAT Algorithm of Or-tool library is used to solve all the constraints
class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables, output_file):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
        self.output_file = output_file

    def on_solution_callback(self):
        self.__solution_count += 1
        with redirect_stdout(self.output_file):
            for i in range(n):
                print(f"{faculty_id[i]} will take Course : " )   
                for j in range(n):
                    if(faculty_preferences[i,j]!=0):
                        if(self.Value(self.__variables[i][j])!=0):
                            print(f"{Courses[j]}", end=" ")
                print()
            print()

    def solution_count(self):
        return self.__solution_count

def SearchForAllSolutionsSampleSat(output_file):
    
    # Defining the model for our constraint problem
    model = cp_model.CpModel()
    
    # Adding all the variables to our model
    for i in range(n):
        for j in range(n):
            if(faculty_preferences[i,j]!=0):
                my_matrix[i][j] = model.NewIntVar(0, 3, "my_matrix[i,j]")

    # Adding our Constraints using the variables which we added previously
    #Column Constraint
    for i in range(n):
        if faculty_preferences[i].sum() != 0:
            row_sum = sum(my_matrix[i][j] for j in range(n))
            bool_var = model.NewBoolVar(f'bool_var_{i}')
            model.Add(row_sum == 2).OnlyEnforceIf(bool_var)
            model.Add(row_sum == 0).OnlyEnforceIf(bool_var.Not())
            
    # Row Constraint
    for j in range(n):
        model.Add(sum(my_matrix[i][j] for i in range(n)) <= faculty_Courselimit[j])        

    # Printing all the possible output in the Output.csv file
    solver = cp_model.CpSolver()
    with open(output_file, 'w') as f:
        solution_printer = VarArraySolutionPrinter(my_matrix, f)
        solver.parameters.enumerate_all_solutions = True
        status = solver.Solve(model, solution_printer)
        print(f"Status = {solver.StatusName(status)}")
        print(f"Number of solutions found: {solution_printer.solution_count()}")

# Specify the output file name
# This creates are output file with all the outputs
output_file_name = 'output.csv'
SearchForAllSolutionsSampleSat(output_file_name)
