import time
import sys
# Written by Peter Norvig.  From the on-line code archive of Russell & Norvig,
# AI: A Modern Approach.
#
# If you need a refresher on heaps:
# www.cs.pitt.edu/~wiebe/courses/CS2710/lectures/heapPriorityQueues.pdf
#
# A heap is used to maintain the priority queue used by heuristic search.
# The operations we will use are all O(log n).  
#
# 3 types of queues are defined in this file.
#        Stack(): A Last In First Out Queue.
#        FIFOQueue(): A First In First Out Queue.
#        PriorityQueue(lt): Queue where items are sorted by lt, (default <).
#   Each type supports the following methods and functions:
#        q.append(item)  -- add an item to the queue
#        q.extend(items) -- equivalent to: for item in items: q.append(item)
#        q.pop()         -- return the top item from the queue, and remove it from the queue
#        len(q)          -- number of items in q (also q.__len())

def Stack():
    """Return an empty list, suitable as a Last-In-First-Out Queue.
    Ex: q = Stack(); q.append(1); q.append(2); q.pop(), q.pop() ==> (2, 1)"""
    return []

class FIFOQueue:
    """A First-In-First-Out Queue.
    Ex: q = FIFOQueue();q.append(1);q.append(2); q.pop(), q.pop() ==> (1, 2)"""
    # len(), append, and extend are already defined for lists
    def __init__(self): self.A = []; self.start = 0
    def append(self, item): self.A.append(item)
    def __len__(self): return len(self.A) - self.start
    def extend(self, items): self.A.extend(items)     
    def pop(self):
        e = self.A[self.start]
        self.start += 1
        if self.start > 5 and self.start > len(self.A)/2:
            self.A = self.A[self.start:]
            self.start = 0
        return e

class PriorityQueue:
    "A queue in which the minimum element (as determined by lt) is first."
    def __init__(self, lt): self.A = []; self.lt = lt
    def append(self, item):
        A = self.A
        A.append(item)
        i = len(A) - 1 
        # the parent is (i-1) / 2 (i.e., integer divisiion)
        while i > 0 and self.lt(item, A[(i-1)/2]):
            A[i], i = A[(i-1)/2], (i-1)/2
        A[i] = item

    def extend(self, items):
        for item in items: self.append(item)

    def __len__(self): return len(self.A)

    def pop(self):
        if len(self.A) == 1: return self.A.pop()
        e = self.A[0]
        self.A[0] = self.A.pop()
        self.heapify(0)
        return e

    def heapify(self, i):
        "Assumes A is an array such that left(i) and right(i) are heaps,"
        "move A[i] into the correct position.  See CLR&S p. 130"
        A, lt = self.A, self.lt
        left, right, N = 2*i + 1, 2*i + 2, len(A)-1
        if left <= N and lt(A[left], A[i]):
            smallest = left
        else:
            smallest = i
        if right <= N and lt(A[right], A[smallest]):
            smallest = right
        if smallest != i:
            A[i], A[smallest] = A[smallest], A[i]
            self.heapify(smallest)

#=======================================

def timer(n, *fn_and_args):
    """Apply fn to args n times and return the number of seconds elapsed.
    You can leave out the n and it defaults to 1.
    Ex: timer(100, abs, -1); timer(1e4, Dict); timer(pow, 3, 4); timer(Dict)"""
    import time
    try:
        n, fn, args = int(n), fn_and_args[0], fn_and_args[1:]
    except TypeError: # n was not a number; it must be fn, with n=1 as default
        n, fn, args = 1, n, fn_and_args
    iterations = range(n)
    start_time = time.clock()
    for i in iterations:
        val = fn(*args)
    elapsed = time.clock() - start_time 
    return {'val': val, 'secs': elapsed}

"""
#test timer
def wastetime(a,b):
    for i in range(1000):
       for j in range(1000):
           x = a * b / float(b) * a
    return x           

print timer(2,wastetime,100,100),"==> {'secs': 4.6899999999999995, 'val': 10000.0}"
"""

#==================================================
