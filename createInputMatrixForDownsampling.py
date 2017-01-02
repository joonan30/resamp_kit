#!/usr/bin/python

import argparse # parsing options
import math, random

# Get inputs from command line
parser = argparse.ArgumentParser()
parser.add_argument("inputFile", help="The input file with homozygous variants")
parser.add_argument("-i", "--iterations", help="The number of permuted files to create", action="store", default="10", type=int)
args = parser.parse_args()

# Open variants file
f = open(args.inputFile, 'rU')
headLine = f.readline()


# Columns with:
#familyCol = 0 # Family names
familyCol = headLine.split('\t').index('familyID')
#roleCol = 1 # Phenotype roles
roleCol = headLine.split('\t').index('role')

# Sort by family ID
sortF = sorted(f, key=lambda f: f.split()[familyCol])


# Create permuted files
baseName = args.inputFile
fileCountDict = {}
for fileCount in range(0,args.iterations):
    fileName = 'P_' + str(fileCount).zfill(5) + '_' + args.inputFile
    fileCountDict[fileCount] = fileName
    #print fileName
    fo = open(fileName, 'w')
    fo.write (headLine)
    fo.close ()

# Processes a family
def famPermute (famList):
    #print "New family"

    # Split by phenotype
    probandFamList = []
    siblingFamList = []
    for line in famList:
        line.rstrip()
        tab = line.split("\t")
        if tab[roleCol] == "P":
        	probandFamList.append(line.rstrip())
        elif tab[roleCol] == "S":
        	siblingFamList.append(line.rstrip())

    # Determine number of variants to pick
    lowerHalf = float(min(len(probandFamList),len(siblingFamList))) / 2
    numToPick = int(round(lowerHalf))
    #print len(probandFamList)
    #print len(siblingFamList)
    #print numToPick

    if numToPick > 0:
	    # Write output
	    for fileCount in range(0,args.iterations):
		    randVarPro = random.sample(probandFamList, numToPick)
		    randVarSib = random.sample(siblingFamList, numToPick)
		    fileName = fileCountDict[fileCount]
		    fo = open(fileName, 'a')
		    fo.write ("\n".join(randVarPro)+"\n")
		    fo.write ("\n".join(randVarSib)+"\n")
		    fo.close ()

# Go through variants file
# families = []
# with open(f) as fh:
#     for line in fh:
#         fID = line.split('\t')[familyCol]
#         if fID not in families:
#             families.append(fID)
#         else:
#             pass


lastFam = ''
tempVar = []
for line in sortF:
    line.rstrip()
    tab = line.split("\t")

    if tab[familyCol] == lastFam:
        tempVar.append(line)
        #print "Here"
    else:
        famPermute(tempVar)
        del tempVar[:]
        lastFam = tab[familyCol]
        #print "There"

# Process last family
famPermute(tempVar)
