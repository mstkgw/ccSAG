import sys
import os
import re
import numpy as np

inpath = sys.argv[1] ## path of directory including sam
input_main = sys.argv[2] #${files[${A}]}

samfile = []
data = []
files = os.listdir(inpath)
reads = 0
for sam in files:
	if sam[0:len(input_main)] != input_main or sam[-18:] != "_uniq_classify.sam" : continue
	if reads == 0:
                for line in open(inpath + "/" + sam):
                        reads += 1
	data.append("")
	samfile.append(open(inpath + "/" + sam))

normal_file = open(inpath + "/" + input_main + "_normal.sam",'w')
chimera_file = open(inpath + "/" + input_main + "_chimera.sam",'w')
unjudge_file = open(inpath + "/" + input_main + "_unjudged.sam",'w')
normal_R1 = open(inpath + "/" + input_main + "_normal_R1_001.fastq",'w')
chimera_R1 = open(inpath + "/" + input_main + "_chimera_R1_001.fastq",'w')
unjudge_R1 = open(inpath + "/" + input_main + "_unjudged_R1_001.fastq",'w')
normal_R2 = open(inpath + "/" + input_main + "_normal_R2_001.fastq",'w')
chimera_R2 = open(inpath + "/" + input_main + "_chimera_R2_001.fastq",'w')
unjudge_R2 = open(inpath + "/" + input_main + "_unjudged_R2_001.fastq",'w')


softclip = re.compile("S")
i = 0
while i < int(reads):
	i = i + 1
	chimera = 0
	normal = 0
	unjudge = 0
	for j in range(len(data)):
		for line in samfile[j]:
			data[j] = line.strip("\n").split("\t")
			data[0].append(data[j][5])
			data[0].append(data[j][1])
			break
		if data[j][5] == '*': unjudge = unjudge + 1
		elif softclip.search(data[j][5]): chimera = chimera + 1
		else: normal = normal + 1
		mergesam = "\t".join(data[0])

	if normal > chimera and normal + chimera > 0:
		normal_file.write(mergesam + "\n")
		if i % 2 == 1:
			normal_R1.write("@" + data[0][0] + "\n" + data[0][9] + "\n" + '+' + "\n" + data[0][10] + "\n")
		else:
			normal_R2.write("@" + data[0][0] + "\n" + data[0][9] + "\n" + '+' + "\n" + data[0][10] + "\n")
	elif normal < chimera and normal + chimera > 0:
		chimera_file.write(mergesam + "\n")
		if i % 2 == 1:
			chimera_R1.write("@" + data[0][0] + "\n" + data[0][9] + "\n" + '+' + "\n" + data[0][10] + "\n")
		else:
			chimera_R2.write("@" + data[0][0] + "\n" + data[0][9] + "\n" + '+' + "\n" + data[0][10] + "\n")
	else: 
		unjudge_file.write(mergesam + "\n")
		if i % 2 == 1:
			unjudge_R1.write("@" + data[0][0] + "\n" + data[0][9] + "\n" + '+' + "\n" + data[0][10] + "\n")
		else:
			unjudge_R2.write("@" + data[0][0] + "\n" + data[0][9] + "\n" + '+' + "\n" + data[0][10] + "\n")
normal_file.close()
chimera_file.close()
unjudge_file.close()
normal_R1.close()
chimera_R1.close()
unjudge_R1.close()
normal_R2.close()
chimera_R2.close()
unjudge_R2.close()

#### cut chimera_read
before_cut = open(inpath + "/" + input_main + "_chimera.sam")
after_cut = open(inpath + "/" + input_main + "_cut_chimera.fastq",'w')
count = 0

for line in before_cut:
	count = count + 1
	line = line.strip("\n").split("\t")
	flag = []
	for i in range(len(data)*2):
		flag.append(line[i*(-1)-1])
	for i in range(len(data)):
		match = []
		k = 0
		for j in range(len(flag[(i*2)+1])):
			if k == j : continue
			if not flag[(i*2)+1][k:j+1].isdigit():
				match.append(flag[(i*2)+1][k:j+1])
				k = j + 1
		for j in range(len(match)-1):
			if match[j][-1:] != "S" and match[j+1][-1:] != "S":
				match[j+1] = str(int(match[j][0:(len(match[j])-1)]) + int(match[j+1][0:(len(match[j+1])-1)])) + "M"
				match[j] = "0"
		tmp = len(match)
		for j in range(len(match)):
			if match[tmp-1-j][0:1] == "0": match.pop(tmp-1-j)
		flag[(i*2)+1] = match

		flag[i*2] = str(bin(int(flag[i*2])))
		flag[i*2] = flag[i*2][2:][::-1]
	for i in range(len(data)):
		if flag[i*2][4] != flag[-2][4]:
			flag[(i*2)+1].reverse()
	double = []
	for i in range(len(data)):
		if len(flag[(i*2)+1]) == 0:
			double.append(0)
		else:
			double.append(flag.count(flag[(i*2)+1]))			
	cutpoint = flag[((np.argmax(double))*2)+1]

	j = 0
	for i in range(len(cutpoint)):
		if int(cutpoint[i][0:(len(cutpoint[i])-1)]) > 20:	
			after_cut.write("@" + line[0] + "_" + str(count%2) + str(i) + "\n" + line[9][j:j+(int(cutpoint[i][0:(len(cutpoint[i])-1)]))] + "\n" + '+' + "\n" + line[10][j:j+(int(cutpoint[i][0:(len(cutpoint[i])-1)]))] + "\n")
		j = int(cutpoint[i][0:(len(cutpoint[i])-1)])

before_cut.close()
after_cut.close()
