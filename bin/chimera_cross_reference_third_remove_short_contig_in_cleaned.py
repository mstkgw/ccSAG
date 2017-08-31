import itertools
import sys
import re

blastresult=open(sys.argv[1])
inputcontigs=open(sys.argv[2])
extractedcontigs=open(sys.argv[3],'w')
keepedcontigs=open(sys.argv[4],'w')
length_threshold=int(sys.argv[5])

contigkey={}
contigstart=re.compile(">")

for resultline in blastresult:
	data = []
        resultline = resultline.split("\t")
        if int(resultline[3]) < length_threshold:
		contigkey[resultline[0]]="k"
		continue
        queryname = resultline[0].split("_")
        if int(resultline[3]) > int(queryname[3]) - 100:
		contigkey[resultline[0]]="r"
		continue
	contigkey[resultline[0]]="e"

for line in inputcontigs:
	if contigstart.search(line):
		contigname = line
		for line in inputcontigs:
			data = contigname + line
			break
		if not contigname[1:-1] in contigkey:
			keepedcontigs.write(data)
                        continue
		if contigkey[contigname[1:-1]] == "k":
			keepedcontigs.write(data)
			continue
		elif contigkey[contigname[1:-1]] == "e":
			extractedcontigs.write(data)
			continue
		else:
			continue
