import sys
import re

blastresult=sys.argv[1]
inputcleaned=sys.argv[2]
inputfished=sys.argv[3]
output=open(sys.argv[4],'w')
length_threshold=int(sys.argv[5])

def Get_contig(inputfile,contigname):
	infile = open(inputfile)
	name = re.compile(contigname)
	for line in infile:
		if name.search(line):
			break
	for line in infile:
		contig = line.rstrip()
		break
	infile.close()
	return contig

def Make_howto_connect_first(blastresult):
        howto_connect = []
        data = blastresult
        cleaned = data[0].split("_")
        fished = data[1].split("_")
        if int(data[6]) - 1 > int(cleaned[3]) - int(data[7]):
                howto = []
                howto = howto + [data[0]] + ["1"] + [cleaned[3]] + ["normal"] + ["cleaned"]
                howto_connect.append(howto)
                if int(data[8]) < int(data[9]):
			if int(data[9])+1+(int(cleaned[3])-int(data[7])) < 0: return 0
                        howto = []
                        howto = howto + [data[1]] + [str(int(data[9])+1+(int(cleaned[3])-int(data[7])))] + [fished[3]] + ["normal"] + ["fished"]
                        howto_connect.append(howto)
                else:
			if int(data[9])-1-(int(cleaned[3])-int(data[7])) < 0: return 0
                        howto = []
                        howto = howto + [data[1]] + ["1"] + [str(int(data[9])-1-(int(cleaned[3])-int(data[7])))] + ["rev"] + ["fished"]
                        howto_connect.append(howto)
        else:
                if int(data[8]) < int(data[9]):
			if int(data[8])-int(data[6]) < 0: return 0
                        howto = []
                        howto = howto + [data[1]] + ["1"] + [str(int(data[8])-int(data[6]))] + ["normal"] + ["fished"]
                        howto_connect.append(howto)
                else:
			if int(data[8])+int(data[6]) < 0: return 0
                        howto = []
                        howto = howto + [data[1]] + [str(int(data[8])+int(data[6]))] + [fished[3]] + ["rev"] + ["fished"]
                        howto_connect.append(howto)
                howto = []
                howto = howto + [data[0]] + ["1"] + [cleaned[3]] + ["normal"] + ["cleaned"]
                howto_connect.append(howto)
	return howto_connect


def Make_howto_connect_second(processed, pre_processed):
	if processed[0][0] == pre_processed[0][0]:
		if processed[0][3] == pre_processed[0][3]:
			print("error:\nprocessed: " + str(processed) + "\npre_processed: " + str(pre_processed))
			return ""
		reverse = [pre_processed[1],pre_processed[0]]
		if reverse[0][3] == "normal": reverse[0][3] = "rev"
		elif reverse[0][3] == "rev": reverse[0][3] = "normal"
		if reverse[1][3] == "normal": reverse[1][3] = "rev"
                elif reverse[1][3] == "rev": reverse[1][3] = "normal"
		pre_processed = reverse
        elif processed[-1][0] == pre_processed[1][0]:
		if processed[-1][3] == pre_processed[1][3]:
                        print("error:\nprocessed: " + str(processed) + "\npre_processed: " + str(pre_processed))
                        return ""
		reverse = [pre_processed[1],pre_processed[0]]
                if reverse[0][3] == "normal": reverse[0][3] = "rev"
                elif reverse[0][3] == "rev": reverse[0][3] = "normal"
                if reverse[1][3] == "normal": reverse[1][3] = "rev"
                elif reverse[1][3] == "rev": reverse[1][3] = "normal"
                pre_processed = reverse

	if processed[0][0] == pre_processed[1][0]:
                if pre_processed[1][4] == "cleaned":
			return_data = [pre_processed[0]] + processed
			return return_data
                elif pre_processed[1][4] == "fished":
			if processed[0][3] != pre_processed[1][3]:
				print("error:\nprocessed: " + str(processed) + "\npre_processed: " + str(pre_processed))
				return ""
			if processed[0][3] == "normal":
				if int(processed[0][2]) >= int(pre_processed[1][1]):
					processed[0][1] = pre_processed[1][1]
					return_data = [pre_processed[0]] + processed
					return return_data
				else: 
					processed[1][1] = str(int(pre_processed[1][1])-int(processed[0][2]))
					del processed[0]
					return_data  = [pre_processed[0]] + processed
                                        return return_data
			if processed[0][3] == "rev":
				if int(processed[0][1]) <= int(pre_processed[1][2]):
                                        processed[0][2] = pre_processed[1][2]
                                        return_data = [pre_processed[0]] + processed
                                        return return_data
                                else:
                                        processed[1][1] = str(int(processed[0][1])-int(pre_processed[1][2]))
                                        del processed[0]
                                        return_data  = [pre_processed[0]] + processed
                                        return return_data					
	elif processed[-1][0] == pre_processed[0][0]:
                if pre_processed[0][4] == "cleaned":
			return_data = processed + [pre_processed[1]]
			return return_data
                elif pre_processed[0][4] == "fished":
			if processed[-1][3] != pre_processed[0][3]:
				print("error:\nprocessed: " + str(processed) + "\npre_processed: " + str(pre_processed))
				return ""
			if processed[-1][3] == "normal":
				if int(processed[-1][1]) <= int(pre_processed[0][2]):
					processed[-1][2] = pre_processed[0][2]
					return_data = processed + [pre_processed[1]]
					return return_data
				else:
					pre_processed[1][1] = str(int(processed[-1][1])-int(pre_processed[0][2]))
					del processed[-1]
					return_data = processed + [pre_processed[1]]
					return return_data
			if processed[-1][3] == "rev":
				if int(processed[-1][2]) >= int(pre_processed[0][1]):
					processed[-1][1] = pre_processed[0][1]
					return_data = processed + [pre_processed[1]]
					return return_data
				else:
					pre_processed[1][1] = str(int(pre_processed[0][1])-int(processed[-1][2]))
					del processed[-1]
                                        return_data = processed + [pre_processed[1]]
                                        return return_data

