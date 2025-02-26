class Cell:
    def __init__(self, condition):
        self.condition = condition
    def __str__(self):
        return f"|{self.condition}|"
    
c = Cell("clean")
d = Cell("dirty")


class State:
    def __init__(self, agentLoc, cellsList):
        self.agentLoc = agentLoc
        self.cellsList = cellsList
    def __str__(self):
        printS = ""
        count =  0
        for a in self.cellsList:
            printS += a.__str__()
            if count == self.agentLoc:
                sentence_list = list(printS)
                sentence_list.insert(len(sentence_list) - 1, " *")
                printS = "".join(sentence_list)
            count += 1
        return printS
    # comparing for two states in problem.isgoal()
    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        if self.agentLoc != other.agentLoc:
            return False
        if len(self.cellsList) != len(other.cellsList):
            return False
        for i in range(len(self.cellsList)):
            if self.cellsList[i].condition != other.cellsList[i].condition:
                return False
        return True
    # got the idea from stack overflow to hash the key of an object function for reached
    def __hash__(self):
        hash_value = hash(self.agentLoc)
        for i, cell in enumerate(self.cellsList):
            hash_value ^= hash((i, cell.condition))
        return hash_value
    

cellList= [Cell("dirty"),Cell("dirty"), Cell("dirty")]

state_1 = State(2, cellList)
#print(state_1)

cellList_3 = [Cell("clean"),Cell("clean"), Cell("clean")]
state_2 = State(1, cellList_3)
#print(state_2)
cellList_4 = [Cell("dirty"),Cell("dirty"), Cell("clean")]
state_3 = State(2, cellList_3)
#print(state_3)


class Node:
    def __init__(self, pathCost, children, state, parent, nodeID):
        self.pathCost = 1
        self.children = []
        self.state = state
      
        self.parent = parent
        self.nodeID = nodeID
    def __str__(self):
        string = ""
        string += f"Node(PathCost:{self.pathCost}, State: {self.state.__str__()},  ID: {self.nodeID}, children:["
        for child in self.children:
            string += f"{child.nodeID}, "
        if self.parent != None:
            string += "], " + "Parent: " + str(self.parent.nodeID)
        else:
            string += "], " + "Parent: None" 

                       
        return string + ")"




class Problem:
    def __init__(self, initialState, goalState):
        self.initialState = initialState # the start state 
        self.goalState = goalState

    def is_goal(self, state):
        """
        Function checks if the current state is goal state
        state: State Object
        returns: boolean
        """
        return (state == self.goalState)
    def actions(self, state):
        """
        Function returns action based on the state 
        state: State
        returns: actions  [clean, left, right, done]
        """
        action = ["clean", "left", "right"]
        #if agent is at the end and the current cell is clean
        if len(state.cellsList) - 1 == state.agentLoc:
            return [action[1], action[0]]
        #if agent is at the beginning
        if state.agentLoc == 0:
            return [action[0], action[2]]
        else:
            return action

    def action_cost(self, state, action, resultState):
        """
        Function calculates the action cost of doing an action on a state
        state: State Object
        resultState: State Object(result due action on s)
        action: action
        returns: UNKNOWN

        """
        return 1
    def result(self, action, state):
        """
        Fuction calculates the resultant state due to the action
        action: action
        state: State Object
        returns: State Object
        """
        new_cells = [Cell(cell.condition) for cell in state.cellsList]
        if action == "left":
            return State(state.agentLoc - 1, new_cells)
        elif action == "right":
            return State(state.agentLoc + 1, new_cells)
        else:# if action is clean.
            new_cells[state.agentLoc].condition = "clean"
            return State(state.agentLoc, new_cells)

root = Node(state = state_1,  parent= None, children=[], pathCost = 0, nodeID= "A")

child1 = Node(state= state_2, children= [], parent = root, pathCost= 0,  nodeID="B")
child2 = Node(state= state_3, children= [], parent = child1, pathCost= 0,  nodeID= "C")

root.children.append(child1)
child1.children.append(child2)


"""
My logic is that it will sort them based on how close there are to the goal state.
- My thinking is to check the less number of dirty cell
- Also to check how close the agent is to the dirty cell


"""
def evaluation_fn(node: Node):
  num_of_dirty = 0
  min_distance = float("inf")
  for i, cell in enumerate(node.state.cellsList):

     if cell.condition == "dirty":
       num_of_dirty += 1
       min_distance = min(min_distance, abs(i - node.state.agentLoc))

  
  return num_of_dirty + (min_distance / 5)


def is_empty(frontier):
    """
    function checks if frontier is empty
    """
    return len(frontier) == 0

def pop(frontier):
    """
    function returns the first node at the frontier
    """    
    return frontier.pop(0)

def expand(problem, node):
    """
     function EXPAND(problem,node) yields nodes
        s= node.STATE
        for each action in problem.ACTIONS(s) do
            s_prime =  problem.RESULT(s,action)
            cost = node.PATH-COST + problem.ACTION-COST(s,action,s)
            yield NODE(STATE=s, PARENT=node, ACTION=action, PATH-COST=cost)
    function returns children based on the parent node 
    """
    node_list = []
    state = node.state
    count = 1
    for action in problem.actions(state):
        resultant_state = problem.result(action, state)
        cost = node.pathCost + problem.action_cost(state, action, resultant_state)
        node_list.append(Node(pathCost= 1, children=[], state= resultant_state, parent = node, nodeID= count))
        count += 1
    return node_list






def best_first_search(problem, eval_f):
    node = Node(pathCost= 1, children=[], state= problem.initialState, parent=None, nodeID=0)
    #lookup table with initial state and node
    reached = {problem.initialState : node}
    #frontier with node as the first element
    frontier = [node]

    while not is_empty(frontier):
        node = pop(frontier)
        if problem.is_goal(node.state):
            return node
        for child in expand(problem, node):
            s = child.state
            if s not in reached or child.pathCost < reached[s].pathCost:
                reached[s] = child
                frontier.append(child)
                frontier.sort(key=eval_f)
    return "failure"
        

p = Problem(state_1, state_2)

node = best_first_search(problem=p, eval_f= evaluation_fn)
while node != None:
    print(node.state)
    node = node.parent











        
     



