#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import numpy as np
import unittest
import unionfind
import random
from nullspace import rank, nullspace
Nmax=1e8

def CheckSpinConserved(permutation, spin):
    ### The spins should satisfy conservation at each interaction line

    Order = len(permutation)/2
    for i in range(Order):
        left, right = i*2, i*2+1
        leftin = permutation.index(left)
        rightin = permutation.index(right)
        if spin[leftin] + spin[rightin] - spin[left] - spin[right] != 0:
            return False
    return True

def GetSpins(permutation):
    size = len(permutation)

    ## Get all the 2^n possible spin configurations
    SpinLists = [tuple([0 for i in range(size)])]
    for pivot in range(size):
        for i in range(len(SpinLists)):
            newspins = list(SpinLists[i])
            newspins[pivot] = 1
            SpinLists.append(tuple(newspins))

    ## Get all the spin configuration that satisfies conservation law
    SpinLists = [spin for spin in SpinLists if CheckSpinConserved(permutation, spin)]

    return SpinLists

if __name__ == '__main__':
    GetSpins((1,3,0,5,2,4))
