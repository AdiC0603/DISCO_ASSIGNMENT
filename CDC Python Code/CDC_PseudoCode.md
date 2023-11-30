# Pseudocode for Faculty-Course Assignment Problem

# User Input
n = input("Enter the value for n: ")

# Variables
variables = create_symbolic_variables(n)

# Initialize faculty-related arrays
faculty_id, faculty_Courselimit, faculty_preferences, my_matrix = initialize_faculty_arrays(n)

# Get user input for courses and faculty preferences
get_user_input(n, Courses, faculty_id, faculty_Courselimit, faculty_preferences)

# Initialize CP-SAT model
model = initialize_cp_sat_model(n, faculty_preferences, faculty_Courselimit, my_matrix)

# Search for all solutions using CP-SAT algorithm
output_file_name = 'output.csv'
search_for_all_solutions(model, my_matrix, output_file_name)

# Define functions used in the code

function create_symbolic_variables(n):
    return symbols('a1:%d' % (n**2 + 1))

function initialize_faculty_arrays(n):
    faculty_id = []
    faculty_Courselimit = []
    faculty_preferences = create_zero_matrix(n)
    my_matrix = create_zero_matrix(n)
    return faculty_id, faculty_Courselimit, faculty_preferences, my_matrix

function create_zero_matrix(n):
    return np.zeros((n, n), dtype=int)

function get_user_input(n, Courses, faculty_id, faculty_Courselimit, faculty_preferences):
    for i in range(n):
        Courses.append(input(f"Enter course number {i}: "))
        faculty_id.append(input("Enter faculty ID: "))
        faculty_Courselimit.append(int(input("Enter faculty course limit: ")))
        for j in range(n):
            preference_input = input(f"Does faculty {faculty_id[i]} prefer course {j+1}? (Y/N): ")
            if preference_input.upper() == "Y":
                faculty_preferences[i, j] = faculty_Courselimit[i]

function initialize_cp_sat_model(n, faculty_preferences, faculty_Courselimit, my_matrix):
    model = cp_model.CpModel()
    for i in range(n):
        for j in range(n):
            if faculty_preferences[i, j] != 0:
                my_matrix[i][j] = model.NewIntVar(0, 3, "my_matrix[i,j]")
    for i in range(n):
        if faculty_preferences[i].sum() != 0:
            model.Add(sum(my_matrix[i][j] for j in range(n)) == faculty_Courselimit[i])
    for j in range(n):
        model.Add(sum(my_matrix[i][j] for i in range(n)) == 2)
    return model

function search_for_all_solutions(model, my_matrix, output_file_name):
    solver = cp_model.CpSolver()
    with open(output_file_name, 'w') as f:
        solution_printer = VarArraySolutionPrinter(my_matrix, f)
        solver.parameters.enumerate_all_solutions = True
        status = solver.Solve(model, solution_printer)
        print(f"Status = {solver.StatusName(status)}")
        print(f"Number of solutions found: {solution_printer.solution_count()}")
