from typing import List

def simplex(objectiveFunction: List[int], constraintCoefficients: List[List[int]], constraintValues: List[int], eps: int = 0.00001) -> tuple:
    if len(constraintCoefficients) != len(constraintValues):
        raise ValueError("Constraints mentioned improperly")

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

    return (x, maximumFunctionValue)

solution = simplex([9,10,16],[[18,15,12],[6,4,8],[5,3,3]],[360,192,180])
print(solution)


