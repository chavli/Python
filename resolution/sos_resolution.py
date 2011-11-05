from __future__ import nested_scopes
import string
from unify import unify
from unify import applySubs
import sys
import re
"""Performs resolution refutation given the input clauses and the negation of the goal, already
   translated to clausal form.

   usage:  python resolution.py infile

   infile should contain one clause per line.  "|" is the or operator.  "-" is negation.
   Each clause must end with a period.  Variables are symbols starting with "var_".
   Upper/lower case has no meaning.  Include spaces in the input lines at your own risk.


   Sample input:
   -p(var_x) | q(var_x).
   -q(var_x1) | r(var_x1).
   p(tom).
   -r(tom).

   Output for above input:
   Initial Clause Set:*************
   c1     -p(var_x)) | q(var_x) []
   c2     -q(var_x1)) | r(var_x1) []
   c3     p(tom) []
   c4     -r(tom) []
   -----
   Result:**********************
   node6 whose state is:
   [] ['c7', 'c4']
   c7     r(var_x1) ['c5', 'c3']
   c5     -p(var_x)) | r(var_x1) ['c1', 'c2']
   c1     -p(var_x)) | q(var_x) []
   c2     -q(var_x1)) | r(var_x1) []
   c3     p(tom) []
   c4     -r(tom) []


   The list to a right of each clause contains the parent clauses, if the clause was produced
   using resolution (otherwise, it is the empty list).  The result contains the original
   clauses (listed last) plus all of the clauses produced during the resolution process.
   Success is reached when there is an empty resolvent.   For example, success is reached in
   the example because resolving clauses c7 and c4 produces the empty set.  Thus, we know there
   was a contradiction in the original set of sentences.

   This version of resolution is not complete.  The successor function returns only
   the result of resolving the first clause with each of the other clauses.
   This is a limited form of the set-of-support strategy.  
   The following inputs show the issue; the same clauses are involved, but
   the second one succeeds while the first one fails:

   q(tom).
   p(tom).
   -p(tom).

   p(tom).
   q(tom).
   -p(tom).

   """

class Node:

   def __init__ (self,state, sos, parent=[],depth=0,gval=0,hval=None):
      global nodegensym
      self.state = state
      self.sos = sos;       #the set of support used by state
      self.parent = parent
      self.depth = depth
      self.gval = gval
      self.hval = hval
      self.id = "node" + str(nodegensym)
      nodegensym = nodegensym + 1

#succSos is an array of sos where each element corresponds to the state at the same 
#index in succStates. meaning the sos at i is to be used by the state at i
def makeNodes (n, succStates, succSos):
   return [Node(succStates[i], succSos[i],parent=n,depth=1+n.depth,\
            gval=n.gval+edgecost(n.state,succStates[i]))\
            for i in range(0, len(succStates))]

class Literal:

   def __init__ (self,neg,predicate,sentence):
      self.neg = neg
      self.pred = predicate
      self.sentence = sentence

class Clause:
   
   def __init__ (self,clause,source=[]):
      global clausegensym
      self.cl = clause
      self.id = "c" + str(clausegensym)
      self.source = source
      clausegensym = clausegensym + 1

#printing functions ==========================================

def printclause(cl):
   def litsentstring (litsent,newstring):
      if not type(litsent) == type([]):
         newstring = newstring + str(litsent)
      else:
         newstring = newstring + litsent[0] + "("
         for r in litsent[1:-1]:
            newstring = litsentstring(r,newstring)
            newstring = newstring + ","
         newstring = litsentstring(litsent[-1],newstring)
         newstring = newstring + ")"
      return newstring   

   def litstring (lit):
      if lit.neg == "-":
         new = litsentstring(lit.sentence,"-")      
      else:
         new = litsentstring(lit.sentence,"")
      return new

   if cl.cl == []:
      print cl.cl,cl.source
   else:
      print "%-5s " %cl.id,
      ls = ""
      for l in cl.cl[:-1]: 
         ls = ls + litstring(l) + " | "
      ls = ls + litstring(cl.cl[-1])
      print ls, cl.source

def printnode(node):
   print node.id, "whose state is:"
   printstate(node.state)

def printstate (state):
   for s in state:  printclause(s)
   print "-----"

