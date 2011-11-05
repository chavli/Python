#
# simple file-based database system that allows for:
#   -insertion
#   -retrieval
#   -deletion

import string

#global variables
option = 0;
filename = "simple.db"

def newClass():
  print
  answer = "";    #a single answer
  answers = [];   #all answers
  
  #ask questions (formatted input)
  answer = raw_input("%-30s" % "Dept and Number (ex. CS2501):");
  answers += [string.upper(answer)]

  answer = raw_input("%-30s" % "Full Class Name:");
  answers += [answer]
  
  answer = raw_input("%-30s" % "Location:");
  answers += [answer]

  answer = raw_input("%-30s" % "Days:");
  answers += [answer]

  answer = raw_input("%-30s" % "Start Time:");
  answers += [answer]
  
  answer = raw_input("%-30s" % "End Time:");
  answers += [answer]
  
  #append everything in answers to a file
  db = open(filename, "a");

  #convert an array to string seprated by "|" 
  #ex. ["a", "b", "c"] -> "a|b|c"
  line = "|".join(answers);	
  db.write(line); #write the string
  db.write("\n"); #add a new line so subsequent entries will be on separate lines
  db.close();
  print "Entry Written\n"

def lookupClass():
  print
  lookup = raw_input("%-30s" % "Enter Class Dept and Number (ex. CS2501):");
  lookup = string.upper(lookup);
  db = open(filename, "r");
  for line in db:
    line = line.strip();
    #turn line back into an array
    #ex. "a|b|c" -> ["a", "b", "c"]
    data = line.split("|");
    
    #print data

    #if class dept and num matches print info
    if data[0] == lookup:
      #print all the data stored in the line
      print "Class Found"
      print "%-30s %s" % ("Class Dept and Number:", data[0]); 
      print "%-30s %s" % ("Full Name:", data[1]); 
      print "%-30s %s" % ("Location:", data[2]); 
      print "%-30s %s" % ("Days:", data[3]); 
      print "%-30s %s" % ("Start Time:", data[4]); 
      print "%-30s %s" % ("End Time:", data[5]); 
      print
  
  db.close();

#EXTRA CREDIT due 11/2
#implement deleteClass which removes an entry from the database file. the entry
#to be deleted is specified by the user. you can decide which fields to base
#it on (class name, location , time, etc.)
#
#trying to lookup a deleted class should result in nothing
#
def deleteClass():
  return;

"""
  Program starts down here
"""
while option != 4:
  print "===== Simple Class Manager =====";
  print "1 - New Class\n2 - Lookup Class\n3 - Delete Class\n4 - Exit";
  option = input("Option: ");

  if option == 1:
    newClass();
  elif option == 2:
    lookupClass();
  elif option == 3:
    deleteClass()


