from __future__ import nested_scopes
import string
import random


max_depth = 6;
#======================== Class GameEngine =======================================
class GameEngine:
    def __init__(self, str_name):
        self.str = str_name

    def __str__(self):
        return self.str

#The return value should be a move that is denoted by a list
    def nextMove(self,state):
        global PLAYER
        curNode = Node(Board(state))
        PLAYER = self.str
        result = maxv(curNode,Thresh(-2000),Thresh(2000),0,"",self.str)
        return result.bestSucc.state.move

#==================== Class Node ============================================
class Node:

   def __init__ (self,state,parent=None,depth=0,gval=0,hval=None):
      self.state = state
      self.parent = parent
      self.depth = depth
      self.gval = gval
      self.hval = hval

   def printNode(self):
      print "state: ", self.state, " Parent: ", self.parent.state, 
      print " Gval=",self.gval," Hval=",self.hval
   
   def printPathToNode(self):
      if self:
         self.printNode()
         if self.parent:
            printPathToNode(self.parent)

#================== Class Thresh =======================================
class Thresh:

   def __init__(self,initVal,node=None):
      self.val = initVal
      self.bestSucc = node

   def __repr__(self): 
      return str(self.val) 

#============== A New Class: Board ============================================
# This class is used to represent board and move
# Class Members:
# board : a list of lists that represents the 8*8 board
# move : is also a list, e.g move = [(1,1),(3,3),(5,5)]


class Board:
    
    def __init__(self,board,move=[]):
        self.board = board
        self.move = move
        self.priorities = {};

#This function outputs the current Board
    def PrintBoard(self,name="====== The current board is: =========",parent = None ):
        if parent:
            print "Move = ",self.move
            print "The Parent board is:", name            
            for i in [7,6,5,4,3,2,1,0]:
                print i,":",
                for j in range(8):
                    print parent.board[i][j],
                print "\t|\t",i,":",
                for j in range(8):
                    print self.board[i][j],
                print
            print "   ",0,1,2,3,4,5,6,7,"\t|\t   ",0,1,2,3,4,5,6,7
        else:
            print name
            print "move = ",self.move
            for i in [7,6,5,4,3,2,1,0]:
                print i,":",
                for j in range(8):
                    print self.board[i][j],
                print
            print "   ",0,1,2,3,4,5,6,7

#This function has not been finished (To be continued ???, or just use PrintBoard)
    def __str__(self):
        return "Board"
#=======================================================
#Please only modify code in the following two functions
#=======================================================
'''
a bunch of helper functions for my heuristic
'''
#see which player we're dealing with and return the direction they move in.
#This is hardcoded to work with boards where red starts on top and black
#starts at the bottom
def playerDirection(piece):
  if 'r' in PlayerDic[piece]:
    direction = -1;
  elif 'b' in PlayerDic[piece]:
    direction = 1;

  return direction;

#checks if the x,y coordinate is within the bounds of the board
def validPosition(pos=()):
  x, y = pos;
  return (x >= 0 and x < 8) and (y >= 0 and y < 8);

#checks if the x,y coordinate is an empty square
def emptyPosition(board, pos = ()):
  x, y = pos;
  retval = False;
  if validPosition(pos):
    retval = board[x][y] == ".";
  return retval;

#checks if the pos is on the left or right edge of the board
def sidePosition(pos = ()):
  x, y = pos;
  retval = False;
  if validPosition(pos):
    retval = (y == 0) or (y == 7);
  return retval;

#checks if a piece in it's homerow
def homeRow(piece, x):
  retval = False;
  if piece == 'r' and x == 7:
    retval = True;
  elif piece == 'b' and x == 0:
    retval = True;

  return retval;

#jumpable means:
#-the finishing position is empty and valid
#-the intermediate position contains an opponent's piece

#check if the piece can jump left from pos
def jumpableLeft(board, pos, piece, direction):
  retval = False;
  x, y = pos;
  if validPosition((x + direction, y - 1)) and\
    board[x + direction][y - 1] in OppDic[piece] and\
    emptyPosition(board, (x + 2*direction, y - 2)):
    retval = True;
  return retval;

