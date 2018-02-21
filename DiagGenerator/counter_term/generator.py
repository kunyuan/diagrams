#!/usr/bin/env python
import numpy as np
import unittest
import unionfind
import random
import IO
from nullspace import rank, nullspace

Nmax=1e8

def GetVerList(Order):
#there are 2*Order vertexes
    return range(2*Order)

def GetInteractionPairs(Order):
    return [(2*i,2*i+1) for i in range(Order)]

def GetReference(Order):
    return range(2*Order)

def swap(array, i, j):
    array = list(array)
    array[i], array[j] = array[j], array[i]
    return tuple(array)

def IsConnected(permutation, reference, InteractionPairs):
    diagram=set(InteractionPairs)
    for i in range(len(permutation)):
        diagram.add((reference[i], permutation[i]))

    n_node = len(InteractionPairs)*2
    diagram_union = unionfind.UnionFind(n_node)

    for edge in diagram:
        if edge[0]!=edge[1] and not diagram_union.is_connected(edge[0], edge[1]):
            diagram_union.union(edge[0], edge[1])
    return diagram_union.get_n_circles() == 1

def HasTadpole(permutation, reference):
    for i in range(len(permutation)):
        if reference[i]==permutation[i]:
            return True
    return False

def HasBuble(permutation, reference):
    for i in range(len(reference)):
        # end=reference[i]
        end=permutation[permutation[i]]
        if i==end and i!=0 and permutation[i]!=0:
            return True
    return False

def HasFock(permutation, reference):
    for i in range(len(reference)):
        # end=reference[i]
        end=permutation[i]
        if abs(i-end)==1 and min(i, end)%2==0:
            return True
    return False

def FindIndependentK(permutation, reference, InteractionPairs):
    # kList=[(random.randint(0, Nmax), random.randint(0,Nmax)) for i in range(len(InteractionPairs)+1)]
    N=len(InteractionPairs)
    Matrix=np.zeros((2*N,3*N))
    for i in range(2*N):
        interaction=int(i/2)+2*N
        sign=i%2
        Matrix[i,interaction]=-(-1)**sign
        Matrix[i, i]=-1
        Matrix[i, permutation.index(i)]=1
    # print Matrix
    vectors = nullspace(Matrix)
    # print len(vectors)
    # print vectors
    freedoms=vectors.shape[1]
    if freedoms!=N+1:
        print "Warning! Rank is wrong for {0} with \n{1}".format(permutation, vectors)
    return vectors

def AssignMomentums(permutation, reference, InteractionPairs):
    N=len(InteractionPairs)
    vectors=FindIndependentK(permutation, reference, InteractionPairs)
    freedoms=vectors.shape[1]
    karray=np.array([random.random() for _ in range(freedoms)])
    kVector=np.dot(vectors, karray)
    # kVector=vectors[:,0]
    return kVector[:2*N], kVector[2*N:]

def GetAllPermutations(Order):
    reference=GetReference(Order)

    InteractionPairs=GetInteractionPairs(Order)
    permutations = [tuple(reference)]
    fermi_sign = {tuple(reference): 1}

    idx = 1
    while idx < 2*Order:
        print "Index {0}".format(idx)
        for i in range(len(permutations)):
            for j in range(idx):
                permutations.append(swap(permutations[i], idx, j))
                fermi_sign[permutations[-1]] = fermi_sign[permutations[i]]*-1
        idx += 1

    # print "Check buble"
    # permutations=[p for p in permutations if not HasBuble(p, reference)]
    # print "Check connectivity"
    # permutations=[p for p in permutations if IsConnected(p, reference, InteractionPairs)]

    permutation_dict={}
    fermi_sign_dict = {}
    for p in permutations:
        permutation_dict[tuple(p)]=None

    print "Diagram Number: {0}".format(len(permutations))
    print "Check Tadpole..."
    for p in permutation_dict.keys():
        if HasTadpole(p, reference):
            del permutation_dict[p]
            del fermi_sign[p]

    # print "Diagram Number: {0}".format(len(permutation_dict))
    # print "Check Buble"
    # for p in permutation_dict.keys():
        # if HasBuble(p, reference):
            # del permutation_dict[p]
            # del fermi_sign[p]

    print "Diagram Number: {0}".format(len(permutation_dict))
    print "Check connectivity"
    for p in permutation_dict.keys():
        if not IsConnected(p, reference, InteractionPairs):
            del permutation_dict[p]
            del fermi_sign[p]

    print "Diagram Number: {0}".format(len(permutation_dict))

    return permutation_dict.keys(), permutation_dict, fermi_sign

def swap_interaction(permutation, m, n, k, l):
    permutation = list(permutation)
    mp,np,kp,lp=(permutation.index(e) for e in (m,n,k,l))
    permutation[mp]=k
    permutation[kp]=m
    permutation[np]=l
    permutation[lp]=n
    permutation[m],permutation[k]=permutation[k],permutation[m]
    permutation[n],permutation[l]=permutation[l],permutation[n]
    return tuple(permutation)

