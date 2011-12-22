#!/bin/sh
#echo DEFANGED.2800
#exit
#!/usr/bin/env python

import os

#The following function is used to output the current board(after move)
#and the parent board (before move), if the parent board is provided
def BoardPrint(board,move=[],name="====== The current board is: ======",parent_board = None,num =0 ):
    if parent_board:
        #print "The parent board is:", name
        print "The parent board(",num - 1,") is:", "====== The current board(",num,")is: ======"
        if move:
            print "move = ",move
        for i in [7,6,5,4,3,2,1,0]:
            print i,":",
            for j in range(8):
                print parent_board[i][j],
            print "\t     |\t  ",i,":",
            for j in range(8):
                print board[i][j],
            print
        print "   ",0,1,2,3,4,5,6,7,"\t     |\t     ",0,1,2,3,4,5,6,7
    else:
        #print name
        print "====== The current board(",num,")is (after move): ======"
        if move:
            print "move = ",move
        for i in [7,6,5,4,3,2,1,0]:
            print i,":",
            for j in range(8):
                print board[i][j],
            print
        print "   ",0,1,2,3,4,5,6,7
    print "";

def BoardCopy(board):
    new_board = [[]]*8
    for i in range(8):
        new_board[i] = [] + board[i]
    return new_board

#========================================================
def Parse_Move(move):
    print type(move)
    return True

def legal(move,state,player):
    if version == 0:
        return True
    else:
        if not move:
            return True
        else:
            new_state = doit(move,state)
            if new_state in successors(state,player):
                return True
            else:
                return 0

def doit(move,state):
    new_state = BoardCopy(state)
    #print "player",player
    #Move one step
    if len(move) == 2 and abs(move[1][0] - move[0][0]) == 1:         
        new_state[move[0][0]][move[0][1]] = '.'
        if state[move[0][0]][move[0][1]] == 'b' and move[1][0] == 7:
            new_state[move[1][0]][move[1][1]] = 'B'
        elif state[move[0][0]][move[0][1]] == 'r' and move[1][0] == 0:
            new_state[move[1][0]][move[1][1]] = 'R'
        else:
            new_state[move[1][0]][move[1][1]] = state[move[0][0]][move[0][1]]
    #Jump
    else:
        step = 0;
        new_state[move[0][0]][move[0][1]] = '.'
        while step < len(move)-1:
            new_state[(move[step][0]+ move[step+1][0])/2][(move[step][1]+ move[step+1][1])/2] = '.'                        
            step = step+1
        if state[move[0][0]][move[0][1]] == 'b' and move[step][0] == 7:
            new_state[move[step][0]][move[step][1]] = 'B'
        elif state[move[0][0]][move[0][1]] == 'r' and move[step][0] == 0:
            new_state[move[step][0]][move[step][1]] = 'R'
        else:
            new_state[move[step][0]][move[step][1]] = state[move[0][0]][move[0][1]]
    return new_state

        
#======================================================================
Initial_Board = [ ['b','.','b','.','b','.','b','.'],\
                  ['.','b','.','b','.','b','.','b'],\
                  ['b','.','b','.','b','.','b','.'],\
                  ['.','.','.','.','.','.','.','.'],\
                  ['.','.','.','.','.','.','.','.'],\
                  ['.','r','.','r','.','r','.','r'],\
                  ['r','.','r','.','r','.','r','.'],\
                  ['.','r','.','r','.','r','.','r'] \
                ]

Test_Board1 =   [ ['.','.','.','.','.','.','.','.'],\
                  ['.','.','.','.','.','.','.','.'],\
                  ['.','.','.','.','.','.','.','.'],\
                  ['.','.','.','B','.','.','.','R'],\
                  ['.','.','.','.','.','.','.','.'],\
                  ['.','.','.','.','.','R','.','.'],\
                  ['.','.','.','.','.','.','.','.'],\
                  ['.','.','.','.','.','.','.','.'] \
                ]

