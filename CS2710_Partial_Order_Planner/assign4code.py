'''
  Cha Li
  11.20.2011
  CS2710 - HW4
'''

from __future__ import nested_scopes
import string
import random
from utils import *
import copy
""" Partial-Order Planning
    usage:  python plan.py 1  to run, e.g.,  planning problem 1 hardcoded in this file.
"""            
#==========================
class Node:

   def __init__ (self,state,statename=[],parent=[],depth=0,gval=0,hval=None):
      self.state = state
      if statename: self.statename = statename
      else:  self.statename = state
      self.parent = parent
      self.depth = depth
      self.gval = gval
      self.hval = hval

   def printNode(self):
      print "State: ", self.statename, " Gval=",self.gval,
      print "Hval=",self.hval,"depth=",self.depth,
      if self.parent:
         print " Parent state:", self.parent.statename
      else:
         print "root node"

   def inlineprintNode(self):
      strings = ["(depth:", ", gval:",", hval:",", fval:"]
      nums =    [str(self.depth),str(self.gval),\
                 str(h(self)),str(self.gval + h(self))]
      s = ""
      for i in range(4):
         s = s + strings[i]
         if int(nums[i]) < 10:   s = s + " "
         if int(nums[i]) < 100:  s = s + " "
         s = s + nums[i]
      s = s + ")"
      print self.statename,s

def makeNodes (n, succStates):
   return [Node(s,parent=n,depth=1+n.depth,\
            gval=n.gval+edgecost(n.state,s))\
            for s in succStates]

#=====Utils (to help create propositionalized versions of FOL actions)
def cr(l,e):
    r=copy.copy(l)
    r.remove(e)
    return r

def perm(l):
    if len(l)==0:
        return [[]]
    else:
        res=[([h]+t) for h in l for t in perm( cr(l,h) )]
        return res

def astr(name,vals):
    s = name + "("
    if vals:
        s = s + str(vals[0])
        for r in vals[1:]:
            s = s + "," + str(r)
    s = s + ")"
    return s

# =======================
# States are plans
class Plan:
 
    def __init__ (self,steps=[],ordercons = [],causallinks=[],\
                 openconds=[],threats=[]):
      global gensymplan
      self.steps = steps           #[step]
      self.ordercons = ordercons   #[(step,step)]
      self.causallinks = causallinks #[(step,proposition,step)]
      self.openconds =  openconds  #[(proposition,step)]
      self.threats = threats       #[causallink,threateningstep]
      self.hval = -1
      self.comment = ""            #for readability of output
      gensymplan = gensymplan + 1  
      self.id = "plan" + str(gensymplan) #for readability of output
    
    #extra functions for checking if things exists already
    def stepExists(self, step):
      for s in self.steps: 
        #parse out step number
        s = s[string.find(s, DIVIDER) + 1 :];
        if step == s:
          return True;
      return False;
  
# Cheap, readable self-documentation.
STEP1_CL = 0    # step1 of a CausalLink (s,p,s) is item 0
PROP_CL = 1     # prop of a CausalLink (s,p,s) is item 1
STEP2_CL = 2    # step2 of a CausalLink (s,p,s) is item 2
CL_THREAT   = 0 # causal link of a threat ((s,p,s),s) is item 0
STEP_THREAT = 1 # step of a threat ((s,p,s),s) is item 1
PROP_OC = 0     # prop of an open condition (p,s) is item 0
STEP_OC = 1     # step of an open condition (p,s) is item 1
DIVIDER = "."   #separate step number from step name

def printstate(state,wantcomment=1):
   print ""
   print state.id, "-----"
   if wantcomment and state.comment: print state.comment
   print "steps:",state.steps
   if state.causallinks:
      print "causal links:"
      for c in state.causallinks:
         print "  (%s < %s < %s)" % (c[0], c[1], c[2])
   if state.ordercons:
      print "ordering constraints:"
      none = 0;
      for o in state.ordercons:
         if not o[0] == "init" and not o[0] == "goal"\
            and not o[1] == "init" and not o[1] == "goal":
            none = 0
            break
      if none:  print "none"
      else:       
         for o in state.ordercons:
            if o[1] != o[0]:
              print "  (%s < %s)" % (o[0], o[1])
            '''
            if not o[0] == "init" and not o[0] == "goal"\
               and not o[1] == "init" and not o[1] == "goal"\
               and o[1] != o[0]:
               print "  (%s < %s)" % (o[0], o[1])
            '''
   if state.openconds:
      print "open conditions:"
      for o in state.openconds:
         print "  (%s, %s)" % (o[0], o[1])
   if state.threats:
      print "threats:"
      for t in state.threats:
         print "  ",t

