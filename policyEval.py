# prints any 2D matrix
def printTable(table):
    for r in table:
        for c in r:
            print('{0: 1.2f}'.format(c), end = " ")
        print()
    return

# intializes value-function table
# terminals is a list of pairs [[row, col], [row, col], ...]
# if you would like to specify a value other than R for a square, use specialVals
# specialVals is a list of triples [[row, col, value], [row, col, value], ...]
def initializeTable(rows, cols, R, terminals, specialVals):
    newTable = [0] * rows
    for row in range(len(newTable)):
        newTable[row] = [R] * cols
    for terminal in terminals:
        row, col = terminal[0], terminal[1]
        if row < 0 or row > rows - 1 or col < 0 or col > cols - 1:
            print("Error: terminal index out of bounds, please try again.")
            break
        else: 
            newTable[row][col] = 0
    for specialVal in specialVals:
        row, col = specialVal[0], specialVal[1]
        if row < 0 or row > rows - 1 or col < 0 or col > cols - 1:
            print("Error: special value index out of bounds, please try again.")
            break
        else: 
            newTable[row][col] =  specialVal[2]
    return newTable

# returns next value after action (left, right, up, or down)
# row & col specify our starting position
# if action exceeds bounds of table, current value is returned (no action taken)
# assumes table[row][col] is within bounds
def returnNext(table, action, row, col):
    rowBound, colBound = len(table) - 1, len(table[0]) - 1 # assuming same num of items per col

    if action == "left":
        if col - 1 < 0:
            return table[row][col]
        else:
            return table[row][col - 1]
    elif action == "right":
        if col + 1 > colBound:
            return table[row][col]
        else:
            return table[row][col + 1]
    elif action == "up":
        if row - 1 < 0:
            return table[row][col]
        else:
            return table[row - 1][col]
    elif action == "down":
        if row + 1 > rowBound:
            return table[row][col]
        else:
            return table[row + 1][col]
    else:
        print("invalid action")
        return

# applies policy evaluation once 
def policyEval(table, terminals, R, y):
    newStateValueTable = initializeTable(len(table), len(table[0]), 0, [], [])
    for i in range(len(table)):
        for j in range(len(table[0])):
            directions = ["left", "right", "up", "down"]
            value = 0
            for direction in directions:
               value += (R + y * returnNext(table, direction, i, j))
            newStateValueTable[i][j] = value/4.0 # 4 is the number of actions (directions) we calculated for
    # reset terminal states
    for terminal in terminals:
        newStateValueTable[terminal[0]][terminal[1]] = 0
    return newStateValueTable

# applies policy evaluation k times
# prints table after each iteration 
def policyIterate(stateValueTable, terminals, R, y, k):
    print("k = 1")
    printTable(stateValueTable)
    print()

    i = 0
    while i < k - 1:
        print("k =", i + 2)
        newStateValueTable = policyEval(stateValueTable, terminals, R, y)
        printTable(newStateValueTable)
        print()
        stateValueTable = newStateValueTable
        i+=1
    
    return

# grabs user input for policy iteration 
def main(): 
    print("This program will apply policy iteration to any value-function table, with any transtion values, and gamma value!")
    print("First we need to determine your initial value-function table.")
    rows = int(input("Enter the number of rows you want your value-function to have: "))
    cols = int(input("Enter the number of columns you want your value-function to have: "))
    R = float(input("Enter the reinforcment value (R_t): "))

    print("Next we will specify the terminal states (value = 0) as a 2D matrix.")
    rowsT = int(input("Enter the number of rows for the terminal state matrix: ")) 
    terminals = []
    if rowsT > 0:
        colsT = 2
        print("For each terminal location, enter the row col following with a new line: ") 
        for i in range(rowsT):         
            a = list(map(int,input().strip().split()))[:colsT]
            terminals.append(a) 

    print("Does this value-function have any special values? (i.e. locations that have a value different than", R, ". Y or N.")
    answer = input()

    specialVals = []
    if answer == 'Y':
        print("Next we will specify the special value states as a 2D matrix.")
        rowsS = int(input("Enter the number of rows for the special value state matrix: ")) 
        colsS = 3
        print("For each special value location, enter the row col value following with a new line: ") 
        for i in range(rowsS):    
            vals = input().strip().split()
            a = [int(vals[0]), int(vals[1]), float(vals[2])]     
            specialVals.append(a) 

    y = float(input("Enter the gamma value (between 0 and 1 inclusive) you want your value-function to have: "))
    k = int(input("Enter the number of iterations of policy evaluation: "))

    print("Does this function-value table look correct?")
    valueFunction = initializeTable(rows, cols, R, terminals, specialVals)
    printTable(valueFunction)
    print("If so, press Y to proceed. If not, press N to restart.")
    answer2 = input()

    if answer2 == 'Y':
        policyIterate(valueFunction, terminals, R, y, k)
    if answer2 == 'N':
        main()

    return

main()