#===================================================
def successors(node):
   # node.state is a list of clauses, with the first one the current
   # clause

   def resolvent (parent1,parent2,lit1,lit2,uresult):
      both = parent1.cl + parent2.cl
      new = []
      for b in both:
         if not b == lit1 and not b == lit2:
            newsentence = applySubs (b.sentence, uresult)
            new = new +[ Literal(b.neg,b.pred,newsentence)]
      new111 =  Clause(new,[parent1.id,parent2.id])
      return new111

   succs = []
   sos = [];
   #see if any clause in the current states sos can cancel out any other 
   #clauses in the current KB
   for sos_clause in node.sos:

     #target is the clause in the KB being compared to sos_clause
     for target in node.state:

       #compare literals
       for lit1 in target.cl:
         for lit2 in sos_clause.cl:
           if not lit1.neg == lit2.neg and lit1.pred == lit2.pred:
             uresult = unify(lit1.sentence,lit2.sentence)
             if not uresult == 'fail':
               #resolve
               #create a new successor state and an updated sos for it
               new_clause = resolvent(sos_clause, target, lit1, lit2, uresult);
               new_sos = [new_clause] + node.sos;
               newsucc = [new_clause] + node.state;
               sos += [new_sos];
               succs += [newsucc]

   #return a tuple of successor states paired with that states set of support
   return (succs, sos)

def h(node):
   return len(node.state[0])

def goalp(node):
   #if node.state[0].cl == []:  return 1
   #else: return 0
   for l in node.state:
     if l.cl==[]: return 1
   return 0
   
def edgecost (state1, state2):
   return 1

def depthfirstsearch(start):
   stack = [Node(start, [start[-1]])] #second argument is set of support clauses
   while stack:
      cur = stack[0]
      stack = stack[1:]
      if goalp (cur):
         return cur
      stack = makeNodes(cur,*successors(cur)) + stack
   return []

def getkbfromfile():
   def breakintoargs(cur):
      paren = 0
      i = 0
      args = []
      while cur[i:]:
         if cur[i] == '(': 
            paren = paren + 1
            i = i + 1
         elif cur[i] == ')': 
            paren = paren - 1
            i = i + 1
         elif cur[i] == ',' and paren == 0:
            args = args + [cur[:i]]
            cur = cur[i+1:]
            i = 0
         else:  
            i = i + 1
      if( cur[-1]=='.' ):
         args = args + [cur[:-2]]
      else:
         args = args + [cur[:-1]]
      #args = args + [cur[:-1]]
      return args

   def tolist(cur):
      predfunRE = re.compile(r"\s*(?P<pf>[^(]+)\((?P<rest>.+)")
      if not cur:  return ""
      elif not '(' in list(cur): return cur
      else:
         m = predfunRE.search(cur)
         if not m: print "!!!!error"
         else:
            pf = m.group("pf")
            rest = m.group("rest")
            args = breakintoargs(rest)
            return [pf] + [tolist(a) for a in args]

   #leadingRE = re.compile(r"\s*(?P<rest>.+)\).*")
   leadingRE = re.compile(r"\s*(?P<rest>.+)")
   kb = []
   infile = open(sys.argv[1],'r')
   line = infile.readline()
   while line != "":
      if not line[0] == '#':
         lits = string.split(line[:-2],'|')
         litlist = []
         for l in lits:
            m = leadingRE.search(l) # get rid of leading spaces
            cur = m.group('rest')
            if cur[0] == "-":
               neg = "-"
               cur = cur[1:]
            else:  neg = "+"
            litlist = litlist + [[neg] + [tolist(cur)]]
         kb = kb + [litlist]   
      line = infile.readline()
   infile.close()
   return kb

def doexample (initList):

   def createInit(lst):
      initclauses = []
      for l in lst:
         curclause = []
         for literal in l:
            curclause = curclause + [Literal(literal[0],literal[1][0],literal[1])]
         initclauses = initclauses + [Clause(curclause)]
      return initclauses

   print "Start:*************"
   initclauses = createInit(initList)
   print "Initial Clause Set:*************"
   printstate(initclauses)
   result = depthfirstsearch(initclauses)
   print "Result:**********************"
   if result: printnode(result)
   else: print "failure"

# A simple example to try out; call doexample(kbsimple)
# all X p(X) -> q(X)
# all X q(X) -> r(X)
# p(tom)
# not r(tom)
kbsimple = [[["-",["p","var_x"]],["+",["q","var_x"]]],\
             [["-",["q","var_x1"]],["+",["r","var_x1"]]],\
             [["+",["p","tom"]]],\
             [["-",["r","tom"]]]]

maxdepth = 60
nodegensym = 1
clausegensym = 1

if len(sys.argv) > 1:
   doexample (getkbfromfile())
else: doexample (kbsimple)


