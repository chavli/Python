'''
  Bookcase.py

  Cha Li
  December 2, 2011
  CS0007 - TA

  The Bookcase class is used to hold Book objects.
'''


from Book import *

class Bookcase:

  #declare class variables
  self.shelves = []
  self.num_shelves = 0;
  self.free_space = 0;
  
  #constructor
  def __init__(self, shelves, max_books):
    self.num_shelves = shelves;
    self.free_space = max_books;
    
    #represent the shelves as a list of lists
    for i in range(0, self.num_shelves):
      self.shelves.append([])
  
  #method that allows books to be added to the bookcase
  def addBook(self, book, shelf):
    if self.free_space > 0:
      self.shelves[shelf].append(book);
      print "Added " + book.title + "to shelf " + str(shelf);
      self.free_space -= 1;
    else:
      print "Bookshelf full";

  #string representation of the bookcase
  def __str__(self):
    info = "";
    for shelf in self.shelves:
      for book in shelf:
        info +=  str(book) + ", "
      info += "\n"

    return info

