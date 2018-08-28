import os
import sys
import argparse

#
# Argument
#
parser = argparse.ArgumentParser()
parser.add_argument("-i",dest="inf",action="store",default=".",help="Path for input file")
parser.add_argument("-o",dest="outf",action="store",default=".",help="Path for output file")
args = parser.parse_args()

##################
# Files
##################
#if args.inf != "none" and args.outf != "none":
#	try:
#		fi = open(args.inf)
#		fo = open(args.outf,"w")
#	except IOError:
#		print("Cannot recognize the filenames")
#	files = []
#else:
#	print("Please enter path for input/output files")
#	sys.exit()

total_num = 0
pair_num = 0
proper_pair = 0
chimera_reads = 0
unmapped_reads = 0
flag2num = dict()
flag2num_all = dict()
for ii,jj in enumerate(fi):
	if jj[0] =="@":
		fo.write(jj)
		continue
	data = jj.strip("\n").split("\t")
	flag = int(data[1])
	flag_bin = str(bin(flag))
	flag_bin2 = flag_bin[2:][::-1]
	#
	flags = []
	for i in range(len(flag_bin2)):
		if flag_bin2[i] == "1": flags.append(i+1)
	#
	total_num += 1
	if 1 in flags and 7 in flags:
		if flag_bin2 in flag2num_all: flag2num_all[flag_bin2] += 1
		else: flag2num_all[flag_bin2] = 1
		#
		pair_num += 1
		if 2 in flags:
			proper_pair += 1
			#print data[0] + "\t" + data[1]
		else:
			if flag_bin2 in flag2num: flag2num[flag_bin2] += 1
			else: flag2num[flag_bin2] = 1
	if 3 in flags:
		unmapped_reads += 1
	if not 12 in flags:
		chimera_reads += 1
		fo.write(jj)
fi.close()
#
#fo.write("Total read number\t" + str(total_num) + "\n")
#fo.write("Number of unmepped reads\t" + str(unmapped_reads) + "\n")
#fo.write("Number of chimeric reads\t" + str(chimera_reads) + "\n\n")
#fo.write("Number of pairs\t" + str(pair_num) + "\n")
#fo.write("Number of proper pairs\t" + str(proper_pair) + "\n")
#fo.write("not proper pairs\n")
#for flag in flag2num.keys(): fo.write(flag + "\t" + str(flag2num[flag]) + "\n")
#fo.write("\nall\n")
#for flag in flag2num_all.keys(): fo.write(flag + "\t" + str(flag2num_all[flag]) + "\n")
#fo.close()