#======================================
# Simple example 1.  From an assignment by Martha Pollack.
#
# Note: Under these definitions, the following is a valid plan:
#  sweep wash-floor dust, and the final world-state would
#    contain floor-dusty and floor-clean
# 
preconds1 = {"init":[],"sweep":["floor-dusty"],\
   "vaccuum":["floor-dusty","vaccuum-works"],\
   "wash-floor":["floor-not-dusty","floor-dirty"],\
   "dust":["furniture-dusty"]}

adds1 = {"goal":[],"sweep":["floor-not-dusty"],\
   "vaccuum":[],"wash-floor":["floor-clean"],\
   "dust":["floor-dusty","furniture-clean"]}

deletes1 = {"init":[],"goal":[],"sweep":["floor-dusty"],\
   "vaccuum":["floor-dusty"],"wash-floor":["floor-dirty"],\
   "dust":["floor-not-dusty","furniture-dusty"]}

initprops1 = ["floor-dusty","floor-dirty","furniture-dusty","vaccuum-works"]

goalprops1 = ["floor-clean","furniture-clean","floor-not-dusty"]
#=======================================
# CS2710 Assignment 4 example
#
preconds3 = {
            "init":[],\
            "playSkyrim":["at-home", "not-tired"],\
            "sleepInBed":["at-home", "tired"],\
            "writeReport":["not-buggy-code"],\
            "compressCode":["not-buggy-code"],\
            "eatFood":["hungry"],\
            "drinkCoffee":["not-at-home", "tired"],\
            "writeCode":["not-tired", "not-at-home","not-hungry"],\
            "debugCode":["buggy-code", "not-use-bathroom"],\
            "useBathroom":["use-bathroom"]\
            }

adds3 = {
            "goal":[],\
            "playSkyrim":["hungry","tired","use-bathroom"],\
            "sleepInBed":["hungry", "not-tired"],\
            "writeReport":["have-report"],\
            "compressCode":["code-compressed"],\
            "eatFood":["not-hungry"],\
            "drinkCoffee":["not-tired"],\
            "writeCode":["buggy-code"],\
            "debugCode":["not-buggy-code","not-code-compressed"],\
            "useBathroom":["not-use-bathroom"]\
        }

deletes3 =  {
            "init":[],\
            "goal":[],\
            "playSkyrim":["not-tired", "not-use-bathroom", "not-hungry"],\
            "sleepInBed":["tired", "not-hungry"],\
            "writeReport":["not-have-report"],\
            "compressCode":["not-code-compressed"],\
            "eatFood":["not-hungry"],\
            "drinkCoffee":["tired"],\
            "writeCode":[],\
            "debugCode":["buggy-code"],\
            "useBathroom":["use-bathroom"]\
            }

initprops3 = ["hungry", "tired", "not-at-home", "use-bathroom"]

goalprops3 = ["have-report", "code-compressed", "not-at-home"]

#=======================================
#blocks world example
##preconds = {"init":[]}
#
adds2 = {"goal":[]}

deletes2 = {"init":[],"goal":[]}

#initprops = ["on(a,table)","on(b,table)","on(c,table)",\
#             "clear(a)","clear(b)","clear(c)"]

#initprops = ["on(a,b)","on(b,table)","on(c,table)",\
#             "clear(a)","clear(c)"]

initprops2 = ["on(b,table)","on(c,a)","on(a,table)",\
             "clear(b)","clear(c)"]
            
#
#goalprops = ["on(a,b)","on(c,a)"]
#goalprops = ["on(b,c)","on(a,table)"]
goalprops2 = ["on(a,b)","on(b,c)"]
#
preconds2 = {"init":[]}
#
#
domain  = ['a','b','c']
#
b = {}

