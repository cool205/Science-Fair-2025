#Code for Simulating Games

import chess
from stockfish import Stockfish
import os
import json
import time
import multiprocessing
import datetime
import ast

os.system('cls')
time.sleep(2)

# Initialize Stockfish
stockfish_path = r"C:\Users\Wilso\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"
stockfish = Stockfish(stockfish_path)




#with open('RawDataTransfer.txt', 'r') as file:
    #gameResultsRawData = ast.literal_eval(file.read())

gameResultsRawData = []

#openings
openings = [
    ["e2e4", "g8f6"], #Alekhine's Defense
    ["d2d4", "g8f6", "c2c4", "c7c5", "d4d5", "b7b5"], #Benko Gambit
    ["d2d4", "g8f6", "c2c4", "c7c5"], #Benoni Defense
    ["d2d4", "g8f6", "c2c4", "e7e6", "g1f3", "f8b4"], #Bogo-Indian Defense
    ["d2d4", "g8f6", "c2c4", "e7e5"], #Budapest Gambit
    ["e2e4", "c7c6", "d2d4", "d7d5"], #Caro-Kann Defense
    ["d2d4", "g8f6", "c2c4", "e7e6", "g2g3"], #Catalan Opening
    ["e2e4", "e7e5", "d2d4", "e5d4","c2c3"], #Danish Gambit
    ["e2e4", "c7c5", "b1c3", "b8c6"], #Closed Sicilian
    ["d2d4", "f7f5"], #Dutch Defense
    ["c2c4"], #English Opening
    ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4", "f8c5", "b2b4"], #Evan's Gambit
    ["f2f4", "e7e5"], #From's Gambit
    ["e2e4", "e7e5", "g1f3", "b8c6", "b1c3", "g8f6"], #Four Knights Game
    ["e2e4", "e7e6", "d2d4", "d7d5", "e4e5"], #French Defense: Advanced Variation
    ["e2e4", "e7e6", "b1c3"], #French Defense with Nc3   
    ["d2d4", "g8f6", "c2c4", "g7g6", "b1c3", "d7d5"], #Grunfeld Defense
    ["d2d4", "g8f6", "c2c4", "b8c6"], #Black Knights' Tango
    ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4"], #Italian Game
    ["e2e4", "e7e5", "f2f4"], #King's Gambit
    ["g1f3", "d7d5", "g2g3"], #King's Indian Attack
    ["d2d4", "g8f6", "c2c4", "g7g6"], #Kings Indian Defense
    ["d2d4", "g8f6"], #Reti Opening
    ["d2d4", "g8f6", "c2c4", "e7e6", "b1c3", "f8b4"], #Nimzo-Indian Defense
    ["d2d4", "g8f6", "c2c4", "d7d6"], #Old Indian Defense
    ["e2e4", "e7e5", "g1f3", "g8f6"], #Petrov's Defense
    ["e2e4", "d7d6"], #Pirc Defense
    ["e2e4", "g7g6"], #Modern Defense
    ["d2d4", "d7d5", "c2c4"], #Queen's Gambit
    ["d2d4", "g8f6", "c2c4", "e2e4", "g1f3", "b7b6"], #Queen's Indian Defense
    ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5", "g8f6"], #Berlin Defense
    ["e2e4", "d7d5"], #Scandanavian Defense
    ["d2d4", "d7d5", "c2c4", "e7e6", "b1c3", "g8f6", "g1f3", "c7c6"], #Semi-Slav Defense
    ["e2e4", "c7c5", "c2c3"], #Alapin Sicilian
    ["e2e4", "e7e5", "g1f3", "b8c6", "d2d4"], #Scotch Game
    ["e2e4", "c7c5", "g1f3", "d7d6", "d2d4", "c5d4", "f3d4", "g8f6", "b1c3", "g7g6"], #Sicilian Dragon
    ["e2e4", "c7c5", "g1f3", "d7d6", "d2d4", "c5d4", "f3d4", "g8f6", "b1c3", "a7a6"], #Sicilian Najdorf
    ["e2e4", "c7c5", "g1f3", "b8c6", "f1b5"], #Sicilian Rossolimo
    ["d2d4", "d7d5", "c2c4", "c7c6"], #Slav Defense
    ["e2e4", "e7e5", "b1c3"], #Vienna Game
    ["e2e4", "e7e5", "f1c4"], #Bishop's Opening
    ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4", "g8f6"], #Two Knights Defense
    ["d2d4", "g8f6", "c1g5"], #Tromposky Attack
    ["d2d4", "g8f6", "g1f3", "e7e6", "c1g5"], #Torre Attack
    ["b2b3", "e2e4"], #Nimzowitsch-Larsen Attack
    ["e2e3", "e7e5"], #Van't Krujis Opening
    ["d2d3", "d7d5"], #Mieses Opening
    ["c2c3", "e7e5", "d2d4"], #Saragossa Opening
    ["g2g4", "d7d5"], #Grob Opening
    ["e2e4", "c7c6", "f1c4"] #Hillbilly Attack
]



