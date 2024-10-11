from typing import List

def simplex(objectiveFunction: List[float], constraintCoefficients: List[List[float]], constraintValues: List[float], eps: int) -> tuple:
    constraints = []
    objectiveFunction = list(map(lambda x: -x, objectiveFunction))
    objectiveFunction.append(0)
    for i in range(len(constraintCoefficients)):
        constraintCoefficients[i].append(constraintValues[i])
    constraints.append(objectiveFunction)
    for constraint in constraintCoefficients:
        constraints.append(constraint)

    variables = []
    basic_variables = ["Maximum function value"]
    for i in range(1, len(objectiveFunction)):
        variables.append(str(i))
    for i in range(1, len(constraintValues) + 1):
        basic_variables.append("s" + str(i))
        variables.append("s" + str(i))

    while min(constraints[0]) < 0:
        pivot_column = constraints[0].index(min(constraints[0]))
        ratios = [-1]
        for i in range(1, len(constraints)):
            if constraints[i][pivot_column] == 0:
                ratios.append(-1)
                continue
            ratios.append(constraints[i][-1] / constraints[i][pivot_column])
        if len(list(filter(lambda x: x >= 0, ratios))) == 0:
            return ["Method is not applicable"]
        pivot_row = ratios.index(min(filter(lambda x: x >= 0, ratios)))
        
        enter = variables[pivot_column]
        basic_variables[pivot_row] = enter
        pivot = constraints[pivot_row][pivot_column]
        constraints[pivot_row] = list(map(lambda x: x / pivot,constraints[pivot_row]))

        enter_row = constraints[pivot_row]
        enter_row_index = constraints.index(enter_row)
        constraints.remove(enter_row)
        for i in range(0, len(constraints)):
            current_pivot = constraints[i][pivot_column]
            for j in range(len(constraints[i])):
                constraints[i][j] -= current_pivot * enter_row[j]
        constraints.insert(enter_row_index,enter_row)

    
    for i in range(len(basic_variables)):
        if "s" in basic_variables[i]:
            constraints.pop(i)
    basic_variables = list(filter(lambda x: "s" not in x, basic_variables))
    constraints = list(map(lambda x: x[-1], constraints))

    x = [0] * (len(objectiveFunction) - 1)
    maximumFunctionValue = constraints.pop(0)
    basic_variables.pop(0)
    for i in range(len(basic_variables)):
        x[int(basic_variables[i]) - 1] = constraints[i]

    x = list(map(lambda x: round(x, eps), x))
    maximumFunctionValue = round(maximumFunctionValue, eps)

    return (x, maximumFunctionValue)


objectiveFunction = list(map(lambda x: float(x), input("Enter coefficients for objective function [\"1 2 3\", for example]:\n").split(" ")))
constraintCoefficients = []
constraintValues = []
n = int(input("Enter number of constraints:\n"))
for i in range(n):
    constraintCoefficients.append(list(map(lambda x: float(x), input(f"Enter coefficients for constraint {i + 1} [\"1 2 3\", for example]:\n").split(" "))))
for i in range(n):
    constraintValues.append(float(input(f"Enter value for constraint {i + 1}:\n")))
eps = int(input("Enter accuracy:\n"))

solution = simplex(objectiveFunction, constraintCoefficients, constraintValues, eps)
print("Answer:", *solution)
