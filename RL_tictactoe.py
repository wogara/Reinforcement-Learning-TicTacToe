from array import *
from random import seed
from random import random
import random

learning_rate = .2
decay = .7

board = [["1","2","3"],["4","5","6"],["7","8","9"]] #board shown on the terminal
state = ["1", "2", "3", "4", "5","6","7","8","9"] #current state

available_spaces = ["1", "2", "3", "4", "5", "6", "7", "8", "9"] #all the spaces available during a game
gamestates = [str(state)] #array to store all the states from one game
Xstate_hash = {str(state):0} #hash table to store all the states through all games

Xwins = 0 #number of wins for "X" player
Owins = 0 #number of wins for 
ties = 0 #number of ties

#gamestates = [str(state)] #array to store all the states from one game
Ostate_hash = {str(state):0} #hash table to store all the states through all games

player_X = 1 #integer to decide which player has turn (1 = X, 0 = O)


def clear_board():
    #used to clear board, i don't think i'll need this
	global board
	board = [["1","2","3"],["4","5","6"],["7","8","9"]]

def changesides():
    #changes the player after each turn
    global player_X
    if (player_X == 1):
        player_X = 0
    else:
        player_X = 1

def explore(checkplayer):
    #function to explore, if checkplayer == 1 then it executes random choice for x
    global state, available_spaces
 
    if (checkplayer == 1):
        t = random.choice(available_spaces)
        symbol = 'X'
    else:
        t = random.choice(available_spaces)
        symbol = 'O'

    for z in range(0,9):
        if (state[z] == t):
            state[z] = symbol

    if (Xstate_hash.get(str(state)) == None):
        Xstate_hash[str(state)] = 0

    if (Ostate_hash.get(str(state)) == None):
        Ostate_hash[str(state)] = 0

    available_spaces.remove(t)
    gamestates.append(str(state))


def makeboard():
    #this function updates the board and shows it (for demonstration)
    global board, state, Xwins, Owins

    c = 0
    r = 0
    for x in range(0,9):
        print("|" + state[x] + "|",end = "")
        board[r][c] = state[x]
        c = c + 1
        if (x == 2 or x == 5 or x == 8):
            r = r + 1
            c = 0
            print()

    print("player 1 wins: " + str(Xwins) + ", player 2 wins: " + str(Owins) + ", ties: " + str(ties))

def update_board():
    #this function updates the board without showing it (for use during training)
    global board, state, Xwins, Owins
    c = 0
    r = 0
    for x in range(0,9):
        #print("|" + state[x] + "|",end = "")
        board[r][c] = state[x]
        c = c + 1
        if (x == 2 or x == 5 or x == 8):
            r = r + 1
            c = 0

def exploit(checkplayer):
    global state, available_spaces, board, player_X
    next_states = []
    best_state = []
    poss_states = []
    if (checkplayer == 1):
        symbol = 'X'
    else:
        symbol = 'O'

    for x in range(0,len(available_spaces)):
        for u in range(0,len(state)):
            if (state[u] == available_spaces[x]):
                poss_states = list(state)
                poss_states[u] = symbol
                next_states.append(poss_states)

    max_value = -9999999

    for item in next_states:
        if (Xstate_hash.get(str(item)) == None):
            Xstate_hash[str(item)] = 0
        if (Ostate_hash.get(str(item)) == None):
            Ostate_hash[str(item)] = 0

        if (player_X == 1):
            if (Xstate_hash.get(str(item))>max_value):
                max_value = Xstate_hash.get(str(item))
                best_state = list(item)
        else:
            if (Ostate_hash.get(str(item))>max_value):
                max_value = Ostate_hash.get(str(item))
                best_state = list(item)
    for l in range(0,9):
        if (state[l] != best_state[l]):
            t = state[l]
            state[l] = symbol
            available_spaces.remove(t)
    gamestates.append(str(state))

def check_row():
    global board
    for x in range(3):
        count_one = 0
        count_two = 0
        for y in range(3):
            if (board[x][y]=="X"):
                count_one+=1
            if (board[x][y]=="O"):
                count_two+=1
            if (count_one==3):
                #player X wins
                return 1
            if (count_two==3):
                #player O wins
                return 2
    return 0

def check_col():
    global board
    for y in range(3):
        count_one = 0
        count_two = 0
        for x in range(3):
            if (board[x][y]=="X"):
                count_one+=1
            if (board[x][y]=="O"):
                count_two+=1
            if (count_one==3):
                #player X wins
                return 1
            if (count_two==3):
                #player O wins
                return 2
    return 0

def check_diag():
    global board
    if (board[0][0]=="X" and board[1][1]=="X" and board[2][2]=="X"):
		#player X wins diag
        return 1
	
    if (board[0][0]=="O" and board[1][1]=="O" and board[2][2]=="O"):
		#player O wins diag
        return 2
	
    if (board[0][2]=="X" and board[1][1]=="X" and board[2][0]=="X"):
		#player X wins diag
        return 1
		
    if (board[0][2]=="O" and board[1][1]=="O" and board[2][0]=="O"):
		#playerO wins diag
        return 2
    return 0
		

