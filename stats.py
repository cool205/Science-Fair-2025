#Statistical Analysis Code
import chess
import ast
import os
import math
import matplotlib.pyplot as plt

os.system('cls')
print("Opening Files")
#read from file
with open('1-46.txt','r') as file:
    gameResultsStats = ast.literal_eval(file.read())

print("Completed")
stats = []

#Resimulate all the games

for n in range(len(gameResultsStats)):#depths
    print(n)
    stats_depth = []
    for l in range(len(gameResultsStats[n])):#games
        board = chess.Board()
        numOfMoves = 0
        stats_game = []
        stats_move = []
        for i in range(len(gameResultsStats[n][l])):#move
            board.push(chess.Move.from_uci(gameResultsStats[n][l][i]))
            numOfMoves += 1
            stats_move.append(len(list(board.legal_moves)))
        stats_game.append(stats_move)
        if board.is_checkmate():
            if board.turn: #true = white, false = black, reverse
                stats_game.append("B")
            else:
                stats_game.append("W")
        elif board.is_stalemate():
            stats_game.append("S")
        elif board.is_fifty_moves():
            stats_game.append("F")
        elif board.is_repetition():
            stats_game.append("R")
        elif board.is_insufficient_material():
            stats_game.append("I")
        else:
            stats_game.append("N")
        stats_game.append(math.ceil((numOfMoves)/2))


        stats_depth.append(stats_game)
    stats.append(stats_depth)



#Analyze Data



#find average number of moves per depth

print("Analyzing Average Moves:")
fig1 = plt.figure("Figure 1")
average_moves = []
for i in range(len(stats)):
    average = 0
    for n in range(50): #number of games
        average += stats[i][n][2]
        if i == 36 and n==0:
            plt.plot(i+1, stats[i][n][2], color = "brown", marker = 'o')
        else:
            plt.plot(i+1, stats[i][n][2], color = "r", marker = 'o')
    average_moves.append(round(average/50))

depths = list(range(1, len(average_moves)+1))


plt.plot(depths, average_moves, marker = 'o', linestyle = "-", color = "b")
plt.title('Average Number of Moves per Depth')
plt.xlabel('Depth')
plt.ylabel('Average Number of Moves')
plt.xticks(depths)
plt.grid(True)


print("Analyzing Average Moves Completed")
print("Analyzing Average Possible Moves:")




#average possible moves
fig2 = plt.figure("Figure 2")
average_possible_moves = []
for i in range(len(stats)):
    averagePossibleMoves = []
    for n in range(50): #number of games
        averagePossibleMovesInGame = 0
        for x in range(len(stats[i][n][0])):
            averagePossibleMovesInGame += stats[i][n][0][x]
        averagePossibleMoves.append(averagePossibleMovesInGame/len(stats[i][n][0]))
        plt.plot(i+1, averagePossibleMovesInGame/len(stats[i][n][0]), color = "r", marker = 'o')
    count = 0
    for w in range(len(averagePossibleMoves)):
        count += averagePossibleMoves[w]
    average_possible_moves.append(count/len(averagePossibleMoves))

depths = list(range(1, len(average_possible_moves)+1))
plt.plot(depths, average_possible_moves, marker = 'o', linestyle = "-", color = "b")
plt.title('Average Number of Possible Moves per Depth')
plt.xlabel('Depth')
plt.ylabel('Average Number of Possible Moves')
plt.xticks(depths)
plt.grid(True)

print("Analyzing Average Possible Moves Completed")





# Analyze Game Ending Conditions per Depth
print("Analyzing Game Ending Conditions:")
fig3 = plt.figure("Figure 3")
game_ending_conditions = {
    "B": [],  # Black Wins
    "W": [],  # White Wins
    "D": [],
    "N": []
}

for i in range(len(stats)):  # depth
    blackWins = 0
    whiteWins = 0
    draws = 0
    none = 0
    

    for w in range(len(stats[i])):
        condition = stats[i][w][1] 

        if condition == "B":
            blackWins += 1
        elif condition == "W":
            whiteWins += 1
        elif condition == "S":
            draws += 1
        elif condition == "F":
            draws += 1
        elif condition == "R":
            draws += 1
        elif condition == "I":
            draws += 1
        else:
            none += 1
            plt.plot(i+1, 1, marker='o', color='brown', label="None")

    game_ending_conditions["B"].append(blackWins)
    game_ending_conditions["W"].append(whiteWins)
    game_ending_conditions["D"].append(draws)
    game_ending_conditions["N"].append(none)

# Now, plot these conditions per depth
depths = list(range(1, len(stats) + 1))

plt.title('Game Ending Conditions per Depth')
plt.xlabel('Depth')
plt.ylabel('Count of Game Ending Conditions')
plt.xticks(depths)
plt.grid(True)

plt.plot(depths, game_ending_conditions["B"], marker='o', linestyle='-', color='red', label="Black Wins")
plt.plot(depths, game_ending_conditions["W"], marker='o', linestyle='-', color='blue', label="White Wins")
plt.plot(depths, game_ending_conditions["D"], marker='o', linestyle='-', color='green', label="Draws")


plt.legend()

print("Analyzing Game Ending Conditions Completed")






#Types of Draws

print("Analyzing Draw Conditions:")

drawConditions = {
    "S": [],
    "F": [], 
    "R": [],
    "I": []
}

for i in range(len(stats)):  # depth
    repetition = 0
    stalemate = 0
    in_material = 0
    fifty_move = 0
    amountOfDraws = 0
    

    for w in range(len(stats[i])):
        condition = stats[i][w][1] 
        if condition == "S":
            stalemate += 1
            amountOfDraws += 1
        elif condition == "F":
            fifty_move += 1
            amountOfDraws += 1
        elif condition == "R":
            repetition += 1
            amountOfDraws += 1
        elif condition == "I":
            in_material += 1
            amountOfDraws += 1

    drawConditions["S"].append(stalemate/amountOfDraws)
    drawConditions["I"].append(in_material/amountOfDraws)
    drawConditions["R"].append(repetition/amountOfDraws)
    drawConditions["F"].append(fifty_move/amountOfDraws)

# Now, plot these conditions per depth
depths = list(range(1, len(stats) + 1))

fig4 = plt.figure("Figure 4")
plt.title('Draw Types')
plt.xlabel('Depth')
plt.ylabel('Draws')
plt.xticks(depths)
plt.grid(True)

plt.plot(depths, drawConditions["S"], marker='o', linestyle='-', color='red', label="Stalemate")
plt.plot(depths, drawConditions["I"], marker='o', linestyle='-', color='blue', label="Insufficient Material")
plt.plot(depths, drawConditions["R"], marker='o', linestyle='-', color='green', label="Repetition")
plt.plot(depths, drawConditions["F"], marker='o', linestyle='-', color='purple', label="Fifty-Moves")


plt.legend()

print("Analyzing Draws Conditions Completed")

plt.show()