#Set up variables
moves_list = []
numOfMoves = 0
gameOver = False
board = chess.Board()


def playGame(depth, opening):
    current_datetime = datetime.datetime.now()
    if openings.index(opening)+1 > 9:
        if depth+1 > 9:
            print(f"Starting a game with  depth={depth+1}   opening={openings.index(opening)+1}   at {current_datetime.hour}:{current_datetime.minute} {current_datetime.month}/{current_datetime.day}")
        else:
            print(f"Starting a game with  depth={depth+1}    opening={openings.index(opening)+1}   at {current_datetime.hour}:{current_datetime.minute} {current_datetime.month}/{current_datetime.day}")
   
    else:
        if depth+1 > 9:
            print(f"Starting a game with  depth={depth+1}   opening={openings.index(opening)+1}    at {current_datetime.hour}:{current_datetime.minute} {current_datetime.month}/{current_datetime.day}")
   
        else:
            print(f"Starting a game with  depth={depth+1}    opening={openings.index(opening)+1}    at {current_datetime.hour}:{current_datetime.minute} {current_datetime.month}/{current_datetime.day}")
     
     
   # New Game
    stockfish.set_depth(depth + 1)  # +1 is default
    gameOver = False
    moves_list = []
    numOfMoves = 0
    board = chess.Board()

    # Insert openings
    for move in opening:
        board.push(chess.Move.from_uci(move))
        moves_list.append(str(move))
        numOfMoves += 1

    # Simulate the rest of the game
    while not gameOver:
        # Stockfish best move
        stockfish.set_fen_position(board.fen())
        best_move_in_position = chess.Move.from_uci(stockfish.get_best_move())
        if best_move_in_position in board.legal_moves:
            board.push(best_move_in_position)
            moves_list.append(str(best_move_in_position))
            numOfMoves += 1
        else:
            print("Not legal")

        # Check for game-ending conditions
        if (board.is_checkmate() or board.is_stalemate() or
                board.is_insufficient_material() or board.is_repetition() or
                board.is_fifty_moves()):
            gameOver = True
    current_datetime = datetime.datetime.now()
    if openings.index(opening)+1 > 9:
        if depth+1 > 9:
            print(f"Finished a game with  depth={depth+1}   opening={openings.index(opening)+1}   at {current_datetime.hour}:{current_datetime.minute} {current_datetime.month}/{current_datetime.day}")
        else:
            print(f"Finished a game with  depth={depth+1}    opening={openings.index(opening)+1}   at {current_datetime.hour}:{current_datetime.minute} {current_datetime.month}/{current_datetime.day}")
   
    else:
        if depth+1 > 9:
            print(f"Finished a game with  depth={depth+1}   opening={openings.index(opening)+1}    at {current_datetime.hour}:{current_datetime.minute} {current_datetime.month}/{current_datetime.day}")
   
        else:
            print(f"Finished a game with  depth={depth+1}    opening={openings.index(opening)+1}    at {current_datetime.hour}:{current_datetime.minute} {current_datetime.month}/{current_datetime.day}")
   
    return moves_list



def run_simulation_parallel(openings, depth):
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        tasks = []

        for opening in openings:
            time.sleep(0.5)
            tasks.append((depth, opening))
            print(f"Task added: depth={depth+1}, opening={opening}")
        # Use starmap to distribute tasks
        print("Done Adding " + str(len(tasks))+ " Tasks")
        time.sleep(1)
        os.system('cls')
        print("Starting parallel tasks...")
        time.sleep(1)
        os.system('cls')
        results = pool.starmap(playGame, tasks)
    os.system('cls')
    return results






def save_results():
    with open('RawDataTransfer.txt', 'w') as file:
        file.write(str(gameResultsRawData))


if __name__ == '__main__':
    # Run simulations for depths 1 to 50
    
    for depthPlay in range(50):
        results = run_simulation_parallel(openings, depthPlay)
        gameResultsRawData.append(results)
        save_results()
    # Save the results
    print("Done Simulating Games")
