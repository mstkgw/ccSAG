import itertools
import sys
import re

inputcontigs=open(sys.argv[1])
extractedcontigs=open(sys.argv[2],'w')
length_threshold=int(sys.argv[3])

seqlen = 0
for line in inputcontigs:
	if line[0:1] == ">":
		if seqlen > 0 and seqlen >= int(length_threshold): extractedcontigs.write(data + "\n")
		data = line
		seqlen = 0
		continue
	data = data + line.rstrip()
	seqlen = seqlen + len(line.rstrip())
if seqlen >= int(length_threshold): extractedcontigs.write(data + "\n")