def swap_LR(permutation, i, j):
    permutation = list(permutation)
    ip,jp=permutation.index(i),permutation.index(j)
    permutation[ip]=j
    permutation[jp]=i
    permutation[i],permutation[j]=permutation[j],permutation[i]
    return tuple(permutation)

def check_Unique_Permutation(permutation, InteractionPairs, PermutationDict):
    measure_in=0
    Order = len(InteractionPairs)
    Deformation = [permutation]
    for idx in range(1, Order):
        if idx==measure_in:
            continue
        for i in range(len(Deformation)):
            for j in range(idx):
                if j==measure_in:
                    continue
                Deformation.append(swap_interaction(Deformation[i], idx*2, idx*2+1, j*2, j*2+1))

    for idx in range(Order):
        if idx==measure_in:
            continue
        for i in range(len(Deformation)):
            Deformation.append(swap_LR(Deformation[i], idx*2, idx*2+1))

    Deformation = set(Deformation)
    for p in Deformation:
        if p in PermutationDict:
            del PermutationDict[p]

    print "remaining length of permutation dictionary:", len(PermutationDict)
    return list(Deformation)

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
        Deformation=check_Unique_Permutation(permutation, InteractionPairs, PermutationDict)
        # if len(Deformation)>0:
        UnlabeledDiagramList.append(Deformation)
        # if permutation==(0,1,3,2):
            # print "working", Deformation
        # FactorList.append(Factor)
    return UnlabeledDiagramList


def RemoveReducibleGW(InteractionPairs, PermutationDict):
    UnlabeledDiagramList =  Group(InteractionPairs, PermutationDict)
    print "Total Unique Diagrams {0}\n".format(len(UnlabeledDiagramList))
    TempList=UnlabeledDiagramList[:]
    for g in TempList:
        p=g[0]
        kG, kW=AssignMomentums(p, Reference, InteractionPairs)
        Flag=True
        for i in range(len(kW)):
            if Flag and abs(kW[i])<1e-12:
                # print "k=0 on W {0}: {1}".format(p, kW[i])
                UnlabeledDiagramList.remove(g)
                Flag=False
                break

        for i in range(len(kW)):
            for j in range(i+1,len(kW)):
                if Flag and abs(abs(kW[i])-abs(kW[j]))<1e-12:
                    # print "Same k on W for {0}: {1} on {2}; {3} on {4}".format(p, kW[i],i,kW[j],j)
                    UnlabeledDiagramList.remove(g)
                    Flag=False
                    break

        for i in range(0,len(kG)):
            for j in range(i+1,len(kG)):
                if Flag and abs(kG[i]-kG[j])<1e-12:
                    # print "Same k on G for {0}: {1} on {2}; {3} on {4}".format(p, kG[i],i,kG[j],j)
                    # print "Same k on W for {0}: {1}; 1, {2}".format(p, kG[i],kG[j])
                    UnlabeledDiagramList.remove(g)
                    Flag=False
                    # print "Flag",Flag
                    break
    return UnlabeledDiagramList

def RemoveReducibleG_HF_V(InteractionPairs, PermutationDict):
    UnlabeledDiagramList =  Group(InteractionPairs, PermutationDict)
    print "Total Unique Diagrams {0}\n".format(len(UnlabeledDiagramList))
    TempList=UnlabeledDiagramList[:]
    UnlabeledBubleDiagramList=[]
    for g in TempList:
        if HasFock(g[0], Reference):
            UnlabeledDiagramList.remove(g)
        else:
            if HasBuble(g[0], Reference):
                UnlabeledBubleDiagramList.append(g[0])
            else:
                print "NoBuble", g[0]
    return UnlabeledDiagramList, UnlabeledBubleDiagramList

def DrawDiagrams(Reference, InteractionPairs, PermutationList, NumberList=[]):
    i=0
    print PermutationList
    for permutation in PermutationList:
        i+=1
        with open("./diagram/{0}.gv".format(i), "w") as f: 
            f.write("digraph Feynman{\nnode [margin=0.1 fillcolor=grey fontcolor=black fontsize=10 width=0.2 shape=circle style=filled fixedsize=true];\n//nVer\n")
            if len(NumberList)==len(PermutationList):
                f.write("//Diagram Number: {0}\n".format(NumberList[i-1]))
            for n in Reference:
                f.write("{0} [fillcolor=grey];\n".format(n))
            f.write("//GLine\n")
            for n in range(len(Reference)):
                if n==0:
                    f.write("{0}->{1} [color=\"red\"];\n".format(Reference[n],permutation[n]))
                else:
                    f.write("{0}->{1} [color=\"blue\"];\n".format(Reference[n],permutation[n]))


            f.write("//WLine\n")
            for p in InteractionPairs:
                f.write("{0}->{1} [style=dashed arrowhead=none];\n".format(p[0],p[1]))
            f.write("}\n")
        f.close()

