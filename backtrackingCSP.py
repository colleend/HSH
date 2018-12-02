import collections, util, copy
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import networkx as nx
import math
import geopy.distance 


# intersections = {(0.03, 0.05): 3, (0.08, 1.2):1}
start = (40.7199779, -74.0053254) #start lat, lon
end = (40.7199380, -74.0014250)
def create_csp(G, start, end, crimeCounts):

    euc = geopy.distance.distance(start, end).meters #get start end as distance in km 
    #print euc


    csp = util.CSP(start, end)
    variables = [(node[0], crimeCounts[node[0]]) for node in G.nodes(data=True)] 
    domain = [0, 1] #if node is in path or not 
    for v in variables:  
        csp.add_variable(v, domain)

    print (csp.variables)

    for v in variables: 
        #need to make sure start node is 1 and end node is 1 
        # Get (lat, lon) from v
        vLatLon = (G.nodes[v[0]]['y'], G.nodes[v[0]]['x'])
        if (vLatLon == start or vLatLon == end):
            csp.add_unary_factor(v, lambda b: b == 1)

        neighbors = G.neighbors(v[0]) #get neighbors of v using G
        for neighbor in neighbors: 
            def crimeCountLength(n, neigh):
                #print (G.edges[v[0],neighbor, 0])
                edgeWeight = G.edges[v[0],neighbor,0]['weights']
                distanceTotal = G.edges[v[0],neighbor,0]['length']
                if distanceTotal > euc: 
                    return 0
                else: 
                    return (1./np.log(edgeWeight))

            neighborCrimeCounts = crimeCounts[neighbor]
            #print ("neighbor " + str(neighbor))
            #print ("neighbor crime counts " + str(neighborCrimeCounts))
            neighborV = (neighbor, neighborCrimeCounts)
            if (v != neighborV):
                csp.add_binary_factor(v, neighborV, crimeCountLength)

    return csp 


'''
    variables = ['{}, {}'.format(lat,lon) for (lat, lon) in intersections] 
    for v in variables:
        newStr = v.split(',')
        floatLat = float(newStr[0])
        floatLon = float(newStr[1])
        tup = (floatLat, floatLon)
        domain = intersections[tup]
        csp.add_variable(tup, domain)'''

    #G = nx.graph()


    #impose binary factors 

    #impose unary factor at start and at end 


def run_csp(crimeCounts, G):
    solver = BacktrackingSearch()
    csp = create_csp(G, start, end, crimeCounts)
    solver.solve(csp)
    print solver.optimalWeight
    print solver.numOptimalAssignments
    print solver.numOperations
    print solver.optimalAssignment

#run_csp()
#create_csp()