for valset in perm(domain):
    varstr = "M" + valset[0] + "FROM" + valset[1] + "TO" + valset[2]
    b['x'] = valset[0]
    b['y'] = valset[1]
    b['z'] = valset[2]
    preconds2[varstr] =\
     [astr("on",[b['x'],b['y']]),astr("clear",[b['x']]),astr("clear",[b['z']])]
    adds2[varstr] =\
     [astr("on",[b['x'],b['z']]),astr("clear",[b['y']])]
    deletes2[varstr] =\
     [astr("on",[b['x'],b['y']]),astr("clear",[b['z']])]

b = {}

for valset in [['a','b'],['a','c'],['b','a'],['b','c'],['c','a'],['c','b']]:
    b['x'] = valset[0]
    b['y'] = valset[1]
    varstr = "M" + b['x'] + "FROM" + b['y'] + "TOtable"
    preconds2[varstr] =\
     [astr("on",[b['x'],b['y']]),astr("clear",[b['x']])]
    adds2[varstr] =\
     [astr("on",[b['x'],"table"]),astr("clear",[b['y']])]
    deletes2[varstr] =\
     [astr("on",[b['x'],b['y']])]

b = {}

for valset in [['a','b'],['a','c'],['b','a'],['b','c'],['c','a'],['c','b']]:
    b['x'] = valset[0]
    b['z'] = valset[1]
    varstr = "M" + b['x'] + "FROMtableTO" + b['z']
    preconds2[varstr] =\
     [astr("on",[b['x'],"table"]),astr("clear",[b['x']]),astr("clear",[b['z']])]
    adds2[varstr] =\
     [astr("on",[b['x'],b['z']])]
    deletes2[varstr] =\
     [astr("on",[b['x'],"table"]),astr("clear",[b['z']])]

#======================================
# The simple flat tire problem description from the text
#
preconds4 = {"init":[],"removeSpareTrunk":["at(spare,trunk)"],"removeFlatAxle":["at(flat,axle)"],\
             "leaveOvernight":[],"putonSpareAxle":["at(spare,ground)","clear(axle)"]}

deletes4 = {"init":[],"goal":[],\
            "removeSpareTrunk":["at(spare,trunk)"],"removeFlatAxle":["at(flat,axle)"],\
            "leaveOvernight":["at(spare,ground)","at(spare,axle)","at(spare,trunk)",\
                              "at(flat,ground)","at(flat,axle)"],\
            "putonSpareAxle":["at(spare,ground)","clear(axle)"]}

adds4 = {"goal":[],"removeSpareTrunk":["at(spare,ground)"],\
         "removeFlatAxle":["at(flat,ground)","clear(axle)"],\
         "leaveOvernight":[],"putonSpareAxle":["at(spare,axle)"]}

initprops4 = ["at(flat,axle)","at(spare,trunk)"]

goalprops4 = ["at(spare,axle)"]

#==================================================
def printoperators ():
   for a in adds.keys():
      if not a == "init" and not a == "goal":
         for p in preconds[a]:  print p," ",
         print ""
         printa = a
         while len(printa) < len("-------------------"):
            printa = " " + printa + " "
         print "-------------------"
         print printa
         print "-------------------"
         if adds[a] and not deletes[a]:
            for x in adds[a]: print x," ",
            print ""
         elif adds[a] and deletes[a]:
            for x in adds[a]: print x," ",
            for y in deletes[a]: print "DEL:%s  " % (y),
            print ""
         elif deletes[a]:
            for y in deletes[a]: print "DEL:%s  " % (y),
            print ""
      print " "
      print " "

#====== Functions defining the problem. 

#check if order conditions are consistent
#avoid things like s1 > s2, s2 > s1
def orderConsistent(order):
  total_order = [];
  for (pre, post) in order:
    if pre == post:
      continue;

    pre_i = -1;
    post_i = -1;

    if pre in total_order:
      pre_i = total_order.index(pre);

    if post in total_order:
      post_i = total_order.index(post);

    #if pre comes after post, then the ordering under inspection
    #is inconsistent pre->post
    if (pre_i != -1 and post_i != -1) and (pre_i > post_i):
      #however, unless post->pre is explicity specified in an ordercon, we can swap the list elements
      if (post, pre) in order:
        return False;
      else:
        total_order.remove(pre);
        total_order.insert(post_i, pre);

    #insert into total_ordering based on the index of pre and post
    if pre_i == post_i:
      total_order.append(pre);
      total_order.append(post);
    elif pre_i < post_i and pre_i == -1:
      total_order.insert(post_i, pre);
    elif post_i < pre_i and post_i == -1:
      total_order.insert(pre_i + 1, post);
  
  return True;