#check if the piece can jump right from pos
def jumpableRight(board, pos, piece, direction):
  retval = False;
  x, y = pos;
  if validPosition((x + direction, y + 1)) and\
    board[x + direction][y + 1] in OppDic[piece] and\
    emptyPosition(board, (x + 2*direction, y + 2)):
    retval = True;
  return retval;

'''
  offensiveValue heuristic functions
'''
#the offensive value of a piece is based on the number of jumps a piece can
#perform given its current position (it is a recursive check to detect jump
#chains) see report for more details
def offensiveValue(board, pos, piece):
  direction = playerDirection(piece);
  return recursiveJump(board, pos, piece, direction, []);

#look for chains of jumps for a given piece at pos on the board. see report
#for more details.
def recursiveJump(board, pos, piece, direction, jump_list):
  x, y = pos;
  is_king = piece in ['R','B'];

  x2 = x + direction;
  y2 = y + 1;
  if validPosition((x2, y2)) and not emptyPosition(board, (x2, y2)) and\
    not jumpableLeft(board, (x2, y2), board[x2][y2], -1 * direction) and\
    jumpableRight(board, pos, piece, direction):

    jumped = (x2, y2);
    if jumped not in jump_list:
      jump_list.append(jumped);
      landed = (x + 2*direction, y + 2);
      return calculateJump(board, landed, piece, direction, jump_list);

  y2 = y - 1;
  if validPosition((x2, y2)) and not emptyPosition(board, (x2, y2)) and\
    not jumpableRight(board, (x2, y2), board[x2][y2], -1 * direction) and\
    jumpableLeft(board, pos, piece, direction):

    jumped = (x2, y2);
    if jumped not in jump_list:
      jump_list.append(jumped);
      landed = (x + 2*direction, y - 2);
      return calculateJump(board, landed, piece, direction, jump_list);
  
  #also check opposite direction if the piece is kinged
  if is_king:
    direction *= -1;
    x2 = x + direction;
    y2 = y + 1;
    if validPosition((x2, y2)) and not emptyPosition(board, (x2, y2)) and\
      not jumpableLeft(board, (x2, y2), board[x2][y2], -1 * direction) and\
      jumpableRight(board, pos, piece, direction):
      jumped = (x + direction, y + 1);
      if jumped not in jump_list:
        jump_list.append(jumped);
        landed = (x + 2*direction, y + 2);
        return calculateJump(board, landed, piece, direction, jump_list);

    y2 = y - 1;
    if validPosition((x2, y2)) and not emptyPosition(board, (x2, y2)) and\
      not jumpableRight(board, (x2, y2), board[x2][y2], -1 * direction) and\
      jumpableLeft(board, pos, piece, direction):
      jumped = (x + direction, y - 1);
      if jumped not in jump_list:
        jump_list.append(jumped);
        landed = (x + 2*direction, y - 2);
        return calculateJump(board, landed, piece, direction, jump_list);
    
  #done recursively checking this branch
  if len(jump_list) > 0:
    jump_list.pop();
  return 0;

def calculateJump(board, pos, piece, direction, jump_list):
  prize = 20 / len(jump_list);
  jumped = jump_list[-1];
  #jumping a king is worth a lot
  if board[jumped[0]][jumped[1]] in ['R', 'B']:
    prize = 40;
  return prize + recursiveJump(board, pos, piece, direction, jump_list); 