def SaveSigmaDiagrams(MxOrder, filename):
    Diagrams = {}
    for Order in range(1, MxOrder+1):
        Reference=GetReference(Order)
        InteractionPairs=GetInteractionPairs(Order)
        Permutations, PermutationDict, FermiSignDict = GetAllPermutations(Order)
        IrreducibleDiagrams = RemoveReducibleGW(InteractionPairs, PermutationDict)
        IrreducibleDiagrams = [item for sublist in IrreducibleDiagrams for item in sublist]

        Permutations = []
        FermiSigns = []
        for permu in IrreducibleDiagrams:
            Permutations.append(list(permu))
            FermiSigns.append(FermiSignDict[permu])
        Diagrams[str(Order)] = {"Permutations": Permutations, "FermiSigns": FermiSigns}
        print "Order ", Order, len(Permutations)
        
    Sigma = {"Sigma": Diagrams}
    IO.SaveDict(filename, "w", Sigma)

def SavePolarDiagrams(MxOrder, filename):
    Diagrams = {}
    for Order in range(1, MxOrder+1):
        Reference=GetReference(Order)
        InteractionPairs=GetInteractionPairs(Order)
        Permutations, PermutationDict, FermiSignDict = GetAllPermutations(Order)
        IrreducibleDiagrams = RemoveReducibleGW(InteractionPairs, PermutationDict)
        IrreducibleDiagrams = [item for sublist in IrreducibleDiagrams for item in sublist]

        Permutations = []
        FermiSigns = []
        for permu in IrreducibleDiagrams:
            Permutations.append(list(permu))
            FermiSigns.append(FermiSignDict[permu])
        Diagrams[str(Order)] = {"Permutations": Permutations, "FermiSigns": FermiSigns}
        
    Polar = {"Polar": Diagrams}
    IO.SaveDict(filename, "w", Polar)


class Test(unittest.TestCase):
 
    def setUp(self):
        pass
 
    def test_InteractionPairs(self):
        self.assertEqual(GetInteractionPairs(3), [(0,1),(2,3),(4,5)])

    # def test_Permutation(self):
        # self.assertEqual(GetAllPermutations(1)[0], [(0,1), (1,0)])
        # self.assertEqual(len(GetAllPermutations(2)[0]), 24) 
        # self.assertEqual((1,0,2,3) in GetAllPermutations(2)[0], True)
        # self.assertEqual(len(set(GetAllPermutations(2)[0])), 24)
        # self.assertEqual(len(set(GetAllPermutations(3)[0])), 720)
        # self.assertEqual(len(set(GetAllPermutations(5))), 3628800)

    def test_Momentum_3(self):
        Order=3
        InteractionPairs=GetInteractionPairs(Order)
        reference=GetReference(Order)
        permutation=[2,4,1,0,5,3]
        kG,kW=AssignMomentums(permutation, reference, InteractionPairs)
        print kG, kW
        self.assertTrue(abs(kG[1]-kG[5])<1e-13)
        self.assertTrue(abs(-kG[0]+kG[3]-kW[0])<1e-13)
        for i in range(Order*2):
            print "Check Ver {0}".format(i)
            self.assertTrue(abs(-kG[i]+kG[permutation.index(i)]-(-1)**(i%2)*kW[int(i/2)])<1e-13)

    def test_Momentum_5(self):
        Order=5
        InteractionPairs=GetInteractionPairs(Order)
        reference=GetReference(Order)
        permutation=[2,4,1,7,5,8,9,0,6,3]
        kG,kW=AssignMomentums(permutation, reference, InteractionPairs)
        print kG, kW
        self.assertTrue(abs(kG[1]-kG[5])<1e-13)
        for i in range(Order*2):
            print "Check Ver {0}".format(i)
            self.assertTrue(abs(-kG[i]+kG[permutation.index(i)]-(-1)**(i%2)*kW[int(i/2)])<1e-13)
 
if __name__ == '__main__':
    Order=5
    Reference=GetReference(Order)
    InteractionPairs=GetInteractionPairs(Order)
    PermutationList, PermutationDict, FermiSignDict = GetAllPermutations(Order)

    # print PermutationList
    # DrawDiagrams(Reference, InteractionPairs, PermutationList)
    # UnlabeledDiagramList = RemoveReducibleGW(InteractionPairs, PermutationDict)
    UnlabeledDiagramList, UnlabeledBubleDiagramList = RemoveReducibleG_HF_V(InteractionPairs, PermutationDict)

    UniqueDiagrams=[]
    print "Total Unique Diagrams for Sigma:  {0}\n".format(len(UnlabeledDiagramList))
    print "Total Unique Buble Diagrams for Sigma: {0}\n".format(len(UnlabeledBubleDiagramList))
    for g in UnlabeledDiagramList:
        # print g[0]
        # for e in g:
            # print "{0}".format(e)
        #print "Total {0}\n".format(len(g))
        UniqueDiagrams.append(g[0])

    for g in UnlabeledBubleDiagramList:
        print g

    # print UniqueDiagrams
    # DrawDiagrams(Reference, InteractionPairs, UniqueDiagrams)
    
    FactorList = [len(p) for p in UnlabeledDiagramList]
    DrawDiagrams(Reference, InteractionPairs, UniqueDiagrams, FactorList)

    # SaveSigmaDiagrams(2, filename="Sigma_Fermi_loops.dig")
    # SavePolarDiagrams(2, filename="Polar_Fermi_loops.dig")
    # unittest.main()
