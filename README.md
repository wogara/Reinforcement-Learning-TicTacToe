# Reinforcement-Learning-TicTacToe

This a some code I implemented to teach an algorithm how to play tic tac toe using a simple reinforcement learning algorithm.
The state of every game is recorded in a dictionary along with its value accoring to the equation below. 

StateValue = LearningRate*(NextValueState*decay - StateValue)

The value of a state gets updated after the end of every game. The final state gets rewarded a 1 if that player won, a -1 if that player lost, and a 0 if the game ended in a tie. 

Each player has a hash table with values with which it can make its choice based on which state has the highest value. During training, each player chooses to either exploit the hash table and make the best decision or explore by selecting a random option.