#the defensive value is based on two things, how well defended the piece at
#pos is and the number of pieces the piece at pos is defending. see report
#for details
def defensiveValue(board, pos, piece):
  x, y = pos;
  value = 0;
  direction = playerDirection(piece);
  #check if the piece is defending any other piece
  if validPosition((x + direction, y - 1)) and\
    board[x + direction][y - 1] in PlayerDic[piece]:
    value += 10;
  if validPosition((x + direction, y + 1)) and\
    board[x + direction][y + 1] in PlayerDic[piece]:
    value += 10;
  
  #check how well defended this piece is. if the piece is on the left or right
  #edge it doesn't another piece defending it. being on the edge is worth 
  #more than being defended by 2 pieces since it frees up 2 pieces to do 
  #something else.
  if sidePosition(pos):
    value += 20;

  else:
    if validPosition((x - direction, y - 1)) and\
      board[x - direction][y - 1] in ['r', 'b']:
      value += 10;
    if validPosition((x - direction, y - 1)) and\
      board[x - direction][y + 1] in ['r', 'b']:
      value += 10;
    
    #check if the piece can be jumped from any direction
    for delta_x in [-1, 1]:
      for delta_y in [-1, 1]:
        x2 = x + delta_x;
        y2 = y + delta_y;
        if not (validPosition((x2, y2)) and not emptyPosition(board, (x2, y2)) and\
          jumpableRight(board, (x2, y2), board[x2][y2], -1 * direction)):
          value += 10;  
  return value;

#the mobility value is based on the number of valid open positions the piece
#at pos can move to. see report for details.
def mobilityValue(board, pos, piece):
  value = 0;
  direction = playerDirection(piece);

  #determine if the piece can move/jump forward
  value += mobilityCalculator(board, pos, piece, direction);

  #if the piece is kinged then the opposite direction has to be checked	
  if piece in ['R', 'B']:
    value += mobilityCalculator(board, pos, piece, direction * -1);

  return value;

#calculates the mobililty value of a position, called by mobilityValue
def mobilityCalculator(board, pos, piece, direction):
  x, y = pos;
  value = 0;
  #check for empty positions infront of the piece
  if emptyPosition(board, (x + direction, y - 1)):
    value += 10;
  if emptyPosition(board, (x + direction, y + 1)):
    value += 10;

  #the one case where having no open spaces infront of you is good is if
  #a piece is in the opponents home row.
  
  if piece == 'r':
    value += 5 * (7 - x);
  elif piece == 'b':
    value += 5 * x;

  return value;

#calculates the value of a piece at pos based on 3 attributes:
#offensive value
#defensive value
#mobility value
#
#default priorities have the AI focus on offensive moves and piece mobility. 
#priorities can change depending on the state of the board
#see report for details
def pieceValue(board, pos, piece, priority):
  value = 0;
  weight = 2;
  for func in priority:
    value += weight * func(board, pos, piece);
    weight -= .25;
  return value;

#predefined strategies
strategies = [[defensiveValue, offensiveValue, mobilityValue],\
              [offensiveValue, defensiveValue, mobilityValue],\
              [offensiveValue, mobilityValue, defensiveValue],\
              [defensiveValue, mobilityValue, offensiveValue],\
              [mobilityValue, defensiveValue, offensiveValue],\
              [mobilityValue, offensiveValue, defensiveValue]]; 


#Heuristic function.
#Input:     
#Type of return value: a real number
def hfun(node,space,player):
    cur_board = node.state.board
    value = 0
    opponent = OppDic1[player]
    
    #a list of functions listed from most to least important
    strategy = [];

    #do some preprocessing of the board to determine the player's
    #priorities
    enemy_count = 0;
    friend_count = 0;
    for i in range(8):
        for j in range(8):
          if cur_board[i][j] in PlayerDic[player]:
            if cur_board[i][j] in ['R', 'B']:
              friend_count += 50;
            else:
              friend_count += 10;
          elif cur_board[i][j] in PlayerDic[opponent]:
            if cur_board[i][j] in ['R', 'B']:
              enemy_count += 50;
            else:
              enemy_count += 10;
    
    #set strategy
    if friend_count >= 3 * enemy_count:
      strategy = [offensiveValue];
    elif friend_count >= 2 * enemy_count:
      strategy = [offensiveValue, offensiveValue, mobilityValue];
    elif friend_count >= 1.5 * enemy_count:
      strategy = [offensiveValue, mobilityValue, mobilityValue];
    elif friend_count > 1.2 *  enemy_count:
      strategy = [offensiveValue, mobilityValue, defensiveValue, mobilityValue];
    elif friend_count > enemy_count:
      strategy = [mobilityValue, offensiveValue, defensiveValue];
    elif friend_count == enemy_count:
      strategy = [mobilityValue, defensiveValue, offensiveValue];
    elif friend_count < (.2 * enemy_count):
      strategy = [offensiveValue];
    else:
      strategy = [defensiveValue, mobilityValue, defensiveValue, offensiveValue];

    value -=  (enemy_count - friend_count);

    #run the heuristic
    for i in range(8):
        for j in range(8):
          if cur_board[i][j] in PlayerDic[player]:
            value += pieceValue(cur_board, (i, j), cur_board[i][j], strategy);
          elif cur_board[i][j] in PlayerDic[opponent]:
            strategy = random.choice(strategies);
            value -= pieceValue(cur_board, (i, j), cur_board[i][j], strategy);
          
    return value;

