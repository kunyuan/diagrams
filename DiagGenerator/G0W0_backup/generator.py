#!/usr/bin/env python
import numpy as np
import unittest
import unionfind
import copy

def GetVerList(Order):
#there are 2*Order vertexes
    return range(2*Order)

def GetInteractionPairs(Order):
    return [(2*i,2*i+1) for i in range(Order)]

def GetReference(Order):
    return range(2*Order)

def swap(array, i, j, measuring):
    array = list(array)
    # array[i],arrary[j]=array[j],array[i]
    tmp = array[i]
    array[i] = array[j]
    array[j] = tmp
    if measuring==i:
        measuring=j
    if measuring==j:
        measuring=i
    return tuple(array), measuring

def IsConnected(permutation,measure, reference, InteractionPairs):
    diagram=set(InteractionPairs)
    for i in range(len(permutation)):
        diagram.add((reference[i], permutation[i]))

    n_node = len(InteractionPairs)*2
    diagram_union = unionfind.UnionFind(n_node)

    for edge in diagram:
        if edge[0]!=edge[1] and not diagram_union.is_connected(edge[0], edge[1]):
            diagram_union.union(edge[0], edge[1])

    return diagram_union.get_n_circles() == 1

def HasTadpole(permutation,measure, reference):
    for i in range(len(permutation)):
        if reference[i]==permutation[i]:
            return True
    return False

def HasBuble(permutation, measure, reference):
    for i in range(len(reference)):
        end=permutation[permutation[i]]
        if reference[i]==end:
            return True
    return False

def GetAllPermutations(Order):
    reference=GetReference(Order)

    InteractionPairs=GetInteractionPairs(Order)
    permutations = [tuple(reference)]
    permutation_dict={tuple(reference):0}

    idx = 1
    mea=0
    while idx < 2*Order:
        print "Index {0}".format(idx)
        for i in range(len(permutations)):
            for j in range(idx):
                p,mea=swap(permutations[i], idx, j, mea)
                permutations.append(p)
                # measurings.append(m)
                permutation_dict[p]=mea
        idx += 1

    print permutation_dict
    print "Diagram Number: {0}".format(len(permutation_dict))
    print "Check Tadpole..."
    for p in permutation_dict.keys():
        if HasTadpole(p, permutation_dict[p], reference):
            del permutation_dict[p]

    # print "Diagram Number: {0}".format(len(permutation_dict))
    # print "Check Buble"
    # for p in permutation_dict.keys():
        # if HasBuble(p, permutation_dict[p], reference):
            # del permutation_dict[p]

    print "Diagram Number: {0}".format(len(permutation_dict))
    print "Check connectivity"
    for p in permutation_dict.keys():
        if not IsConnected(p, permutation_dict[p], reference, InteractionPairs):
            del permutation_dict[p]

    print "Diagram Number: {0}".format(len(permutation_dict))

    return permutation_dict.keys(), permutation_dict

def check_LR_Permutation(CurrentPermutation, Index, Deformation, Factor, InteractionPairs, PermutationDict):
    if Index==len(InteractionPairs):
        return Deformation, Factor
    permutation=list(CurrentPermutation)
    permutation_t=tuple(permutation)
    Deformation, Factor=check_Interaction_Permutation(permutation_t, 0, Deformation, Factor, InteractionPairs, PermutationDict)
    Deformation, Factor=check_LR_Permutation(permutation_t, Index+1, Deformation, Factor, InteractionPairs, PermutationDict)

    i,j=InteractionPairs[Index]
    ip,jp=permutation.index(i),permutation.index(j)
    permutation[ip]=j
    permutation[jp]=i
    permutation[i],permutation[j]=permutation[j],permutation[i]
    # print "after", i, j, permutation, Index
    permutation_t=tuple(permutation)
    Deformation, Factor=check_Interaction_Permutation(permutation_t, 0, Deformation, Factor, InteractionPairs, PermutationDict)
    Deformation, Factor=check_LR_Permutation(permutation_t, Index+1, Deformation, Factor, InteractionPairs, PermutationDict)
    return Deformation, Factor

def check_Interaction_Permutation(CurrentPermutation, InteractionIndex, Deformation, Factor, InteractionPairs, PermutationDict):
    permutation=list(CurrentPermutation)
    # print permutation, InteractionIndex

    permutation_t=tuple(permutation)
    if permutation_t in PermutationDict:
        # PermutationDict.remove(permutation_t)
        del PermutationDict[permutation_t]
        Deformation.append(permutation_t)
        Factor+=1

    if InteractionIndex==len(InteractionPairs):
        return Deformation, Factor

    Deformation, Factor=check_Interaction_Permutation(permutation_t, InteractionIndex+1, Deformation, Factor, InteractionPairs, PermutationDict)

    m,n=InteractionPairs[InteractionIndex]
    for i in range(InteractionIndex):
        k,l=InteractionPairs[i]
        mp,np,kp,lp=(permutation.index(e) for e in (m,n,k,l))
        permutation[mp]=k
        permutation[kp]=m
        permutation[np]=l
        permutation[lp]=n
        permutation[m],permutation[k]=permutation[k],permutation[m]
        permutation[n],permutation[l]=permutation[l],permutation[n]
        permutation_t=tuple(permutation)
        if permutation_t in PermutationDict:
            # PermutationList.remove(permutation_t)
            del PermutationDict[permutation_t]
            Deformation.append(permutation_t)
            Factor+=1
        Deformation, Factor=check_Interaction_Permutation(permutation_t, InteractionIndex+1, Deformation, Factor, InteractionPairs, PermutationDict)
    return Deformation, Factor