Test_Board2 = [ ['.','.','.','.','.','.','b','.'],\
    ['.','.','.','b','.','b','.','b'],\
    ['b','.','.','.','.','.','b','.'],\
    ['.','.','.','.','.','.','.','.'],\
    ['.','.','.','.','b','.','.','.'],\
    ['.','.','.','.','.','B','.','.'],\
    ['b','.','.','.','.','.','.','.'],\
    ['.','.','.','.','.','.','.','r'],\
    ]

Test_Board3 = [ ['.','.','.','.','.','.','.','.'],\
    ['.','.','.','.','.','.','.','.'],\
    ['.','.','B','.','.','.','b','.'],\
    ['.','.','.','b','.','B','.','.'],\
    ['.','.','.','.','R','.','.','.'],\
    ['.','.','.','b','.','B','.','.'],\
    ['.','.','b','.','.','.','b','.'],\
    ['.','.','.','.','.','.','.','.'],\
    ]


def IsBoardLegal(test_board):
    legal = 1
    red_num = 0
    black_num = 0
    
    for i in range(8):
        for j in range(8):
            if (i+j) %2 == 0:
                if test_board[i][j] == 'r' or test_board[i][j] == 'R':
                    red_num += 1
                elif test_board[i][j] == 'b' or test_board[i][j] == 'B':
                    black_num += 1
                elif test_board[i][j] != '.':
                    print "Position (",i,j,") is wrong and it should be one of '.', 'b', 'B', 'r' or 'R' "
                    legal = 0
            else:
                if test_board[i][j] != '.':
                    print "Position (",i,j,") is wrong and it should be '.'"
                    legal = 0

    if red_num > 12:
        print "The number of red pieces should less than or equal to 12, now it is", red_num
        legal = 0

    if black_num > 12:
        print "The number of black pieces should less than or equal to 12, now it is", black_num
        legal = 0

    return legal        
    

def play(file_A, file_B,start_state = Initial_Board):
    exec("import " + file_A + " as Aplayer")
    exec("import " + file_B + " as Bplayer")

    A = Aplayer.GameEngine('r')
    B = Bplayer.GameEngine('b')
    
    currPlayer = A
    state = start_state    

    previous_states_list = []
    draw_flag = 0
    board_num = 0
        
    BoardPrint(state,name="====== The initial board (0) is: ======")
    
    while True:
        print "It is ", currPlayer ,"'s turn"
        move = currPlayer.nextMove(state)

        if not move:
            break

        #Check draw
        if currPlayer == A:
            player_name = 'r'            
        else:
            player_name = 'b'
            
        state_with_player = [state, player_name]
        
        if state_with_player in previous_states_list:
            ind = previous_states_list.index(state_with_player)
            ind = board_num - len(previous_states_list) + ind ;
            print "The current board is the same as the", ind, "th board"
            print "You might need to create a better heutistic function"
            draw_flag = 1 
            break
        
        previous_states_list.append(state_with_player);
        if(len(previous_states_list) > 100):
            previous_states_list = previous_states_list[1:]

        print "The move is : ",move
        parent = BoardCopy(state);
        if legal(move, state,currPlayer.str):
            state = doit(move,state)

        board_num = board_num + 1
        #BoardPrint(state,parent_board = parent, num = board_num)
        BoardPrint(state,num = board_num)

        if currPlayer == A:
            currPlayer = B
        else:
            currPlayer = A

    print "Game Over"
    if draw_flag:
        print "It is a DRAW"
    elif currPlayer == A:    
        print "The Winner is:",file_B, 'b'
    else:
        print "The Winner is:",file_A, 'r'



#(1)Computer vs Computer model:
#if version = 0, we will not check the correctness of a move
version = 0
play("Checkers","Checkers")
#play("Checkers","default")
#play("default","Checkers")
#play("Checkers","???Checkers")
#play("???Checkers","Checkers")

#play("Checkers","Checkers",start_state = Test_Board1)
#play("Checkers","Checkers",start_state = Test_Board2)
#play("Checkers","Checkers",start_state = Test_Board3)

#if IsBoardLegal(Test_Board1):
#    print "The board is legal"
#else:
#    BoardPrint(Test_Board1)
#    print "The board is not legal"
    