def goalp(node):
  state = node.state;
  return len(state.openconds) == 0\
          and \
         len(state.threats) == 0;

def h(node):
  state = node.state;
  return len(state.openconds) + len(state.threats);

def edgecost (state1, state2):
   return 1

#return a list of nodes
def successors(node):
  children = [];    #this will be a list of Plans
  
  plan = node.state
  if printPlans:
    print "fringe[0].state:",plan.id, "---"
    printstate(plan)
    if node.parent:
       print "parent: plan",node.parent.state.id
  
  print "-------------"

  #decide if an open condition of threat should be fixed
  to_fix = random.randint(0, len(plan.openconds) + len(plan.threats) - 1) 
  
  #fix flaws
  if to_fix < len(plan.openconds):
    #pick a random open_cond to fix
    open_cond = plan.openconds[ random.randint(0, len(plan.openconds) - 1) ];
    print "[STATUS] Working on open condition: ", open_cond;
    open_prop = open_cond[PROP_OC];
    end_step = open_cond[STEP_OC];

    #go through add list and see which step can satisfy the open prop
    for step, props  in adds.iteritems():
      if (open_prop in props):
        #create the successor
        child = Plan();

        child.steps = list(plan.steps);
        if not child.stepExists(step):
          child.steps.append(str(node.depth) + DIVIDER + step);
          print "[STATUS] Added Step: ", step;

        #create new ordering condition based on open condition and step that satifies it
        new_ordercon = (step, end_step);
        child.ordercons = list(plan.ordercons);
        if new_ordercon not in child.ordercons:
          child.ordercons.append(new_ordercon)
          print "[STATUS] Added New Order Condition: ", new_ordercon;

        #create and add new causal link
        new_causal= (step, open_prop, end_step);
        child.causallinks = list(plan.causallinks);
        if new_causal not in child.causallinks:
          child.causallinks.append(new_causal);
          print "[STATUS] Added New Causal Link: ", new_causal;


        #update open conditions
        #1. remove any resolved open conditions
        #2. add new open conditions (the preconditions of added step)
        child.openconds = list(plan.openconds);
        child.openconds.remove((open_prop, end_step));
        print "[STATUS] Removing Open Condition: ", (open_prop, end_step);

        #add pre conditions of added step to open conditions
        for precond in preconds[step]:
          child.openconds.append((precond, step));
        
        #see if the adds of the added step remove any other open conditions
        for opencond in child.openconds:
          if opencond[PROP_OC] in adds[step]:
            child.openconds.remove(opencond);  
        
        #detect threats
        #previous threats carry over
        child.threats = plan.threats;
        
        num_threats = 0;

        #1. check if any of the current steps delete any of the new step's preconditions
        for previous_step in plan.steps:
          #parse out the step number
          previous_step = previous_step[string.find(previous_step, DIVIDER) + 1  :];
          delete_list = deletes[previous_step]
          if open_prop in delete_list:
            new_threat = (new_causal, previous_step);  
            #prevent duplicate threats
            if new_threat not in child.threats:
              child.threats.append(new_threat);
              num_threats += 1;

        #2. check if the delete list of the new step delete any of the conditions in the
        #   current causal links
        for current_causal in plan.causallinks:
          if current_causal[PROP_CL] in deletes[step]:
            new_threat = (current_causal, step);  
            #prevent duplicate threats
            if new_threat not in child.threats:
              child.threats.append(new_threat);
              num_threats += 1;
        
        print "[STATUS] Found", num_threats, "threats"; 

        child.comment = "RESOLVED OPEN CONDITION: " + step + " satifies " + open_prop
        children.append(child);
  
  #2. fix threats
  elif to_fix >= len(plan.openconds):
    #copy over parent's attributes. DEEP COPY ALL THE THINGS
    child = Plan();
    child.steps = list(plan.steps);
    child.ordercons = list(plan.ordercons);
    child.causallinks = list(plan.causallinks);
    child.openconds = list(plan.openconds);
    
    #pick a random threat to fix
    threat = plan.threats[ random.randint(0, len(plan.threats) - 1) ]; 
    print "[STATUS] Working on threat: ", threat;
    clause = threat[CL_THREAT]
    step = threat[STEP_THREAT]

    #deep copy some lists so i can work with them and not effect original
    child_threats = list(plan.threats);
    order = list(plan.ordercons);
            
    pre_step = clause[STEP1_CL];
    post_step = clause[STEP2_CL];

    #try demotion, goal cant be demoted
    if step != "goal" and pre_step != "init" and orderConsistent(order + [(step, pre_step)]):
      child_threats.remove(threat);
      #fixed a threat, create new plan
      new_ordercon = (step, clause[STEP1_CL])
      if new_ordercon not in child.ordercons: 
        child.ordercons.append(new_ordercon);
      child.threats = child_threats;
      child.comment = "RESOLVED THREAT: producer of clause(" + pre_step + ") ordered after " + step; 
      children.append(child);
      print "[STATUS] Threat resolved through demotion:", new_ordercon

    #try promotion, init cant be promoted
    elif step != "init" and post_step != "goal" and orderConsistent(order + [(post_step, step)]):
      child_threats.remove(threat);
      #fixed a threat, create new plan
      new_ordercon = (clause[STEP2_CL], step);
      if new_ordercon not in child.ordercons: 
        child.ordercons.append(new_ordercon);
      child.threats = child_threats;
      child.comment = "RESOLVED THREAT: consumer of clause(" + post_step + ") ordered before " + step; 
      children.append(child);
      print "[STATUS] Threat resolved through promotion:", new_ordercon 

  return children;

