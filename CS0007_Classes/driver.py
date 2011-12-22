'''
  Cha Li
  December 2, 2011
  CS0007 - TA

  This is the driver file that uses the Book and Bookcase classes. It illustrates
  how to use the methods of each class and how to use the classes together.
'''

from Book import *
from Bookcase import *

def main():

  #create a bookcase object
  bookshelf = Bookcase(3 ,10)

  #create three different book objects
  book = Book("A Tale of Two Cities", 100);
  book2 = Book("Harry Potter", 1000);
  book3 = Book("1984", 150);
  
  #print each book
  print book
  print book2
  print book3

  #add book to bookcase
  bookshelf.addBook(book, 0)
  bookshelf.addBook(book2, 1)
  bookshelf.addBook(book3, 2)

  #print the bookcase
  print bookshelf;


if __name__ == "__main__":
  main();


