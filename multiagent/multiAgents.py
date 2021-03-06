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

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
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

    def evaluationFunction(self, currentGameState, action):
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
        curFood = currentGameState.getFood().asList()
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # Get the Food Positions
        # Use weighted distance for the Food points and Ghosts
        # For better score, we are considering the Farthest available food point and nearest ghost

        Foodposition = newFood.asList()
        foodscores = []
        ghostScores = []
        ghostFactor = -.5
        if (newPos in curFood):
            farthestFood = 2
        else:
            for food in Foodposition:
                foodscores.append(1 / float((1 + manhattanDistance(newPos, food))))
            farthestFood = max(foodscores)
        for ghostState in newGhostStates:
            ghostScores.append(1 / float(1 + manhattanDistance(newPos, ghostState.configuration.getPosition())))

        closestGhost = min(ghostScores)
        sumOfGhosts = sum(ghostScores)

        if (closestGhost <= .6):
            ghostFactor = -2

        return farthestFood + ghostFactor * sumOfGhosts + successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
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
        self.actionValueDictionary = {}  #Dictionary for holding the actions

    # Function for checking if the Terminal state is reached
    # If game is won or lost or maximum depth (terminal nodes) is reached
    def isTerminalState(self,gameState,depth):
        endOfgame = False
        if( gameState.isWin() or gameState.isLose()):
            endOfgame =True
        elif(depth == self.depth):
            endOfgame = True

        return endOfgame

    def utilityFunction(self,gameState):
        return self.evaluationFunction(gameState)

    # We perform depth first search till the leaf node. Once we reach the leaf node
    # we get the value from the utility evaluation function. We keep on generating
    # all the successors resulting from legal actions available from any particular
    # state. We have to keep multiple "min" layers in case of multiple ghosts for
    # each "max" layer.

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    # Maximizer function tries to return the maximum value possible from the available values
    def maxValue(self,gameState,depth,agentIndex):
        if( self.isTerminalState(gameState,depth)):
                return self.utilityFunction(gameState)
        v = float("-inf")
        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            #print( "Agent"  + str(agentIndex) + action )
            actionValue = self.minValue(gameState.generateSuccessor(agentIndex , action), depth, agentIndex + 1)
            if(agentIndex == 0 and depth == 0 ):
                self.actionValueDictionary[actionValue] = action
            v=  max(v,actionValue)
        return v

    # Minimizer function tries to return the minimum value from the values available

    def minValue(self,gameState,depth,agentIndex):
        if( self.isTerminalState(gameState,depth)):
                return self.utilityFunction(gameState)
        v = float("+inf")
        actions = gameState.getLegalActions(agentIndex)

        # current agent is the last ghost then increase depth by one since one ply is completed
        if(agentIndex == gameState.getNumAgents() -1 ) :
            for action in actions:
                #print("Agent" + str(agentIndex) + action)
                v=  min(v, self.maxValue(gameState.generateSuccessor(agentIndex, action), depth + 1, 0))
        else :
            for action in actions:
                #print("Agent" + str(agentIndex) + action)
                v = min(v, self.minValue(gameState.generateSuccessor(agentIndex , action), depth, agentIndex + 1))
        return v

    # Returns the best possible action from root based on backed up values from leaf nodes to root
    # by alternating between "min" and "max" layers

    def getAction(self, gameState):
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
        """
        self.actionValueDictionary = {}
        v =  self.maxValue(gameState,0,0)
        #print("[" + str(v) + " " + str(self.actionValueDictionary[v]) + "]");
        return self.actionValueDictionary[v]
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    # We perform depth first search till the leaf node. Once we reach the leaf node
    # we get the value from the utility evaluation function. We keep on generating
    # all the successors resulting from legal actions available from any particular
    # state. We have to keep multiple "min" layers in case of multiple ghosts for
    # each "max" layer. We applied pruning to those branches which we are sure the
    # maximizer will never take. If already found value at a leaf node is greater
    # than the next subtree at the minimizer, we would stop our search through that
    # subtree and proceed for next. We continue this till the end and pruning all
    # the necessary branches.

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def maxValue(self,gameState,depth,agentIndex,alpha,beta):
        if( self.isTerminalState(gameState,depth)):
                return self.utilityFunction(gameState)
        v = float("-inf")
        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            #print( "Agent"  + str(agentIndex) + action )
            actionValue = self.minValue(gameState.generateSuccessor(agentIndex , action), depth, agentIndex + 1,alpha,beta)
            if(agentIndex == 0 and depth == 0 ):
                self.actionValueDictionary[actionValue] = action
            v = max(v,actionValue)
            if(v > beta):
                return v
            alpha = max(alpha,v)
        return v

    def minValue(self,gameState,depth,agentIndex,alpha,beta):
        if( self.isTerminalState(gameState,depth)):
                return self.utilityFunction(gameState)
        v = float("+inf")
        actions = gameState.getLegalActions(agentIndex)

        # current agent is the last ghost then increase depth by one since one ply is completed
        if(agentIndex == gameState.getNumAgents() -1 ) :
            for action in actions:
                #print("Agent" + str(agentIndex) + action)
                v = min(v, self.maxValue(gameState.generateSuccessor(agentIndex, action), depth + 1, 0,alpha,beta))
                if(v < alpha):
                    return v
                beta = min(beta,v)
        else :
            for action in actions:
                #print("Agent" + str(agentIndex) + action)
                v = min(v, self.minValue(gameState.generateSuccessor(agentIndex , action), depth, agentIndex + 1,alpha,beta))
                if(v < alpha):
                    return v
                beta = min(beta,v)
        return v

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        self.actionValueDictionary = {}
        v = self.maxValue(gameState, 0, 0,float("-inf"),float("inf"))
        #print("[" + str(v) + " " + str(self.actionValueDictionary[v]) + "]");
        return self.actionValueDictionary[v]
        util.raiseNotDefined()

    # We perform depth first search till the leaf node. Once we reach the leaf node
    # we get the value from the utility evaluation function. We keep on generating
    # all the successors resulting from legal actions available from any particular
    # state. We have to keep multiple "min" layers in case of multiple ghosts for
    # each "max" layer. Instead of assuming the worst case scenario, i.e. the ghosts
    # always play optimally, we consider them playing randomly. So, instead of
    # taking the minimum of the values at "min", we calculated the average value.

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def maxValue(self,gameState,depth,agentIndex):
        if( self.isTerminalState(gameState,depth)):
                return self.utilityFunction(gameState)
        v = float("-inf")
        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            #print( "Agent"  + str(agentIndex) + action )
            actionValue = self.expValue(gameState.generateSuccessor(agentIndex , action), depth, agentIndex + 1)
            if(agentIndex == 0 and depth == 0 ):
                self.actionValueDictionary[actionValue] = action
            v = max(v,actionValue)
        return v

    def expValue(self,gameState,depth,agentIndex):
        #To keep track of total number of utility
        count = 0.0
        if( self.isTerminalState(gameState,depth)):
                return self.utilityFunction(gameState)
        v = 0.0
        actions = gameState.getLegalActions(agentIndex)

        # current agent is the last ghost then increase depth by one since one ply is completed
        if(agentIndex == gameState.getNumAgents() -1 ) :
            for action in actions:
                #print("Agent" + str(agentIndex) + action)
                v += self.maxValue(gameState.generateSuccessor(agentIndex, action), depth + 1, 0)
                count += 1.0
        else :
            for action in actions:
                #print("Agent" + str(agentIndex) + action)
                v += self.expValue(gameState.generateSuccessor(agentIndex , action), depth, agentIndex + 1)
                count += 1.0

        return (v/count)

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        self.actionValueDictionary ={}
        v =  self.maxValue(gameState,0,0)
        #print("[" + str(v) + " " + str(self.actionValueDictionary[v]) + "]");
        return self.actionValueDictionary[v]
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