#======= The core search functions and auxiliaries

def treesearch(start,fringe):
   """Search through the successors of a problem to find a goal.

   start -- the start state
   fringe -- an empty queue
   Don't worry about repeated paths to a state """
   fringe.append(Node(start))
   while len(fringe) > 0:
      print "=========";
      print "Len of fringe:",len(fringe)   
      cur = fringe.pop()
      if goalp(cur): return cur
      if cur.depth >= INFINITY:
         print "** REACHED INFINITY; giving up"
         return []
      if printVerbose:
         print "VISITED:",
         cur.inlineprintNode()
      fringe.extend(makeNodes(cur,successors(cur)))
   return []

def graphsearch(start,fringe):
   """Search through the successors of a problem to find a goal.

   start -- the start state
   fringe -- an empty queue
   If a new path to a state is found, save the shortest-length path"""

   expanded = {}
   fringe.append(Node(start))
   while len(fringe) > 0:
      cur = fringe.pop()
      if cur.depth >= INFINITY:
         print "** REACHED INFINITY; giving up"
         return []
      # The next if statement is just for printing
      if printVerbose and expanded.has_key(cur.state):
         if expanded[cur.state].gval <= cur.gval:
            print "**New path to",cur.statename,"from",cur.parent.statename,\
            "is NOT better than the old path to",cur.statename
         else:
            print "**New path to",cur.statename,"from",cur.parent.statename,\
            "IS better than the old path to",cur.statename
      if not (expanded.has_key(cur.state) and\
              expanded[cur.state].gval <= cur.gval):
         expanded[cur.state] = cur
         if goalp(cur):
            return cur         
         if printVerbose:
            print "VISITED:",
            cur.inlineprintNode()
         fringe.extend(makeNodes(cur,successors(cur)))
   return []

def depthfirst(start,coreAlgorithm=treesearch):
    """Search the deepest nodes in the search tree first. """
    return coreAlgorithm (start,Stack())

def breadthfirst(start,coreAlgorithm=treesearch):
   """Search the shallowest nodes in the search tree first. """
   return coreAlgorithm (start,FIFOQueue())

def uniformcost(start,coreAlgorithm=treesearch):
   """Search the nodes with the lowest path cost first. """
   return coreAlgorithm (start,\
             PriorityQueue(lambda a,b:a.gval < b.gval))

def bestfirst(start,coreAlgorithm=treesearch):
   """Search the nodes with the lowest h scores first.
      Called greedy search in Russell and Norvig 1st edition,
      and greedy best-first search in the 2nd edition.  """
   return coreAlgorithm (start,\
             PriorityQueue(lambda a,b: h(a) < h(b)))

def Astar(start,coreAlgorithm=treesearch):
   """Search the nodes with the lowest f=h+g scores first."""
   return coreAlgorithm(start,\
             PriorityQueue(lambda a,b: h(a) + a.gval < h(b) + b.gval))

