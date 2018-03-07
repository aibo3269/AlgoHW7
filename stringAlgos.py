#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Aidan
"""

import random

class Matrix(object):
	def __init__(self, n, m):
		#Init1ialize n x m matrix with all zeros
		self.matrix = []
		i = 0
		j = 0
		while (i < n):
			j = 0
			newrow = []
			while (j < m):
				newrow.append(0)
				j += 1
			self.matrix.append(newrow)
			i += 1

	#Return string version of row array if print is called on the object
	def __repr__(self):
		return str(self.matrix)

	def rowlength(self):
		return len(self.matrix[0])

	def columnlength(self):
		return len(self.matrix)

	#Change a specified array element with a specified value
	def editentry(self, row, column, newentry):
		self.matrix[row][column] = newentry

	#Return a specific value from the matrix
	def getentry(self, row, column):
		return self.matrix[row][column]

	def printmatrix(self):
		rowstring = ""
		for row in self.matrix:
			rowstring = ""
			for entry  in row:
				rowstring += '{:{align}{width}}'.format(str(entry), align='^', width='3')
			print(rowstring)




def determineOptimalOp(S, i, j, x, y):
	#This method works backwards starting from the endpoint to find the optimal solution
	#Check if the op is not sub
	if((S.getentry(i,j) - S.getentry(i-1, j-1)) < 12):
		cheapests = []
		if(S.getentry(i,j) == S.getentry(i-1, j-1)):
			cheapest = min(S.getentry(i,j), S.getentry(i-1,j),S.getentry(i, j-1))
			if(S.getentry(i-1, j) == cheapest):
				cheapests.append("Delete " + x[i-1] + " from x")
			if(S.getentry(i, j-1) == cheapest):
				cheapests.append("Insert " + y[j-1] + " into x")
			if(S.getentry(i-1, j-1) == cheapest):
				cheapests.append("no-op")
		else:
			cheapest = min(S.getentry(i-1, j), S.getentry(i, j-1))
			if(S.getentry(i-1, j) == cheapest):
				cheapests.append("Delete " + x[i-1] + " from x")
			if(S.getentry(i, j-1) == cheapest):
				cheapests.append("Insert " + y[j-1] + " into x")
		if(len(cheapests) == 3):
			return "no-op"
		else:
			rand = random.randint(0,len(cheapests)-1)
			return cheapests[rand]
	#If sub is the cheapest op
	else:
		return "Sub " + x[i-1] + " with " + y[j-1]


def alignStrings(x, y):
	print(len(x),len(y))
	S = Matrix(len(x)+1, len(y)+1)
	#Initialize entries in first row
	i = 1
	print(S.rowlength(),S.columnlength())
	while (i < S.rowlength()):
		S.editentry(0, i, i)
		i += 1
	#Initialize entries in first column
	i = 1
	while (i < S.columnlength()):
		S.editentry(i, 0, i)
		i += 1
	#Determine the cost for aligning all substrings
	i = 1
	j = 1
	while (i < S.columnlength()):
		j = 1
		while (j < S.rowlength()):
			#If no-op
			if (x[i-1] == y[j-1]):          
			#Set entry i,j to the minimum cost of any op but swap
				S.editentry(i, j, min(S.getentry(i-1, j), S.getentry(i, j-1), S.getentry(i-1, j-1)))
			else:
				#If swap is possible
				if (i >= 2 and j >= 2):
					#Set entry i,j to the minimum cost of all possible ops
					S.editentry(i, j, min(S.getentry(i-2, j-2) + 37, S.getentry(i-1, j) + 1, S.getentry(i, j-1) + 1, S.getentry(i-1, j-1) + 12))
				#If swap is not possible
				else:
					#Set entry i,j to the minimum cost of any op but swap
					S.editentry(i, j, min(S.getentry(i-1, j) + 1,  S.getentry(i, j-1) + 1, S.getentry(i-1, j-1) + 12))
			j += 1
		i += 1
	return S


def extractAlignment(S, x, y):
	a = []
	i = len(x)
	j = len(y)
	while(i > 0 or j > 0):
		a.insert(0, determineOptimalOp(S, i, j, x, y))
		if(a[0][:6] == "Insert"):
			j -= 1
		elif(a[0][:6] == "Delete"):
			i -= 1
		else:
			i -= 1
			j -= 1
	return a

def commonSubstrings(x, L, a):
	substrings = []
	substring = ""
	i = 0
	for op in a:
		if(op[:6] != "Insert"):
			if(op == "no-op"):
				substring += x[i]
				i += 1
			else:
				if(len(substring) >= L):
					substrings.append(substring)
				substring = ""
				i += 1
		else:
			if(len(substring) >= L):
				substrings.append(substring)
			substring = ""
	if(substring != ""):
		substrings.append(substring)
	return substrings
file1 = open("string_x.txt", "r")
file2 = open("string_y.txt", "r")
file1lines = file1.readlines()
file2lines = file2.readlines()
x = "".join(file1lines)[:-1]
print(x)
y = "".join(file2lines)[:-1]
print(y)
S = alignStrings(x, y)
print(S)
a = extractAlignment(S, x, y)
print(a)
m = commonSubstrings(x, 10 ,a)