def Group(InteractionPairs, PermutationDict):
    UnlabeledDiagramList=[]
    FactorList=[]
    # for permutation in PermutationList[0:1]:
    while len(PermutationDict)>0:
        print "Remaining diagram {0}".format(len(PermutationDict))
        permutation=PermutationDict.keys()[0]
    # for permutation in [(0,1,3,2)]:
        # print permutation
        # if permutation==(0,1,3,2):
            # print "working"
        Factor=0
        Deformation=[]
        Deformation, Factor=check_LR_Permutation(permutation, 0, Deformation, Factor, InteractionPairs, PermutationDict)
        # if len(Deformation)>0:
        UnlabeledDiagramList.append(Deformation)
        # if permutation==(0,1,3,2):
            # print "working", Deformation
        FactorList.append(Factor)
    return UnlabeledDiagramList, FactorList

def DrawDiagrams(Reference, InteractionPairs, PermutationList, PermutationDict, NumberList=[]):
    i=0
    for permutation in PermutationList:
        i+=1
        measuring=PermutationDict[permutation]
        node1=measuring
        node2=permutation[measuring]
        with open("./diagram/{0}.gv".format(i), "w") as f: 
            f.write("digraph Feynman{\nnode [margin=0.1 fillcolor=grey fontcolor=black fontsize=10 width=0.2 shape=circle style=filled fixedsize=true];\n//nVer\n")
            if len(NumberList)==len(PermutationList):
                f.write("//Diagram Number: {0}\n".format(NumberList[i-1]))
            for n in Reference:
                if n==node1:
                    f.write("{0} [fillcolor=red, pos=\"0,0!\", pin=true];\n".format(n))
                elif n==node2:
                    f.write("{0} [fillcolor=red, pos=\"10,10!\", pin=true];\n".format(n))
                else:
                    f.write("{0} [fillcolor=grey];\n".format(n))
            f.write("//GLine\n")
            for n in range(len(Reference)):
                if PermutationDict[permutation]==n:
                    f.write("{0}->{1} [color=\"red\"];\n".format(Reference[n],permutation[n]))
                else:
                    f.write("{0}->{1} [color=\"blue\"];\n".format(Reference[n],permutation[n]))

            f.write("//WLine\n")
            for p in InteractionPairs:
                f.write("{0}->{1} [style=dashed arrowhead=none];\n".format(p[0],p[1]))
            f.write("}\n")
        f.close()

class Test(unittest.TestCase):
 
    def setUp(self):
        pass
 
    def test_InteractionPairs(self):
        self.assertEqual(GetInteractionPairs(3), [(0,1),(2,3),(4,5)])

    def test_Permutation(self):
        self.assertEqual(GetAllPermutations(1)[0], [(0,1), (1,0)])
        self.assertEqual(len(GetAllPermutations(2)[0]), 24) 
        self.assertEqual((1,0,2,3) in GetAllPermutations(2)[0], True)
        self.assertEqual(len(set(GetAllPermutations(2)[0])), 24)
        self.assertEqual(len(set(GetAllPermutations(3)[0])), 720)
        # self.assertEqual(len(set(GetAllPermutations(5))), 3628800)
 
if __name__ == '__main__':
    Order=3
    Reference=GetReference(Order)
    InteractionPairs=GetInteractionPairs(Order)
    PermutationList, PermutationDict=GetAllPermutations(Order)
    OriginalPermutationDict=copy.deepcopy(PermutationDict)
    # print PermutationList
    # DrawDiagrams(Reference, InteractionPairs, PermutationList)

    # DrawDiagrams(Reference, InteractionPairs, PermutationList)
    UnlabeledDiagramList, FactorList =  Group(InteractionPairs, PermutationDict)
    UniqueDiagrams=[]
    print "Total Unique Diagrams {0}\n".format(len(UnlabeledDiagramList))
    for g in UnlabeledDiagramList:
        # for e in g:
            # print "{0}".format(e)
        print g[0], len(g)
        UniqueDiagrams.append(g[0])
    # print UniqueDiagrams
    # DrawDiagrams(Reference, InteractionPairs, UniqueDiagrams)
    DrawDiagrams(Reference, InteractionPairs, UniqueDiagrams, OriginalPermutationDict, FactorList)
        
    
    # unittest.main()