def iterativeDeepening(start):
   result = []
   depthlim = 1
   startnode = Node(start)
   while not result and depthlim < INFINITY:
      result = depthLimSearch([startnode],depthlim)
      depthlim = depthlim + 1
      if depthlim == INFINITY: print "** REACHED INFINITY; giving up"
   return result

def depthLimSearch(fringe,depthlim):
   if printVerbose:
      print ""     
      print "**Starting at root with depthLim=%d" %(depthlim)
      print ""     
   while fringe:
      # The following line was an error. When I wrote this, I thought 
      # pop returned the first element of a list.  In fact, it
      # returns the last element of the list.
      # cur = fringe.pop()
      cur = fringe[0]
      fringe = fringe[1:]
      if goalp (cur):
         return cur
      if printVerbose:
         print "VISITED:",
         cur.inlineprintNode()
      if cur.depth <= depthlim:
         fringe = makeNodes(cur,successors(cur)) + fringe
   return []

def IDAstar(start):
   result = []
   startNode = Node(start)
   fLim = h(startNode)
   while not result and fLim < FINFINITY:
      if printVerbose:
         print ""     
         print "**Starting at root with fLim=%d" %(fLim)
         print ""     
      result, fLim = fLimSearch([startNode],fLim)
      if fLim == FINFINITY: print "** REACHED INFINITY; giving up"
   return result


def fLimSearch(fringe,fLim):
   nextF = FINFINITY
   while fringe:
      cur = fringe[0]
      fringe = fringe[1:]
      curF = cur.gval + h(cur)
      if goalp (cur): return (cur, curF)
      if curF <= fLim:
         if printVerbose:
            print "VISITED:",
            cur.inlineprintNode()
         succNodes = makeNodes(cur,successors(cur))
         for s in succNodes:
            fVal = s.gval + h(s)
            if fVal > fLim and fVal < nextF:
               nextF = fVal
         fringe = succNodes + fringe 
   return ([],nextF)

def beamsearch(start,beamwidth):
   
   def insertByH (item,lst):
      i = 0
      while i < len(lst) and h(lst[i]) < h(item): i = i + 1
      return lst[:i] + [item] + lst[i:]
   
   fringe = [Node(start)]
   while len(fringe) > 0:
      cur = fringe[0]
      fringe = fringe[1:]
      if goalp(cur): return cur
      if cur.depth >= INFINITY:
         print "** REACHED INFINITY; giving up"
         return []
      if printVerbose:
         print "LEN(FRINGE):",len(fringe),"VISITED:",
         cur.inlineprintNode()
      newnodes = makeNodes(cur,successors(cur))    
      for s in newnodes:
         fringe = insertByH(s, fringe)
      fringe = fringe[:beamwidth]   
   return []


#==== Main program.  Change this as appropriate for your application.
#==== 
#==== 

print sys.argv
def planfun(initprops,goalprops):

   adds["init"] = initprops
   preconds["goal"] = goalprops
   print ""
   print "initial props:", initprops
   print
   print "goal props:", goalprops
   print
   print "add list: ", adds
   print
   print "precond list: ", preconds
   print
   print "delete list: ", deletes
   print


   print ""

  

   initialstate = Plan(steps=["init","goal"],openconds=[(x,"goal") for x in goalprops])
   printstate(initialstate)
   return Astar(initialstate)

#===============
gensymnode = 0

gensymplan = 0

gensymstep = 0

   
def printPathToNode(node):
   if node:
      node.printNode()
      if node.parent:
         printPathToNode(node.parent)

def printStatesOnPathToNode (node):
   n = node
   states = []
   while n:
      states = states + [n.state]
      n = n.parent
   states.reverse()
   for s in states:
      printstate(s)

#=========================================
#
maxdepth = 15
INFINITY = 35
printVerbose = 0
printPlans = 1

if len(sys.argv) > 1:
   exec("initprops = initprops" + str(sys.argv[1]))
   exec("goalprops = goalprops" + str(sys.argv[1]))
   exec("preconds = preconds" + str(sys.argv[1]))
   exec("adds = adds" + str(sys.argv[1]))
   exec("deletes = deletes" + str(sys.argv[1]))
else:
   initprops = initprops2
   goalprops = goalprops2
   preconds = preconds2
   adds = adds2
   deletes = deletes2
printoperators()

result = planfun(initprops,goalprops)
print ""
print "Result:**********************"
print ""

printStatesOnPathToNode(result)