def cutoff(state,depth,space,player):
    if depth >= max_depth or not successors(state,player):
        return 1
    else:
        return 0

#======================================================
#Please don't change anything below this point
#======================================================
def edgecost (state1, state2):
   return 1

def expand (n, succboards):
   if succboards == []:
      return []
   else:
      x = map(lambda s: Node(s,parent=n,depth=1+n.depth,\
              gval=n.gval+edgecost(n.state,s)),succboards)
      return x


#This function will return move. It has not been tested and it is not used yet
def GetMoveList(cur_board,suc_board,player):
    for i in range(8):
        for j in range(8):
            if suc_board[i][j]  == '.' and cur_board[i][j] in PlayerDic[player]:
                s,r = i,j
            if cur_board[i][j]  == '.' and suc_board[i][j] in PlayerDic[player]:
                a,b = i,j

    if abs(s-a) == 1:
        move = [(s,r),(a,b)]
    else:
        move = [(s,r)]
        while s != a and r != b:
            if s >= 2 and r >= 2 and cur_board[s-1][r-1] in Oppdic[player]  and suc_board[s-1][r-1] == '.':
                s,r = s-2,r-2
                move = move + [(s,r)]
            elif s >= 2 and r<= 5 and cur_board[s-1][r+1] in Oppdic[player]  and suc_board[s-1][r+1] == '.':
                s,r = s-2,r+2
                move = move + [(s,r)]
            elif s <= 5 and r >= 2 and cur_board[s+1][r-1] in Oppdic[player]  and suc_board[s+1][r-1] == '.':
                s,r = s+2,r-2
                move = move + [(s,r)]
            elif s <= 5 and r <= 5 and cur_board[s+1][r+1] in Oppdic[player]  and suc_board[s+1][r+1] == '.':
                s,r = s+2,r+2
                move = move + [(s,r)]
    return move

