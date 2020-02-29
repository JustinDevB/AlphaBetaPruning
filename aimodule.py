#!/usr/bin/env python3

import sys
from random import choice,shuffle

count = 0

NOTDONE = 99

winners = ( (0,1,2), (3,4,5), (6,7,8), (0,3,6),
            (1,4,7), (2,5,8), (0,4,8), (2,4,6))

squareorder = [4, 0, 2, 6, 8, 1, 3, 5, 7]
squarevalue = [2, 1, 2, 1, 3, 1, 2, 1, 2]

# pattern means row, column, diagonal


def boardvalue(board, who):
    total = 0
#
# does 'who' have 3-in-a-row ?
#
    for pat in winners:
        tmp = {board[x] for x in pat}
        if len(tmp) == 1 and who in tmp:
            total += who * 1000
#
# does -who have an open 2-in-a-row
#
    for pat in winners:
        tmp = [board[x] for x in pat]
        if who not in tmp:
            if sum([x == -who for x in tmp]) == 2:
                total += -who * 100
#
# points for occupying squares
#
    total += sum([squarevalue[x] * board[x] for x in board])
    return total

# alpha-beta pruning version

def boardscore(board, who):
    for pat in winners:
        tmp = {board[x] for x in pat}
        if len(tmp) == 1 and who in tmp:
            return who
    if 0 not in board:
        return 0
    return NOTDONE

def alpha(board):     # considering X's moves
    global count

    count += 1
    movelist = [i for i in range(9) if board[i] == 0]
    shuffle(movelist)
    bestmove, bestval = -1, -2
    for move in movelist:
        board[move] = 1
        val = boardscore(board, 1)
        if val == NOTDONE:
            _ , val = beta(board)
        if val > bestval:
            bestmove, bestval = move, val
        board[move] = 0
    return bestmove, bestval

def beta(board):     # considering O's moves
    movelist = [i for i in range(9) if board[i] == 0]
    shuffle(movelist)
    bestmove, bestval = -1,  2
    for move in movelist:
        board[move] = -1
        val = boardscore(board, -1)
        if val == NOTDONE:
            _ , val = alpha(board)
        if val < bestval:
            bestmove, bestval = move, val
        board[move] = 0
    return bestmove, bestval

def alphabeta(board, who):
    global count

    if all([x == 0 for x in board]):
        return choice(range(9))
    count = 0
    bcopy = [-1 if x == 2 else x for x in board]  # copy board, change 2's to -1's
    if who == 1:
        bestmove, bestval = alpha(bcopy)
    else:
        bestmove, bestval = beta(bcopy)
    return bestmove

if __name__ == "__main__":

    board = [1, 1, 0, -1, -1, 0, 0, 0, 0]
    print(phase4(board,1))

