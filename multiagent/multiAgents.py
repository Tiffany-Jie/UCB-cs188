# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #close to win!
        if successorGameState.isWin():
            return float("inf")

        #close to the goast!
        """currentPos = currentGameState.getPacmanPosition()
        currentGoastStates = currentGameState.getGhostStates()
        currentDistanceMin=10000000
        for currentGoast in currentGoastStates:
            currentDistance = util.manhattanDistance(currentGoast.getPosition,currentPos)
            if currentDistance < currentDistanceMin:
                currentDistanceMi =currentDistance
        """
        goastScore = 0
        #too dangerous!
        for goast in newGhostStates:
            if util.manhattanDistance(goast.getPosition(),newPos)<2:
                return float("-inf")
        newDistanceMin=1000000
        """for goast in currentGoastStates:
            newDistance = util.manhattanDistance(goast.getPosition,currentPos)
            if newDistance < newDistanceMin:
                 newDistanceMin = newDistance
        if newDistance < currentDistance:
            goastScore = -40
        elif newDistance > currentDistance:
            goastScore = 40
        """
        #close to the food!
        #number
        if currentGameState.getNumFood() > successorGameState.getNumFood():
            foodScore = 400
        else:
            foodScore = 0
        #distance
        foodDistance = []
        for food in list(newFood.asList()):
            foodDistance.append(util.manhattanDistance(food, newPos))
        
        return successorGameState.getScore() - 5*min(foodDistance) + foodScore #+goastScore
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)

    your minimax tree will have multiple min layers (one for each ghost) 
    for every max layer.

    Your code should also expand the game tree to an arbitrary depth. 
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #for depth == 0
        currentDepth=0
        maxValue = float('-inf')
        maxAction = Directions.STOP

        #all the legal actions, which one is best:
        for action in gameState.getLegalActions(0):
            nextState = gameState.generateSuccessor(0, action)
            nextValue = self.next_value(nextState, currentDepth, 1)
            if nextValue > maxValue:
                maxValue = nextValue
                maxAction = action
        return maxAction

    def next_value(self, gameState, currentDepth, agentIndex):
        #search to the limit depth of the tree:
        if currentDepth == self.depth:
            return self.evaluationFunction(gameState)
        # win or lose
        # I'm a little bit confused by the isWin() and isLose()
        elif (gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        # nextTurn is pacman
        elif agentIndex == 0:
            return self.max_value(gameState,currentDepth)
        # nextTurn is goast
        else:
            return self.min_value(gameState,currentDepth,agentIndex)
    #should define max/min for pacman and other goasts

    def max_value(self, gameState, currentDepth):
        maxValue = float('-inf')
        for action in gameState.getLegalActions(0):
            nextValue = self.next_value(gameState.generateSuccessor(0, action), currentDepth, 1)
            maxValue = max(maxValue, nextValue)
        return maxValue

    
    def min_value(self, gameState, currentDepth, agentIndex):
        minValue = float('inf')
        for action in  gameState.getLegalActions(agentIndex):
            #next turn is pacman
            if agentIndex == gameState.getNumAgents()-1:
                nextValue = self.next_value(gameState.generateSuccessor(agentIndex, action), currentDepth+1, 0)
            #next turn is another goast
            else:
                nextValue = self.next_value(gameState.generateSuccessor(agentIndex, action), currentDepth, agentIndex+1)
            minValue = min(minValue, nextValue)
        return minValue

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
#        util.raiseNotDefined()
        currentDepth=0
        maxValue = float('-inf')
        maxAction = Directions.STOP

        a = float('-inf')
        b = float('inf')
        #all the legal actions, which one is best:
        for action in gameState.getLegalActions(0):
            nextState = gameState.generateSuccessor(0, action)
            nextValue = self.next_value(nextState, currentDepth, 1, a, b)
            if nextValue > maxValue:
                maxValue = nextValue
                maxAction = action
            a = max(a, maxValue)
        return maxAction

    def next_value(self, gameState, currentDepth, agentIndex, a, b):
        #search to the limit depth of the tree:
        if currentDepth == self.depth:
            return self.evaluationFunction(gameState)
        # win or lose
        # I'm a little bit confused by the isWin() and isLose()
        elif (gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        # nextTurn is pacman
        elif agentIndex == 0:
            return self.max_value(gameState,currentDepth,a, b)
        # nextTurn is goast
        else:
            return self.min_value(gameState,currentDepth,agentIndex, a, b)
    #should define max/min for pacman and other goasts

    def max_value(self, gameState, currentDepth, a, b):
        maxValue = float('-inf')
        for action in gameState.getLegalActions(0):
            nextValue = self.next_value(gameState.generateSuccessor(0, action), currentDepth, 1, a, b)
            maxValue = max(maxValue, nextValue)
            if maxValue > b:
                return maxValue
            a = max(a, maxValue)
        return maxValue

    
    def min_value(self, gameState, currentDepth, agentIndex, a, b):
        minValue = float('inf')
        for action in  gameState.getLegalActions(agentIndex):
            #next turn is pacman
            if agentIndex == gameState.getNumAgents()-1:
                nextValue = self.next_value(gameState.generateSuccessor(agentIndex, action), currentDepth+1, 0, a, b)
            #next turn is another goast
            else:
                nextValue = self.next_value(gameState.generateSuccessor(agentIndex, action), currentDepth, agentIndex+1, a, b)
            minValue = min(minValue, nextValue)
            if minValue < a:
                return minValue
            b = min(b, minValue)
        return minValue

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        #for depth == 0
        currentDepth=0
        maxValue = float('-inf')
        maxAction = Directions.STOP

        #all the legal actions, which one is best:
        for action in gameState.getLegalActions(0):
            nextState = gameState.generateSuccessor(0, action)
            nextValue = self.next_value(nextState, currentDepth, 1)
            if nextValue > maxValue:
                maxValue = nextValue
                maxAction = action
        return maxAction

    def next_value(self, gameState, currentDepth, agentIndex):
        #search to the limit depth of the tree:
        if currentDepth == self.depth:
            return self.evaluationFunction(gameState)
        # win or lose
        # I'm a little bit confused by the isWin() and isLose()
        elif (gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        # nextTurn is pacman
        elif agentIndex == 0:
            return self.max_value(gameState,currentDepth)
        # nextTurn is goast
        else:
            return self.ave_value(gameState,currentDepth,agentIndex)
    #should define max/min for pacman and other goasts

    def max_value(self, gameState, currentDepth):
        maxValue = float('-inf')
        for action in gameState.getLegalActions(0):
            nextValue = self.next_value(gameState.generateSuccessor(0, action), currentDepth, 1)
            maxValue = max(maxValue, nextValue)
        return maxValue

    
    def ave_value(self, gameState, currentDepth, agentIndex):
        #minValue = float('inf')
        aveValue=0
        nextValues=[]
        for action in  gameState.getLegalActions(agentIndex):
            #next turn is pacman
            if agentIndex == gameState.getNumAgents()-1:
                nextValue = self.next_value(gameState.generateSuccessor(agentIndex, action), currentDepth+1, 0)
            #next turn is another goast
            else:
                nextValue = self.next_value(gameState.generateSuccessor(agentIndex, action), currentDepth, agentIndex+1)
            aveValue += nextValue
            nextValues.append(nextValue)
            #minValue = min(minValue, nextValue)
        #return random.choice(nextValues)
        return aveValue


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    This function is quite similar to the evaluationFunction() in ReflexAgent calss.
     
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    #close to win!
    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return float("-inf")
    #close to the goast!
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    currentDistanceMin=10000000
    currentDistanceMax=0
    ghostScore = 0
    for ghost in newGhostStates:
        currentDistance = manhattanDistance(newPos, newGhostStates[0].getPosition())
        if currentDistance > 0:
            if ghost.scaredTimer > 0:
                ghostScore += 100/currentDistance
            else:
                ghostScore -= 10/currentDistance
        if currentDistance < currentDistanceMin:
            currentDistanceMin =currentDistance
        if currentDistance > currentDistanceMax:
            currentDistanceMax =currentDistance
         #too dangerous?
        if currentDistance < 2:
            return float("-inf")

        #close to the food!
        #distance
    foodDistance = []
    for food in list(newFood.asList()):
        foodDistance.append(util.manhattanDistance(food, newPos))
        
    return scoreEvaluationFunction(currentGameState) - 5*min(foodDistance) - 6*currentGameState.getNumFood() +ghostScore#+ 1.5*currentDistanceMin + currentDistanceMax #+ ghostScore 
    #return successorGameState.getScore()


# Abbreviation
better = betterEvaluationFunction