def Jump(board, a,b, jstep, player):
    result = []
    if player == 'b':
        #Jump:  upper right
        if a <= 5 and b <= 5 and (board[a+1][b+1] == 'r' or board[a+1][b+1] == 'R') and board[a+2][b+2] == '.':
            new_board = Copyboard(board)
            new_board[a][b], new_board[a+1][b+1] = '.','.'
            if a == 5:
                new_board[a+2][b+2] = 'B'
            else:
                new_board[a+2][b+2] = 'b'
            tlist  = Jump(new_board,a+2,b+2,jstep+1,'b')
            for state in tlist:
                state.move = [(a,b)]+ state.move 
            result = result + tlist
        #Jump:  upper left
        if a <= 5 and b >= 2 and (board[a+1][b-1] == 'r' or board[a+1][b-1] == 'R') and board[a+2][b-2] == '.':
            new_board = Copyboard(board)
            new_board[a][b], new_board[a+1][b-1] = '.','.'
            if a == 5:
                new_board[a+2][b-2] = 'B'
            else:
                new_board[a+2][b-2] = 'b'
            tlist  = Jump(new_board,a+2,b-2,jstep+1,'b')
            for state in tlist:
                state.move = [(a,b)]+ state.move 
            result = result + tlist
        if not result and jstep >= 1:
            result = [Board(board,move = [(a,b)])]
    elif player == 'r':
        #Jump:  down right
        if a >= 2 and b <= 5 and (board[a-1][b+1] == 'b' or board[a-1][b+1] == 'B') and board[a-2][b+2] == '.':
            new_board = Copyboard(board)
            new_board[a][b], new_board[a-1][b+1] = '.','.'
            if a == 2:
                new_board[a-2][b+2] = 'R'
            else:
                new_board[a-2][b+2] = 'r'
            tlist  = Jump(new_board,a-2,b+2,jstep+1,'r')
            for state in tlist:
                state.move = [(a,b)]+ state.move 
            result = result + tlist
        #Jump:  down left
        if a >= 2 and b >= 2 and (board[a-1][b-1] == 'b' or board[a-1][b-1] == 'B') and board[a-2][b-2] == '.':
            new_board = Copyboard(board)
            new_board[a][b], new_board[a-1][b-1] = '.','.'
            if a == 2:
                new_board[a-2][b-2] = 'R'
            else:
                new_board[a-2][b-2] = 'r'
            tlist  = Jump(new_board,a-2,b-2,jstep+1,'r')
            for state in tlist:
                state.move = [(a,b)]+ state.move 
            result = result + tlist
        if not result and jstep >= 1:
            result = [Board(board,move = [(a,b)])]
    elif player == 'B' or player == 'R':
        #Jump:  upper right
        if a <= 5 and b <= 5 and (board[a+1][b+1] in OppDic[player]) and board[a+2][b+2] == '.':
            new_board = Copyboard(board)
            new_board[a][b], new_board[a+1][b+1] = '.','.'    
            new_board[a+2][b+2] = player            
            tlist  = Jump(new_board,a+2,b+2,jstep+1,player)
            for state in tlist:
                state.move = [(a,b)]+ state.move 
            result = result + tlist
        #Jump:  upper left
        if a <= 5 and b >= 2 and (board[a+1][b-1] in OppDic[player]) and board[a+2][b-2] == '.':
            new_board = Copyboard(board)
            new_board[a][b], new_board[a+1][b-1] = '.','.'
            new_board[a+2][b-2] = player
            tlist  = Jump(new_board,a+2,b-2,jstep+1,player)
            for state in tlist:
                state.move = [(a,b)]+ state.move 
            result = result + tlist
        #Jump: down right
        if a >= 2 and b <= 5 and (board[a-1][b+1] in OppDic[player]) and board[a-2][b+2] == '.':
            new_board = Copyboard(board)
            new_board[a][b], new_board[a-1][b+1] = '.','.'
            new_board[a-2][b+2] = player
            tlist  = Jump(new_board,a-2,b+2,jstep+1,player)
            for state in tlist:
                state.move = [(a,b)]+ state.move 
            result = result + tlist
        #Jump: down left
        if a >= 2 and b >= 2 and (board[a-1][b-1] in OppDic[player]) and board[a-2][b-2] == '.':
            new_board = Copyboard(board)
            new_board[a][b], new_board[a-1][b-1] = '.','.'
            new_board[a-2][b-2] = player
            tlist  = Jump(new_board,a-2,b-2,jstep+1,player)
            for state in tlist:
                state.move = [(a,b)]+ state.move 
            result = result + tlist
        if not result and jstep >= 1:
            result = [Board(board,move = [(a,b)])]
    return result

def Copyboard(board):
    new_board = [[]]*8
    for i in range(8):
        new_board[i] = [] + board[i]
    return new_board

