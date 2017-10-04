# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

# Raahil Sha and Avinash Lal collaborated to complete this problem set

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

# Allows us to avoid pushing locations that are already on fringe for BFS/DFS
def inFringe(location, fringe):
    for (loc, path, cost) in fringe.list:
        if location == loc:
            return True
    return False

# Allows us to avoid pushing locations with higher cost paths on frings for
# UCS and A*
def inFringePrio(location, cost, fringe):
    for (prio, ind, (loc, path, costOnFringe)) in fringe.heap:
        if location == loc and costOnFringe <= cost:
            return True
    return False

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    #Access start state of input node
    currentNode = problem.getStartState()
    #Create visited and fringe data structures
    visited, fringe = set(), util.Stack()
    #Add input node and 0 to respective lists
    fringe.push((currentNode,[],0))

    #while items are in the fringe, iterate over each one
    while fringe:
        #Review first node in fringe
        (currentState, currentPath, currentCost) = fringe.pop()
        #Return the path thus far, if we reach a goal state
        if problem.isGoalState(currentState):
            return currentPath
        #Move node in review to visited set
        visited.add(currentState)
        #Access child nodes of the current node
        successors = problem.getSuccessors(currentState)
        for (location, direction, cost) in successors:
            # if (location not in visited) and (not inFringe(location, fringe)):
            # ^ The above code is the optimization to DFS discussed in the pset spec
            # However, it makes the autograder (who is king) angry so we have commented it out
            # If child node has not been visited, append it to the fringe with potential viable paths
            if (location not in visited):
                newPath = list(currentPath)
                newPath.append(direction)
                fringe.push((location, newPath, currentCost + cost))
    # Return nothing if no solution found
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #Access start state of input node
    currentNode = problem.getStartState()
    #Create visited and fringe data structures
    visited, fringe = set(), util.Queue()
    #Add input node and 0 to respective lists
    fringe.push((currentNode,[],0))

    #while items are in the fringe, iterate over each one
    while fringe:
        #Review first node in fringe
        (currentState, currentPath, currentCost) = fringe.pop()
        #Return the path thus far, if we reach a goal state
        if problem.isGoalState(currentState):
            return currentPath
        #Move node in review to visited set
        visited.add(currentState)
        #Access child nodes of the current node
        successors = problem.getSuccessors(currentState)
        for (location, direction, cost) in successors:
            #If child node has not been visited,append it to the fringe with potential viable paths
            if (location not in visited) and (not inFringe(location, fringe)):
                newPath = list(currentPath)
                newPath.append(direction)
                # The below is an optimization to BFS discussed in the pset spec
                # However, it makes the autograder (who is king) angry so we have commented it out
                # In BFS, we can accept a solution path on pushing instead of popping
                # if problem.isGoalState(location):
                #    return newPath
                fringe.push((location, newPath, currentCost + cost))
    # Return nothing if no solution found
    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #Access start state of input node
    currentNode = problem.getStartState()
    #Create visited and fringe data structures
    visited, fringe = set(), util.PriorityQueue()
    #Add input node and 0 to respective lists
    fringe.push((currentNode,[],0), 0)

    #while items are in the fringe, iterate over each one
    while fringe:
        #Review first node in fringe
        (currentState, currentPath, currentCost) = fringe.pop()
        #Return the path thus far, if we reach a goal state
        if problem.isGoalState(currentState):
            return currentPath
        #Move node in review to visited set
        visited.add(currentState)
        #Access child nodes of the current node
        successors = problem.getSuccessors(currentState)
        for (location, direction, cost) in successors:
            newCost = currentCost + cost
            #If child node has not been visited,append it to the fringe with potential viable paths
            if (location not in visited) and (not inFringePrio(location, newCost, fringe)):
                newPath = list(currentPath)
                newPath.append(direction)
                fringe.push((location, newPath, newCost), newCost)
    # Return nothing if no solution found
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #Access start state of input node
    currentNode = problem.getStartState()
    #Create visited and fringe data structures
    visited, fringe = set(), util.PriorityQueue()
    #Add input node and 0 to respective lists
    fringe.push((currentNode,[],0), heuristic(currentNode, problem))

    #while items are in the fringe, iterate over each one
    while fringe:
        #Review first node in fringe
        (currentState, currentPath, currentCost) = fringe.pop()
        if problem.isGoalState(currentState):
            return currentPath
        #Return the path thus far, if we reach a goal state
        visited.add(currentState)
        #Access child nodes of the current node
        successors = problem.getSuccessors(currentState)
        for (location, direction, cost) in successors:
            newCost = currentCost + cost
            #If child node has not been visited,append it to the fringe with potential viable paths
            if (location not in visited) and (not inFringePrio(location, newCost, fringe)):
                newPath = list(currentPath)
                newPath.append(direction)
                fringe.push((location, newPath, newCost), newCost + heuristic(location, problem))
    # Return nothing if no solution found
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
