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

from cmath import cos
from pathlib import Path
from unittest.mock import sentinel
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

class Info(object):
    def __init__(self, locations, directions, cost):
        self.locations = locations
        self.directions = directions
        self.cost = cost

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    #define the start state and action
    Nowaction='NULL'
    NowState=problem.getStartState()
    path = Info([NowState],[],0)
    if problem.isGoalState(NowState):
        return []
    #list for all the path it have visited
    seen=list()
    seen.append(NowState)  
    #use the util stack to finish this 
    stack = util.Stack()
    stack.push(path)

    while stack.isEmpty()==False:
        currentInfo = stack.pop()
        currentLocation = currentInfo.locations[-1]
        if problem.isGoalState(currentLocation):
            return currentInfo.directions
        else:
            for nextLocation, nextDirection, nextCost in problem.getSuccessors(currentLocation):
                if nextLocation not in currentInfo.locations:
                    nextLocations = currentInfo.locations[:]
                    nextLocations.append(nextLocation)
                    nextDirections = currentInfo.directions[:]
                    nextDirections.append(nextDirection)
                    nextCosts = currentInfo.cost + nextCost
                    nextInfo = Info(nextLocations, nextDirections, nextCosts)
                    stack.push(nextInfo)
    return []

    #util.raiseNotDefined()
   


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    #get started
    NowState=problem.getStartState()
    Nowaction='NULL'
    cost=0
    path = Info([ NowState],[],0)

    if(problem.isGoalState(NowState)):
        return []
    queue = util.Queue()
    queue.push(path)
    seen=list()
    seen.append(NowState)

    while queue.isEmpty()==False:
        currentInfo = queue.pop()
        currentLocation = currentInfo.locations[-1]
        if problem.isGoalState(currentLocation):
            return currentInfo.directions
        else:
            for nextLocation, nextDirection, nextCost in  problem.getSuccessors(currentLocation):
                if (nextLocation not in currentInfo.locations) and (nextLocation not in seen):
                    if not problem.isGoalState(nextLocation):
                        seen.append(nextLocation)
                    nextLocations = currentInfo.locations[:]
                    nextLocations.append(nextLocation)
                    nextDirections = currentInfo.directions[:]
                    nextDirections.append(nextDirection)
                    nextCosts = currentInfo.cost + nextCost
                    nextInfo = Info(nextLocations, nextDirections, nextCosts)
                    queue.push(nextInfo)
    return []
    #util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    NowState=problem.getStartState()
    Nowaction='NULL'
    cost=0
    path = Info([NowState],[],0)

    if(problem.isGoalState(NowState)):
        return []
    #use the PriorityQueue to finish the UCS
    #And the cost shows the priority
    queue = util.PriorityQueue()
    queue.push(path, 0)
    seen = list()
    seen.append(NowState)

    while queue.isEmpty()==False:
        currentInfo = queue.pop()
        currentLocation = currentInfo.locations[-1]
        if problem.isGoalState(currentLocation):
            return currentInfo.directions
        else:
            #print( problem.getSuccessors(currentLocation))
            for nextLocation, nextDirection, nextCost in problem.getSuccessors(currentLocation):
                if (nextLocation not in currentInfo.locations) and (nextLocation not in seen):
                    if not problem.isGoalState(nextLocation):
                        seen.append(nextLocation)
                    nextLocations = currentInfo.locations[:]
                    nextLocations.append(nextLocation)
                    nextDirections = currentInfo.directions[:]
                    nextDirections.append(nextDirection)
                    nextCosts = currentInfo.cost + nextCost
                    nextInfo = Info(nextLocations, nextDirections, nextCosts)
                    queue.push(nextInfo, nextCosts)
    return []
    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    
    NowState=problem.getStartState()
    Nowaction='NULL'
    cost=0
    path = Info([NowState],[],0)
    if(problem.isGoalState(NowState)):
        return []
    #use the PriorityQueue to finish the A*
    #And the cost shows the priority
    queue = util.PriorityQueue()
    queue.push(path, 0)
    seen = list()
    seen.append(NowState)

    while queue.isEmpty()==False:
        currentInfo = queue.pop()
        currentLocation = currentInfo.locations[-1]
        if problem.isGoalState(currentLocation):
            return currentInfo.directions
        else:
            for nextLocation, nextDirection, nextCost in problem.getSuccessors(currentLocation):
                if (nextLocation not in currentInfo.locations) and (nextLocation not in seen):
                    if not problem.isGoalState(nextLocation):
                        seen.append(nextLocation)
                    nextLocations = currentInfo.locations[:]
                    nextLocations.append(nextLocation)
                    nextDirections = currentInfo.directions[:]
                    nextDirections.append(nextDirection)
                    nextCosts = currentInfo.cost + nextCost
                    #This is the difference 
                    nextHeuristic = heuristic(nextLocation, problem)
                    nextInfo = Info(nextLocations, nextDirections, nextCosts)
                    queue.push(nextInfo, nextCosts + nextHeuristic)

    return []
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
