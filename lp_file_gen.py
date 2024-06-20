"""
COSC364 flow assignment 
Created by Yuxi (Harry) Chen
01/05/24
"""
import sys

MAX_PATH_NUM = 2

def createDemandConstraint(s,t,d):
    """creates the demand volmue ( hij = i+j) for a path from source->transit->destination (Xijk) 
        returns a string
    """
    string = "\n\CONSTRAINTS \n"
    for i in range(1, s + 1):
        for j in range(1, d + 1):
            for k in range(1,t + 1):
                if k == t:
                    string += f"x{i}{k}{j} = {i + j} \n"
                else:
                    string += f"x{i}{k}{j} + " 
    return string

def createStoTCapacity(s,t,d): 
    """Calculate capacity contraints for each link from source to transit nodes 
        returns a string
    """
    string = "\n\CAPACITY FOR SOURCE TO TRANSIT \n"
    for i in range(1, s+1):
        for k in range(1, t+1):
            for j in range(1,d+1):
                if j == d:
                    string += f"x{i}{k}{j} - c{i}{k} = 0 \n"
                else:
                    string += f"x{i}{k}{j} + "
    return string

def createTtoDCapacity(s,t,d): 
    """Calculate capacity contraints for each link from transit to dest nodes"""
    string = "\n\CAPCITY FOR TRANSIT TO DEST \n"
    for k in range(1,t + 1):
        for j in range(1, d + 1):
            for i in range(1, s + 1):
                if i == s:
                    string += f"x{i}{k}{j} - d{k}{j} = 0 \n"
                else:
                    string += f"x{i}{k}{j} + "
    return string

def createNonNegativityConstraints(s,t,d):
    """Create non-negative constraints onto variables"""
    string = "\nBOUNDS \nr >= 0 \n"
    #Ensure non-negativity for each path
    for i in range(1, s + 1):
        for k in range(1,t + 1):
            for j in range(1, d + 1):
                string+=f"x{i}{k}{j} >= 0 \n"

    #Ensure non-negative capacity from Source to transit
    for i in range(1, s + 1):
        for k in range(1, t + 1):
            string+=f"c{i}{k} >= 0\n"

    #Ensure non-negative capacity from transit to destination 
    for k in range(1,t+1):
        for j in range(1,d+1):
            string += f"d{k}{j} >= 0 \n"
    return string

def createDemandFlow(s,t,d): 
    """Calculates and returns a string for the equal path flow requirement"""
    string = "\n\DEMAND FLOW \n"
    for i in range(1, s + 1):
        for k in range(1, t+ 1):
            for j in range(1, d + 1):
                string += (f"2x{i}{k}{j} - {i + j}u{i}{k}{j} = 0 \n")
    return string

def createMaxPathConstraint(s,t,d):
    """Ensure 2 active transit nodes( max path is 2 ) and return it as a string"""
    #Ensure 2 path max per source to destination (from specs)
    string = "\n\BINARY VARIABLES \n"
    for i in range(1,s + 1):
        for j in range(1, d + 1):
            for k in range(1, t + 1):
                if k == t:
                    string += (f"u{i}{k}{j} = {MAX_PATH_NUM} \n")
                else:
                    string += (f"u{i}{k}{j} + ")
    return string

def createTransitLoad(s,t,d): 
    """Calculate load constraint for each path and return it as a String"""
    string = "\n\TRANSIT LOAD CONSTRAINTS\n"
    #Calculate the sum of each transit load
    for k in range (1, t + 1):
        for i in range(1, s + 1):
            for j in range(1,d + 1):
                if (j == d) and (i == s):
                    string += (f"x{i}{k}{j} - r <= 0 \n") 
                else:
                    string += (f"x{i}{k}{j} + ")
    return string

def createBinaryVariables(s,t,d): 
    """create binary variables and return it as a String"""
    string = "\nBINARY \n"
    for i in range(1,s+1):
        for j in range(1, d + 1):
            for k in range(1, t + 1):
                string += (f"u{i}{k}{j} \n")
    return string

def generateLPFile(s,t,d):
    """Create LP file based on required specifications
        Note: 
        total Source nodes = s
        total transit nodes = t
        total destination nodes = d

        individual Source node = i,
        individual Transit node = k,
        individual Destination node = j
    """
    with open(f"{s}{t}{d}.lp", "w") as file:
        file.write("MINIMIZE \nr \n\nSUBJECT TO \n")
        file.write(createDemandConstraint(s,t,d))
        file.write(createStoTCapacity(s,t,d))
        file.write(createTtoDCapacity(s,t,d))
        file.write(createTransitLoad(s,t,d))
        file.write(createDemandFlow(s,t,d))
        file.write(createMaxPathConstraint(s,t,d))
        file.write(createNonNegativityConstraints(s,t,d))
        file.write(createBinaryVariables(s,t,d))
        file.write("END \n")

def checkInputParameters():
    """Check correct inputs from user"""
    try: 
        #Assume the user knows that nodes can't be negative
        source, transit, dest = abs(int(sys.argv[1])), abs(int(sys.argv[2])), abs(int(sys.argv[3]))
        if (transit >= MAX_PATH_NUM): 
            return [source, transit, dest]
        else: 
            print("Incorrect arguments are given: Transit nodes must be >= 2 ")
    except Exception as e: 
        print(f"Error: {e}.")
    
def main(): 
    userInputs = checkInputParameters()
    if userInputs:
        generateLPFile(userInputs[0], userInputs[1], userInputs[2])

if __name__ == "__main__": 
    main()
    