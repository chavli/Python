"""
  Cha Li
  10.24.2011
  Assignment 3
  CS007 - TA

  A program that sorts a pile of pancakes so the largest pancakes are at the
  bottom
"""
import random

FANCY = True
CURRENT = 0;
FLIPS  = 1;
ORIGINAL = 2;


#
# create a pile of n pancakes of random size [1-n] in random order
#
def makePile(n):
  shuffled = [];
  
  #create the pile of pancakes
  for x in range(0, n):
    shuffled += [x + 1];

  #shuffle the shuffled array
  random.shuffle(shuffled);
  original = shuffled; 
  #[current_state, number of moves, original_state]
  return [shuffled, 0, list(shuffled)];

#
# flip the top k pancakes in the pile, same concept as reversing a string
#
def flip(pile, k):
  queue = [];

  #remove items from the top of the pile , and add each item to another list
  #such that first item removed from the pile is the first item in the new list
  #second is second, third is third, and so on.
  #
  #use the list functions defined by python
  for i in range(0, k):
    top = pile[CURRENT].pop(0)
    queue.append(top);
  
  #after adding the pancakes to the new list, remove pancakes from the front
  #of the new list and add them to the front of current pile
  #
  #continue using list functions
  while len(queue) > 0:
    top = queue.pop(0);
    pile[CURRENT]  = [top] + pile[CURRENT];
  
  #increment number of flips by 1
  pile[FLIPS] += 1;

#
# find the largest pancake not in the correct position and return the index of
# of that pancake
#
def indexOfGreatestNotInPlace(pile):
  index = -1;
  largest = 0;
  current_pile = pile[CURRENT];
  for i in range(0, len(current_pile)):
    #if the pancake is in the wrong position and larger than
    #what the code has seen before save the info about it
    if current_pile[i] != (i + 1) and current_pile[i] > largest:
      index = i;                  #save the location of the largest pancake
      largest = current_pile[i];  #save the size of the largest pancake

  #return the location of the largest pancake, or -1 if the pile is sorted
  return index;

#
# return the top pancake
#
def topPancake(pile):
  return pile[CURRENT][0];

#
# return the number of flips executed so far
#
def flipsSoFar(pile):
  return pile[FLIPS];

#
# restore current state of pile to original pile
#
def reset(pile):
  pile[CURRENT] = list(pile[ORIGINAL]);
  pile[FLIPS] = 0;

#
# computer will sort the pile
#
def solve(pile):
  print "Initial Pile: "
  printPile(pile);
  while not isSorted(pile):
    #1. find the index of the largest misplaced pancake
    index = indexOfGreatestNotInPlace(pile);

    #2. increment the index by 1 so the largest pancake is included in a flip
    index += 1;
    
    #3. flip the pancakes so the largest pancake is at the top of the pile
    flip(pile, index);
    print "Pile after flip " + str(flipsSoFar(pile)) + ":";
    printPile(pile);

    #4. do another flip so the largest pancake is put in it's correct spot
    # the size of the flip is determine by the size of the top pancake
    flip(pile, topPancake(pile));
    print "Pile after flip " + str(flipsSoFar(pile)) + ":";
    printPile(pile);

  print "DONE"


#
# human plays the game
#
def playGame(pile):
  #keep playing until the pile is sorted
  while not isSorted(pile):
    printPile(pile);
    toflip = input("Flip how many pancakes (-1 to exit): ");
    if toflip < 0:
      break;

    if toflip >= 2:
      flip(pile, toflip);

  #if the player gave up, ask if they want the solution
  # the pile won't be sorted at this point in the code if the user gave up
  if not isSorted(pile):
    ans = raw_input("Do you want to see the answer (y/n)? ");
    if ans == "y":
      print "\nSolution: ";
      reset(pile);
      solve(pile);

#
# check if the pile is sorted
#
def isSorted(pile):
  cur_pile = pile[CURRENT];
  for i in range(0, len(cur_pile)):
    #if we find one item out of place than we know the entire list 
    #isn't sorted
    if cur_pile[i] != (i + 1):
      return False;

  #if the code makes it to this point than the list is sorted
  return True;

#
# print the pile
#
def printPile(pile):
  if FANCY:
    i = 1;
    for pancake in pile[CURRENT]:
      print "%30s %2d [%d]" % (pancake * "=", pancake, i);
      i += 1;
    print "\n";
  else:
    print "Current Pile is: " + str(pile[CURRENT]) + "\n";

#
# program starts here
#
print "===== Pancake Flipper ====="
size = -1;
while size < 1 or size > 30: 
  size = input("Number of Pancakes(1-30): ");

#create the initial values used by the game
state = makePile(size);

#play the game
playGame(state);
