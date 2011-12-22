#To run some examples, enter "python unify.py" on Linux; 
#"unify.py" on Windows
#
#
quotedSymbols = ["loves","mary","john","fred","var_x","var_y","var_z","dog"]
for s in quotedSymbols:
   cmd = s + " = " + "'" + s + "'"
   exec(cmd)

# A substitution is a list: [variable,filler being substituted for it]
# Following are constants for the respective list positions
filler = 1 
variable = 0

def isVar (x):
   # variables are represented as strings that begin with "var_"
   return type(x) is type("") and x[0:4] == "var_"

def isList (x):
   return type(x) == type([])

def applySubs (sentence, subs):
   # returns "sentence" with substitutions "subs" applied to it
   # starting with subs[0]
   new = sentence
   for s in subs:
      new = replaceAll(s[variable],s[filler],new)
   return new

def replaceAll(exp1, new, exp2):
   # replace all occurrences of exp1 in list exp2 with new
   if exp2 == []:
      return []
   elif not exp1 == exp2[0]:
      if type(exp2[0]) == type([]):
         return [replaceAll(exp1,new,exp2[0])] + replaceAll(exp1,new,exp2[1:])
      else:
         return [exp2[0]] + replaceAll(exp1,new,exp2[1:])
   else:
      return [new] + replaceAll(exp1,new,exp2[1:])

def unify (p, q):
   return auxUnify (p, q, [])

def auxUnify (p, q, bdgs):
   d = disagreement(p, q)
   # If there is no disagreement, then success.
   if not d: 
      return bdgs
   elif not isVar(d[0]) and not isVar(d[1]): return 'fail'
   else:
      if isVar(d[0]):
         var = d[0]
         other = d[1]
      else:
         var = d[1]
         other = d[0]
      if occursp (var,other):  
         print var,"occurs in", other
         return 'fail'
     # Resolve the disagreement by making appropriate
     # substitutions and then recurse on the result.
      else:
         pp = replaceAll(var,other,p)
         qq = replaceAll(var,other,q)
         return auxUnify (pp,qq, bdgs + [[var,other]])

def disagreement (p, q):
   # Return subexpressions where P and Q first disagree.
   if p == q: return []
   elif p == []:  return [q,p]
   elif q == []:  return [p,q]
   elif isVar(p) or isVar(q):
      if isVar(p): return [p,q]
      else:  return [q,p]
   # mismatching constants, or a constant and a list
   elif not isList (p) or not isList(q): return [p,q] 
   else: return disagreement (p[0],q[0]) or disagreement (p[1:],q[1:])

#  Check to see of if X appears anywhere in Y.
def occursp (x, y):
   if isVar(y):  return x == y
   elif y == [] or not isList(y):  return []
   else:
      return occursp (x,y[0]) or occursp (x, y[1:])

def callUnifyAndPrint(sentence1,sentence2):
   print "unify:"
   print " ",sentence1
   print " ",sentence2
   print "--------"
   result = unify (sentence1,sentence2)
   print "--------"
   if not result == 'fail':
      print "subs:",result
      print "result:", applySubs(sentence1,result)
   else: print "failure"

def printExamples():
   callUnifyAndPrint(["loves", ["dog", "var_x"], ["dog", "fred"]],["loves", "var_z", "var_z"])
   print "================================"
   callUnifyAndPrint (["loves", ["dog", fred], fred],["loves",["dog","fred"],fred])
   print "================================"
   callUnifyAndPrint (["loves", "var_x","var_x"],["loves", "var_x","var_x"])
   print "================================"
   callUnifyAndPrint (["loves", ["dog", fred], fred],["loves", "var_x", "var_y"])
   print "================================"
   callUnifyAndPrint (["loves", ["dog", fred], "mary"],["loves", ["dog", "var_x"], "var_y"])
   print "================================"
   callUnifyAndPrint (["loves", ["dog", fred], fred],["loves", "var_x", "var_x"])
   print "================================"
   callUnifyAndPrint (["loves", ["dog", fred], mary],["loves", ["dog", "var_x"], "var_x"])
   print "================================"
   callUnifyAndPrint ([loves,var_x,fred],[loves,[dog,var_x],fred])
   print "================================"
   callUnifyAndPrint ([loves,var_x,[dog,var_x]],[loves,var_y,var_y])
   print "================================"
   callUnifyAndPrint ([loves,var_y,var_y],[loves,var_x,[dog,var_x]])
   print "================================"
   print "Here is an example where unification fails because vars not",
   print "standardized apart"
   callUnifyAndPrint (["hates","agatha","var_x"],["hates","var_x",["f1","var_x"]])
   print "================================"
   callUnifyAndPrint (["hates","agatha","var_x"],["hates","var_y",["f1","var_y"]])

# printExamples()
