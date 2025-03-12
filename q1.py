from z3 import Solver, Int, Ints, And, sat

def solve_all_positive_smt():
    # Create a Z3 solver instance
    solver = Solver()
    
    # Declare the variables representing the list elements (at most 5)
    n1, n2, n3, n4, n5 = Ints('n1 n2 n3 n4 n5')
    
    # Constraint for the length of the list (at least one element)
    length = Int('length')
    solver.add(length > 0)
    
    # Constraint that all elements in the list are positive
    solver.add(And(n1 > 0, n2 > 0, n3 > 0, n4 > 0, n5 > 0))
    
    # You can add constraints to limit the number of elements processed (e.g., length <= 5)
    solver.add(length <= 5)
    
    # Check for satisfiability and model the solution
    if solver.check() == sat:
        model = solver.model()
        solution = [model[n1].as_long(), model[n2].as_long(), model[n3].as_long(), model[n4].as_long(), model[n5].as_long()]
        return solution
    else:
        return None

# Run the solver to find an "AllPositive" input list
result = solve_all_positive_smt()
print(result if result else "No solution found")