def Check_partially_alignment(inputdata):
        data = inputdata.split("\t")
        query = data[0].split("_")
        ref = data[1].split("_")
        left_ribbon = int(data[6]) - 1
        right_ribbon = int(query[3]) - int(data[7])
        if left_ribbon >= 150:
                if int(data[8]) < int(data[9]):
                        if int(data[8]) - left_ribbon > 0 or int(data[8]) > int(ref[3]) - int(data[9]): return "remove"
                else:
                        if int(data[8]) + left_ribbon < int(ref[3]) or int(ref[3]) - int(data[8]) > int(data[9]): return "remove"
        if right_ribbon >= 150:
                if int(data[8]) < int(data[9]):
                        if int(data[9]) + right_ribbon < int(ref[3]) or int(ref[3]) - int(data[9]) > int(data[8]): return "remove"
                else:
                        if int(data[9]) - right_ribbon > 0 or int(data[9]) > int(ref[3]) - int(data[8]): return "remove"
        return "clear"

switch=""
preuniq_data=[]
used_cleaned=[]
used_fished=[]
partially_aligned=[]
blastfile = open(blastresult)
for line in blastfile:
        result = line.split("\t")
        if int(result[3]) < length_threshold: continue
	judge = Check_partially_alignment(line)
        if judge == "remove":
                partially_aligned.append(result[1])
                continue
blastfile.close()
blastfile = open(blastresult)
for line in blastfile:
        result = line.split("\t")
	if int(result[3]) < length_threshold: continue
	used_fished.append(result[1])
	for data in partially_aligned:
		if data == result[1]:
			switch = "off"
			break
		switch = "on"
	if switch == "off": continue
	used_cleaned.append(result[0])
	preuniq_data.append(result)
blastfile.close()
used_cleaned = list(set(used_cleaned))
used_fished = list(set(used_fished))


cleanedfile = open(inputcleaned)
for line in cleanedfile:
        if line[0:1] == ">":
                for data in used_cleaned:
                        if data == line.rstrip()[1:]:
                                switch = "off"
                                break
                        switch = "on"
                if switch == "on":
                        output.write(line)
                        for line in cleanedfile:
                                output.write(line)
                                break
cleanedfile.close()

connection_list = []
while len(preuniq_data) >= 1:
	search_list = []
	searched_list = []
	search_list.append(preuniq_data[0][0])
	search_list.append(preuniq_data[0][1])
	searched_list.append(0)
	while len(search_list) > 0:
		count = -1
		for data in preuniq_data:
			count = count + 1
			if data[0] == search_list[0]:
				for j in range(len(searched_list)):
					if searched_list[j] == count:
						switch = "off"
						break
					switch = "on"
				if switch == "off": continue
				searched_list.append(count)
				search_list.append(data[1])
			elif data[1] == search_list[0]:
				for j in range(len(searched_list)):
                                        if searched_list[j] == count:
                                                switch = "off"
                                                break
                                        switch = "on"
                                if switch == "off": continue
                                searched_list.append(count)
                                search_list.append(data[0])
		del search_list[0]
	searched_list.sort()
	searched_list.reverse()
	connection_group = []
	for k in range(len(searched_list)):
		connection_group.append(preuniq_data[searched_list[k]])
		del preuniq_data[searched_list[k]]
	connection_list.append(connection_group)

pre_howto_connect_list=[]
for data in connection_list:
	howto_connect = []
	for i in range(len(data)):
		howto = Make_howto_connect_first(data[i])
		if howto != 0: howto_connect.append(howto)
	if len(howto_connect) > 0: pre_howto_connect_list.append(howto_connect)

howto_connect_list=[]
for data in pre_howto_connect_list:
	if len(data) == 1: howto_connect_list.append(data[0])
	else:
		processed = data[0]
		del data[0]
		while len(data) > 0:
			for i in range(len(data)):
				if len(set([processed[0][0], processed[-1][0], data[i][0][0], data[i][1][0]])) != 3: continue
				pre_processed = data[i]
				del data[i]
				processed = Make_howto_connect_second(processed, pre_processed)
				break
		if processed != "": howto_connect_list.append(processed)

count = 0
for data in howto_connect_list:
	print(data)
	count = count + 1
	name = ">CONSENSUS_" + str(count)
	consensus= ""
	for i in range(len(data)):
		contigname = data[i][0]
		changedname = contigname.split("_")
		changedname = changedname[0] + "_" + changedname[1] + "_" + data[i][4]
		name = name + "_" + changedname
		if data[i][4] == "cleaned":
			sequence = Get_contig(inputcleaned,contigname)
		elif data[i][4] == "fished":
			sequence = Get_contig(inputfished,contigname)
		sequence = sequence[int(data[i][1])-1:int(data[i][2])]
		if data[i][3] == "rev":
			sequence = sequence[::-1]
			my_dictionary = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
			sequence = "".join([my_dictionary[base] for base in sequence])
		consensus = consensus + sequence
	output.write(name + "\n" + consensus + "\n")

fishedfile = open(inputfished)
for line in fishedfile:
	if line[0:1] == ">":
		for data in used_fished:
			if data == line.rstrip()[1:]:
				switch = "off"
				break
			switch = "on"
		if switch == "on":
			count = count + 1
			output.write(">CONSENSUS_" + str(count) + "\n")
			for line in fishedfile:
				output.write(line)
				break
fishedfile.close()
print("finished")