class BacktrackingSearch():
    
    def reset_results(self):
        """
        This function resets the statistics of the different aspects of the
        CSP solver. We will be using the values here for grading, so please
        do not make any modification to these variables.
        """
        # Keep track of the best assignment and weight found.
        self.optimalAssignment = {}
        self.optimalWeight = 0

        # Keep track of the number of optimal assignments and assignments. These
        # two values should be identical when the CSP is unweighted or only has binary
        # weights.
        self.numOptimalAssignments = 0
        self.numAssignments = 0

        # Keep track of the number of times backtrack() gets called.
        self.numOperations = 0

        # Keep track of the number of operations to get to the very first successful
        # assignment (doesn't have to be optimal).
        self.firstAssignmentNumOperations = 0

        # List of all solutions found.
        self.allAssignments = []

    def print_stats(self):
        """
        Prints a message summarizing the outcome of the solver.
        """
        if self.optimalAssignment:
            print "Found %d optimal assignments with weight %f in %d operations" % \
                (self.numOptimalAssignments, self.optimalWeight, self.numOperations)
            print "First assignment took %d operations" % self.firstAssignmentNumOperations
        else:
            print "No solution was found."

    def get_delta_weight(self, assignment, var, val):
        """
        Given a CSP, a partial assignment, and a proposed new value for a variable,
        return the change of weights after assigning the variable with the proposed
        value.

        @param assignment: A dictionary of current assignment. Unassigned variables
            do not have entries, while an assigned variable has the assigned value
            as value in dictionary. e.g. if the domain of the variable A is [5,6],
            and 6 was assigned to it, then assignment[A] == 6.
        @param var: name of an unassigned variable.
        @param val: the proposed value.

        @return w: Change in weights as a result of the proposed assignment. This
            will be used as a multiplier on the current weight.
        """
        assert var not in assignment
        w = 1.0
        if self.csp.unaryFactors[var]:
            w *= self.csp.unaryFactors[var][val]
            if w == 0: return w
        for var2, factor in self.csp.binaryFactors[var].iteritems():
            if var2 not in assignment: continue  # Not assigned yet
            w *= factor[val][assignment[var2]]
            if w == 0: return w
        return w

    def solve(self, csp, mcv = False, ac3 = False):
        """
        Solves the given weighted CSP using heuristics as specified in the
        parameter. Note that unlike a typical unweighted CSP where the search
        terminates when one solution is found, we want this function to find
        all possible assignments. The results are stored in the variables
        described in reset_result().

        @param csp: A weighted CSP.
        @param mcv: When enabled, Most Constrained Variable heuristics is used.
        @param ac3: When enabled, AC-3 will be used after each assignment of an
            variable is made.
        """
        # CSP to be solved.
        self.csp = csp

        # Set the search heuristics requested asked.
        self.mcv = mcv
        self.ac3 = ac3

        # Reset solutions from previous search.
        self.reset_results()

        # The dictionary of domains of every variable in the CSP.
        self.domains = {var: list(self.csp.values[var]) for var in self.csp.variables}

        # Perform backtracking search.
        self.backtrack({}, 0, 1)
        # Print summary of solutions.
        self.print_stats()

    def backtrack(self, assignment, numAssigned, weight):
        """
        Perform the back-tracking algorithms to find all possible solutions to
        the CSP.

        @param assignment: A dictionary of current assignment. Unassigned variables
            do not have entries, while an assigned variable has the assigned value
            as value in dictionary. e.g. if the domain of the variable A is [5,6],
            and 6 was assigned to it, then assignment[A] == 6.
        @param numAssigned: Number of currently assigned variables
        @param weight: The weight of the current partial assignment.
        """
        self.numOperations += 1
        assert weight > 0

        if numAssigned == self.csp.numVars:
            # A satisfiable solution have been found. Update the statistics.
            self.numAssignments += 1
            newAssignment = {}
            for var in self.csp.variables:
                newAssignment[var] = assignment[var]
            self.allAssignments.append(newAssignment)

            if len(self.optimalAssignment) == 0 or weight >= self.optimalWeight:
                if weight == self.optimalWeight:
                    self.numOptimalAssignments += 1
                else:
                    self.numOptimalAssignments = 1
                self.optimalWeight = weight

                self.optimalAssignment = newAssignment
                if self.firstAssignmentNumOperations == 0:
                    self.firstAssignmentNumOperations = self.numOperations
            return

        # Select the next variable to be assigned.
        var = self.get_unassigned_variable(assignment)
        # Get an ordering of the values.
        ordered_values = self.domains[var]

        # Continue the backtracking recursion using |var| and |ordered_values|.
        for val in ordered_values:
            deltaWeight = self.get_delta_weight(assignment, var, val)
            if deltaWeight > 0:
                assignment[var] = val
                self.backtrack(assignment, numAssigned + 1, weight * deltaWeight)
                del assignment[var]

    def get_unassigned_variable(self, assignment):
        """
        Given a partial assignment, return a currently unassigned variable.

        @param assignment: A dictionary of current assignment. This is the same as
            what you've seen so far.

        @return var: a currently unassigned variable.
        """

        if not self.mcv: #if not the most constrained
            # Select a variable without any heuristics.
            for var in self.csp.variables:
                if var not in assignment: return var
        else:
            variables = self.csp.variables
            unassignedVariables = []
            allVarA = []
            for var in variables: 
                if var not in assignment: # ONLY FOR UNASSIGNED VARIABLES 
                    possVals = self.domains[var] #all possible Values for variable
                    valuesA = 0
                    for val in possVals: 
                        valWeight = self.get_delta_weight(assignment, var, val)
                        if valWeight > 0: # Piazza: if get_delta_weight returns 0, that value for that variable violates the constraint.
                            valuesA += 1
                    allVarA.append(valuesA) #keeps track of # values a > 0 for each UNASSIGNED VARIABLE 
                    unassignedVariables.append(var) #keeps track of unassigned variables so index is the same

            correctIndex = 0 #keeps track of index of variable with fewest numver of values a which are consistent w curr assign
            index = 0 #keeps track of current index loop 
            fewestA = allVarA[0]
            for check in allVarA:
                if check < fewestA: #if ==, would keep one in earlier index (fewestA wouldn't change)
                    fewestA = check 
                    correctIndex = index 
                index += 1 
            return unassignedVariables[correctIndex]