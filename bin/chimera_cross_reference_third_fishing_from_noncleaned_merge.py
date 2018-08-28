import itertools
import sys
import re

blastresult=open(sys.argv[1])
inputcontigs=open(sys.argv[2])
extractedcontigs=open(sys.argv[3],'w')
length_threshold=int(sys.argv[4])

a=0
contigkey=""
contigstart=re.compile(">")

for resultline in blastresult:
	resultline = resultline.split("\t")
	if int(resultline[3]) < length_threshold: continue
	queryname = resultline[0].split("_")
	if int(resultline[3]) > int(queryname[3]) - 100: continue
	resultkey = re.compile(resultline[0])
	if resultkey.search(contigkey):
		extractedcontigs.write(contigkey)
		for line in inputcontigs:
			if contigstart.search(line):
				contigkey = line
				break
			extractedcontigs.write(line)
	else:
		for line in inputcontigs:
			if resultkey.search(line):
				extractedcontigs.write(line)
				break
		for line in inputcontigs:
			if contigstart.search(line):
				contigkey = line
				break
			extractedcontigs.write(line)

blastresult.close()
inputcontigs.close()
extractedcontigs.close()
