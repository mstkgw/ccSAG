import sys
import re

blastresult=open(sys.argv[1])
uniqblastresult=open(sys.argv[2],'w')
length_threshold=int(sys.argv[3])
check_partial_mapping=sys.argv[4] # on/off

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


previous_node=""
preuniq_data=[]
i = -1

for line in blastresult:
        result = line.split("\t")
	if result[0] == previous_node:
		if int(result[3]) < length_threshold: continue
		preuniq_data[i].append(line)
	else:
		i = i + 1
		preuniq_data.append([line])
		previous_node=result[0]


for data in preuniq_data:
	if len(data) == 1:
		if check_partial_mapping == "on":
			judge = Check_partially_alignment(data[0])
			if judge == "remove":
				continue
		uniqblastresult.write(data[0])
	else:
		query_map_position=[]
		ref_map_position=[]
		for i in range(len(data)):
			tmpdata = data[i].split("\t")
			query_map_position.append(int(tmpdata[6]))
			query_map_position.append(int(tmpdata[7]))
                        ref_map_position.append(int(tmpdata[8]))
                        ref_map_position.append(int(tmpdata[9]))
		merged_data = data[0].split("\t")
		merged_data[6] = str(min(query_map_position))
		merged_data[7] = str(max(query_map_position))
		merged_data[8] = str(ref_map_position[query_map_position.index(min(query_map_position))])
		merged_data[9] = str(ref_map_position[query_map_position.index(max(query_map_position))])
		merged_data[3] = str(max(query_map_position) - min(query_map_position) + 1)
		merged_data = "\t".join(merged_data)
                if check_partial_mapping == "on":
                        judge = Check_partially_alignment(merged_data)
                        if judge == "remove":
                                continue
                uniqblastresult.write(merged_data)
