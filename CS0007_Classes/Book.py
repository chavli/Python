'''
  Book.py

  Cha Li
  December 2, 2011
  CS0007 - TA

  Simple class that represents a book
'''
class Book:
  self.title = "";
  self.pages = 0;

  #constructor
  def __init__(self, title, pages):
    self.title = title;
    self.pages = pages;
  
  #return the title and number of pages
  def __str__(self):
    return self.title + " has " + str(self.pages) + " pages.";