def successors(state,player):
    cur_board = state.board
    suc_result = []
    if player == 'b':
        #Test jump: If a piece can jump, it must jump
        piece_list = []
        for i in range(8):
            for j in range(8):
                if cur_board[i][j] == 'b' or cur_board[i][j] == 'B':                    
                    suc_result = suc_result + Jump(cur_board, i,j, 0, cur_board[i][j])
                    piece_list = piece_list + [[i,j]]
        #Move the piece one step
        if not suc_result:
            for x in piece_list:
                i,j = x[0],x[1]
                if cur_board[i][j] == 'b':
                    #(1)The piece is not in the rightmost column, move to upperright
                    if j <= 6 and cur_board[i+1][j+1] == '.':
                        suc_board = Copyboard(cur_board)
                        suc_board[i][j] = '.'
                        if i<=5:
                            suc_board[i+1][j+1] = 'b'
                        else:
                            suc_board[i+1][j+1] = 'B'                        
                        move = [(i,j),(i+1,j+1)]
                        suc_result = suc_result + [Board(suc_board,move)]
                    #(2)The pice is not in the leftmost column, move to the upperleft
                    if j >= 1 and cur_board[i+1][j-1] == '.':
                        suc_board = Copyboard(cur_board)
                        suc_board[i][j] = '.'                    
                        if i<= 5:
                            suc_board[i+1][j-1] = 'b'
                        else:
                            suc_board[i+1][j-1] = 'B'                        
                        move = [(i,j),(i+1,j-1)]
                        suc_result = suc_result + [Board(suc_board,move)]                                    
                elif cur_board[i][j] == 'B':
                    #Move the king one step
                    #(1)The king is not in top and the rightmost column, move to upperright 
                    if i <= 6 and j <= 6 and cur_board[i+1][j+1] == '.':
                        suc_board = Copyboard(cur_board)
                        suc_board[i][j] = '.'    
                        suc_board[i+1][j+1] = 'B'                        
                        move = [(i,j),(i+1,j+1)]
                        suc_result = suc_result + [Board(suc_board,move)]
                    #(2)The king is not in top and the leftmost column, move to the upperleft
                    if i <= 6 and j >= 1 and cur_board[i+1][j-1] == '.':
                        suc_board = Copyboard(cur_board)
                        suc_board[i][j] = '.'                                    
                        suc_board[i+1][j-1] = 'B'                        
                        move = [(i,j),(i+1,j-1)]
                        suc_result = suc_result + [Board(suc_board,move)]
                    #(3)The king is not in bottom and the rightmost column, move to the downright
                    if i >= 1 and j <= 6 and cur_board[i-1][j+1] == '.':
                        suc_board = Copyboard(cur_board)
                        suc_board[i][j] = '.'                                    
                        suc_board[i-1][j+1] = 'B'
                        move = [(i,j),(i-1,j+1)]
                        suc_result = suc_result + [Board(suc_board,move)]
                    #(4)The king is not in the leftmost column, move to the downleft
                    if i >= 1 and j >= 1 and cur_board[i-1][j-1] == '.':
                        suc_board = Copyboard(cur_board)
                        suc_board[i][j] = '.'                                    
                        suc_board[i-1][j-1] = 'B'
                        move = [(i,j),(i-1,j-1)]
                        suc_result = suc_result + [Board(suc_board,move)]                    
    else:
        #Test jump: If a piece can jump, it must jump
        piece_list = []
        for i in range(8):
            for j in range(8):
                if cur_board[i][j] == 'r' or cur_board[i][j] == 'R':                    
                    suc_result = suc_result + Jump(cur_board, i,j, 0, cur_board[i][j])
                    piece_list = piece_list + [[i,j]]
        #If jump is not available, move the piece one step
        if not suc_result:
            for x in piece_list:
                i,j = x[0],x[1]
                if cur_board[i][j] == 'r':
                    #move the piece one step
                    #(1)the piece is not in the rightmost column, move to downright
                    if j <= 6 and cur_board[i-1][j+1] == '.':
                        suc_board = Copyboard(cur_board)
                        suc_board[i][j] = '.'
                        if i >= 2:
                            suc_board[i-1][j+1] = 'r'
                        else:
                            suc_board[i-1][j+1] = 'R'
                        move = [(i,j),(i-1,j+1)]
                        suc_result = suc_result + [Board(suc_board,move)]
                    #(2)the pice is not in the leftmost column, move to the upperleft
                    if j >= 1 and cur_board[i-1][j-1] == '.':
                        suc_board = Copyboard(cur_board)
                        suc_board[i][j] = '.'                    
                        if i >= 2:
                            suc_board[i-1][j-1] = 'r'
                        else:
                            suc_board[i-1][j-1] = 'R'
                        move = [(i,j),(i-1,j-1)]
                        suc_result = suc_result + [Board(suc_board,move)]
                elif cur_board[i][j] == 'R':
                   #move the king one step
                    #(1)the king is not in top and the rightmost column, move to upperright
                    if i <= 6 and j <= 6 and cur_board[i+1][j+1] == '.':
                        suc_board = Copyboard(cur_board)
                        suc_board[i][j] = '.'    
                        suc_board[i+1][j+1] = 'R'
                        move = [(i,j),(i+1,j+1)]
                        suc_result = suc_result + [Board(suc_board,move)]
                    #(2)the king is not in top and the leftmost column, move to the upperleft
                    if i <= 6 and j >= 1 and cur_board[i+1][j-1] == '.':
                        suc_board = Copyboard(cur_board)
                        suc_board[i][j] = '.'                                    
                        suc_board[i+1][j-1] = 'R'
                        move = [(i,j),(i+1,j-1)]
                        suc_result = suc_result + [Board(suc_board,move)]
                    #(3)the king is not in bottom and the rightmost column, move to the downright
                    if i >= 1 and j <= 6 and cur_board[i-1][j+1] == '.':
                        suc_board = Copyboard(cur_board)
                        suc_board[i][j] = '.'                                    
                        suc_board[i-1][j+1] = 'R'
                        move = [(i,j),(i-1,j+1)]
                        suc_result = suc_result + [Board(suc_board,move)]
                    #(4)the king is not in the leftmost column, move to the upperleft
                    if i >= 1 and j >= 1 and cur_board[i-1][j-1] == '.':
                        suc_board = Copyboard(cur_board)
                        suc_board[i][j] = '.'                                    
                        suc_board[i-1][j-1] = 'R'
                        move = [(i,j),(i-1,j-1)]
                        suc_result = suc_result + [Board(suc_board,move)]        
    return suc_result

