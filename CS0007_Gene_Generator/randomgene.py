#
# Cha Li
# 11.16.2011
# TA-CS0007
#
# Generate a random gene sequence and output it to a randomgene.txt. The
# following is an example of the generated file:
#
#   0001 ACGATTAGTAGAGTAACCACTGTATATATA 0030                                                                                                                                                       
#   0031 CATGCACCGTAAGTAACGGAA          0051 
#
# Put this file in the same folder as your gene manipulator code. 
# randomgene.txt ends up in the same folder as this file.
#
# Just run this file the same way you run all your python files
#
# If you find a bug in this code, email me an explanation about the bug you
# found and if it's actually a bug I'll give you some extra
# credit (towards the gene manipulation assignment).
#

import random

#global variables
MIN_LEN = 30;
MAX_LEN = 1000;
NUCLEOTIDES = ["T", "C", "G", "A"];
FILENAME = "randomgene.txt";

#create a random gene sequence of the given length and return it
def geneSequence(length):
  sequence = "";
  while(length > 0):
    #append a random valid nucleotide to the sequence
    sequence += random.choice(NUCLEOTIDES);
    length -= 1;

  return sequence;

def main():
  sequence_length = random.randint(MIN_LEN, MAX_LEN);
  print "Generating gene sequence of length " + str(sequence_length);

  #first, the file is opened for writing and everything in it is erased by
  #writing a blank
  #
  #if the file didn't exist in the first place then an empty file is created
  file = open(FILENAME, "w");
  file.write("");
  file.close();

  #second, the file is re-opened for appending so new data can be added
  file = open(FILENAME, "a");
  

  #each line of the file can have a max of 30 nucleotides, so write
  #sequence_length MIN_LE N at a time.
  #
  #if sequence_length < MIN_LEN, you write sequence_length nucleotides
  #
  #counter is used to create the numbers that are added to the start and end
  #of each line
  #
  counter = 0;
  while sequence_length > 0:
    #reduce sequence length by the length of the gene sequence that gets 
    #created
    if sequence_length > MIN_LEN:
      sequence_length -= MIN_LEN;
      sequence = geneSequence(MIN_LEN)
    else:
      sequence = geneSequence(sequence_length);
      sequence_length = 0;

    #formatted file writing, same as formatted strings
    file.write("%04d %-30s %04d\n" % (counter + 1, sequence, counter + len(sequence)));
    counter += len(sequence);
  
  #close the file since nothing else will be written
  file.close();
  print "DONE";


"""
  code starts from here
"""
if __name__== "__main__":
  main();