def check_win():
	if (check_col() != 0):
		return check_col()
	elif (check_row()!=0):
		return check_row()
	elif (check_diag()!=0):
		return check_diag()
	elif (len(available_spaces)==0):
		return -1

	return 0

def reward(checkplayer):
    global learning_rate, decay

    if (checkplayer == 1):

        for x in reversed(range(len(gamestates))):
            if (x == (len(gamestates)-1)):
                Xstate_hash[gamestates[x]] += 1
                X_reward = Xstate_hash[gamestates[x]]
                Ostate_hash[gamestates[x]] -= 1
                O_reward = Ostate_hash[gamestates[x]]
            else:
                Xstate_hash[gamestates[x]] += learning_rate*(X_reward*decay - Xstate_hash[gamestates[x]])
                X_reward = Xstate_hash[gamestates[x]]
                Ostate_hash[gamestates[x]] += learning_rate*(O_reward*decay - Ostate_hash[gamestates[x]])
                O_reward = Ostate_hash[gamestates[x]]
    else:
        for x in reversed(range(len(gamestates))):
            if (x == (len(gamestates)-1)):
                Xstate_hash[gamestates[x]] -= 1
                X_reward = Xstate_hash[gamestates[x]]
                Ostate_hash[gamestates[x]] += 1
                O_reward = Ostate_hash[gamestates[x]]
            else:
                Xstate_hash[gamestates[x]] += learning_rate*(X_reward*decay - Xstate_hash[gamestates[x]])
                X_reward = Xstate_hash[gamestates[x]]
                Ostate_hash[gamestates[x]] += learning_rate*(O_reward*decay - Ostate_hash[gamestates[x]])
                O_reward = Ostate_hash[gamestates[x]]


def reward_tie():
    for x in range(0,len(gamestates)):
        Xstate_hash[gamestates[x]] += 0
        Ostate_hash[gamestates[x]] += 0

def reset():
    #this function resets the stage for a new game
    global gamestates, available_spaces, board, state

    available_spaces = ["1", "2", "3", "4", "5","6","7","8","9"]
    state = ["1", "2", "3", "4", "5","6","7","8","9"]
    gamestates = [str(state)]
    board = [["1","2","3"],["4","5","6"],["7","8","9"]]

def train(number):
    #this function trains both agents simultaneous for as many games as the input
    global Xwins, Owins, ties, player_X

    for x in range(number):
        player_X = 1
        reset()
        update_board()
        while(check_win()==0):
            y = random.uniform(0,1)
            if (y < float(.3)):
                explore(player_X)
            else:
                exploit(player_X)
            update_board()
            if (check_win() == 1):
                #X won
                Xwins = Xwins + 1
                reward(1)
            elif (check_win() == 2):
                #O wins
                Owins = Owins + 1
                reward(2)
            elif (check_win() == -1):
                #tie
                ties = ties + 1
                reward_tie()

            changesides()

def train_against_random(number,player):
    #this function trains an agent against a random opponent, the player is the agent to be trained
    #the agent is trained for as many games as the number input 
    global Xwins, Owins, ties, player_X

    if (player != "X" and player != "O"):
        while (player != "X" and player != "O"):
            z = input("wrong input to train, type X or O")
            player = z

    for x in range(number):
        player_X = 1
        reset()
        update_board()
        while(check_win()==0):
            if (player_X == 0):
                if (player == "O"):
                    y = random.uniform(0,1)
                    if (y < float(.3)):
                        explore(player_X)
                    else:
                        exploit(player_X)
                else:
                    explore(player_X)
            else:
                if (player == "X"):
                    y = random.uniform(0,1)
                    if (y < float(.3)):
                        explore(player_X)
                    else:
                        exploit(player_X)
                else:
                    explore(player_X)
            update_board()
            if (check_win() == 1):
                #X won
                Xwins = Xwins + 1
                reward(1)
            elif (check_win() == 2):
                #O won
                Owins = Owins + 1
                reward(2)
            elif (check_win() == -1):
                #tie
                ties = ties + 1
                reward_tie()

            changesides()


#--------------------------------------------------------------------------------- 


train(200000)
train_against_random(200000,"O")

Xwins = 0
Owins = 0
ties = 0
for x in range(1000):
    #z = input()
    player_X = 1
    reset()
    makeboard()
    while(check_win()==0):
        z = input()

        if (player_X == 0):
            exploit(player_X)
        else:
            explore(player_X)
        makeboard()
        if (check_win() == 1):
            #X won
            Xwins = Xwins + 1
            reward(1)
        elif (check_win() == 2):
            Owins = Owins + 1
            #O won
            reward(2)
        elif (check_win() == -1):
            #tie
            ties = ties + 1
            reward_tie()

        changesides()