#=============================================================================   
def maxv (node, parentalpha, parentbeta, depth,space,player):
 alpha = Thresh(parentalpha.val,parentalpha.bestSucc)
 beta = Thresh(parentbeta.val,parentbeta.bestSucc)
 if PrintFlag:
     #print "player =",player
     print space, "maxv", node.state, " alpha:", alpha.val, " beta:", beta.val,"-->"
 if cutoff(node.state,depth,space,player):
    #t = Thresh(hfun(node.state,space,PLAYER),node)
    t = Thresh(hfun(node,space,PLAYER),node)
    if PrintFlag:
        print space,"returning",t,"<--"
    return t
 else:
    for s in expand(node,successors(node.state,player)):
        newspace = space + "    "
        minval = minv(s, alpha, beta, depth+1,newspace,OppDic1[player])
        if minval.val > alpha.val:
           alpha.val = minval.val
           alpha.bestSucc = s
           if PrintFlag:
               print space, "alpha updated to ", alpha.val
        if alpha.val >= beta.val:
           if PrintFlag: 
               print space, "alpha >= beta so returning beta, which is ", beta.val,"<--"
           return beta
    if PrintFlag:
        print space, "returning alpha ", alpha,"<--"
    return alpha

def minv (node, parentalpha, parentbeta, depth, space,player):
 alpha = Thresh(parentalpha.val,parentalpha.bestSucc)
 beta = Thresh(parentbeta.val,parentbeta.bestSucc)
 if PrintFlag:
     #print "player =",player
     print space, "minv",node.state, " alpha:", alpha.val, " beta:", beta.val,"-->"
 if cutoff(node.state,depth,space,player):
    #t = Thresh(hfun(node.state,space,PLAYER),node)
    t = Thresh(hfun(node,space,PLAYER),node)
    if PrintFlag:
        print space,"returning",t,"<--"
    return t
 else:
    for s in expand(node,successors(node.state,player)):
        newspace = space + "    "
        maxval = maxv(s, alpha, beta, depth+1,newspace,OppDic1[player])
        if maxval.val < beta.val:
           beta.val = maxval.val
           beta.bestSucc = s
           if PrintFlag:
               print space, "beta updated to ", beta.val
        if beta.val <=  alpha.val:
           if PrintFlag:
               print space, "beta <= alpha so returning alpha, which is ", alpha.val,"<--"
           return alpha
    if PrintFlag:
        print space, "returning beta ", beta
    return beta


