from sudoku import *
import time
class Solver:


    def AC3(self,csp, queue=None, removals=None):
        '''returns false if an inconsistency is found, and true otherwise'''
        '''
        your code here
        '''
        queue = []
        csp.support_pruning()
        for x in csp.neighbors:
            for y in csp.neighbors[x]:
                queue.append([x,y])
        while queue:
            test = queue.pop(0)
            if self.revise(csp,test[0],test[1],removals):
                if len(csp.curr_domains[test[0]]) == 0:
                    return False
                for val in csp.neighbors[test[0]]:
                    queue.append([val,test[0]])
        return True



    def revise(self,csp, Xi, Xj, removals):
        """Return true if we remove a value."""
        '''
        your code here
        '''
        revised = False
        for vi in csp.curr_domains[Xi]:
            satisfied = False
            for vj in csp.curr_domains[Xj]:
                if (csp.constraints(Xi, vi,Xj,vj)):
                    satisfied = True
            if (satisfied == False):
                csp.prune(Xi, vi, removals)
                revised = True
        return revised

    def backtrack(self, assignment, csp):
        csp.support_pruning()
        if csp.goal_test(assignment):
            return assignment
        for x in csp.curr_domains:
            if x not in assignment:
                var = x
                break
        for value in csp.curr_domains[var]:
            if csp.nconflicts(var,value,assignment) == 0:
                csp.assign(var,value,assignment)
                removals = csp.suppose(var,value)
                b = self.AC3(csp,None,removals)
                if b:
                    result = self.backtrack(assignment,csp)
                    if result:
                        return result
                csp.unassign(var,assignment)
                csp.restore(removals)
        return None


    def backtracking_search(self,csp):
        '''returns a solution or failure'''
        '''
        your code here
        '''
        self.AC3(csp)
        assignment = {}
        return self.backtrack(assignment, csp)


if __name__ == '__main__':

    '''
    Some board test cases, each string is a flat enumeration of all the board positions
    where . indicates an unfilled location
    Impossible: 123456789.........123456789123456789123456789123456789123456789123456789123456789
    Easy ..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..
    Easy ...7.46.3..38...51.1.9.327..34...76....6.8....62...98..473.6.1.68...13..3.12.5...
    Difficult ..5...1.3....2.........176.7.49....1...8.4...3....7..8.3.5....2....9....4.6...9..
    '''

    '''to check your implementatios:'''
    removals=[]
    assignment={}
    # AC3 should return false for impossible example above
    board = Sudoku('...7.46.3..38...51.1.9.327..34...76....6.8....62...98..473.6.1.68...13..3.12.5...')
    print(board)
    sol = Solver()
    start=time.clock()
    print(sol.AC3(board))
    print("time: " + str(time.clock() - start))
    board.display(board.infer_assignment())

    # backtracking search usage example
    solu = Solver()
    board1 = Sudoku('..5...1.3....2.........176.7.49....1...8.4...3....7..8.3.5....2....9....4.6...9..')
    start=time.clock()

    result = solu.backtracking_search(board1)
    print("time: " + str(time.clock() - start))
    board1.display(result) #<<< This will crash now since the result is empty