#============= The Checkers Problem =========================
Initial_Board = [ ['b','.','b','.','b','.','b','.'],\
                  ['.','b','.','b','.','b','.','b'],\
                  ['b','.','b','.','b','.','b','.'],\
                  ['.','.','.','.','.','.','.','.'],\
                  ['.','.','.','.','.','.','.','.'],\
                  ['.','r','.','r','.','r','.','r'],\
                  ['r','.','r','.','r','.','r','.'],\
                  ['.','r','.','r','.','r','.','r'] \
                ]
#This board is used to test one-step move
Test_Board1 = [ ['b','.','b','.','.','.','.','.'],\
                ['.','b','.','.','.','r','.','b'],\
                ['.','.','.','.','b','.','.','.'],\
                ['.','B','.','.','.','.','.','R'],\
                ['B','.','.','.','.','.','R','.'],\
                ['.','.','.','r','.','.','.','.'],\
                ['r','.','b','.','.','.','r','.'],\
                ['.','.','.','.','.','r','.','r'] \
                ]

#These boards are used to test jump
Test_Board2 = [ ['.','.','.','.','.','.','.','.'],\
                ['r','.','R','.','R','.','R','.'],\
                ['.','.','.','.','.','.','.','.'],\
                ['r','.','r','.','R','.','r','.'],\
                ['.','.','.','.','.','.','.','.'],\
                ['R','.','R','.','r','.','R','.'],\
                ['.','.','.','B','.','.','.','.'],\
                ['.','.','.','.','.','.','b','.'] \
                ]

Test_Board3 = [ ['.','.','.','.','.','.','.','.'],\
                ['b','.','b','.','b','.','B','.'],\
                ['.','.','.','.','.','.','.','.'],\
                ['b','.','b','.','B','.','b','.'],\
                ['.','.','.','.','.','.','.','.'],\
                ['B','.','b','.','b','.','B','.'],\
                ['.','.','.','r','.','.','.','.'],\
                ['.','.','.','.','.','.','R','.'] \
                ]

PieceToKingDic = {'r':'R', 'b':'B'}
OppDic = {'B':['r','R'],'R':['b','B'],'b':['r','R'],'r':['r','R']}
PlayerDic = {'r':['r','R'],'b':['b','B'],'R':['r','R'],'B':['b','B']}
OppDic1 = {'b':'r','r':'b'}
PrintFlag = 0
#PLAYER = 'r'

#The following code is used to test the successors function
#Board(Test_Board1).PrintBoard(name = "Test_Board1 for one step move:")
#for board in successors(Board(Test_Board1),'r'):
#    board.PrintBoard(parent = Board(Test_Board1))
#    print "";

#Board(Test_Board2).PrintBoard(name = "Test_Board2 for jump:")
#for board in successors(Board(Test_Board2),'b'):
#    board.PrintBoard(parent = Board(Test_Board2))
#    print "";

#Board(Test_Board3).PrintBoard(name = "Test_Board3 for jump:")
#for board in successors(Board(Test_Board3),'r'):
#    board.PrintBoard(parent = Board(Test_Board3))
#    print "";
 
