import sys

input_R1=open(sys.argv[1])
input_R2=open(sys.argv[2])
output_R1=open(sys.argv[3],'w')
output_R2=open(sys.argv[4],'w')

count = 0
R1_read = set()
for line in input_R1:
	count += 1
	if count % 4 != 1: continue
	line = line.split(" ")
	R1_read.add(line[0])
input_R1.close()

count = 0
R2_read = set()
for line in input_R2:
        count += 1
        if count % 4 != 1: continue
        line = line.split(" ")
        R2_read.add(line[0])
input_R2.close()

remove_R1_read = R1_read.difference(R2_read)
input_R1=open(sys.argv[1])
count = 0
for line in input_R1:
	count += 1
	if count % 4 == 1: data = []
	data.append(line)
	if count % 4 == 0:
		read_name = data[0].split(" ")
		if read_name[0] in remove_R1_read: continue
		output_R1.write(data[0] + data[1] + data[2] + data[3])
input_R1.close()
output_R1.close()

remove_R2_read = R2_read.difference(R1_read)
input_R2=open(sys.argv[2])
count = 0
for line in input_R2:
        count += 1
        if count % 4 == 1: data = []
        data.append(line)
        if count % 4 == 0:
                read_name = data[0].split(" ")
                if read_name[0] in remove_R2_read: continue
                output_R2.write(data[0] + data[1] + data[2] + data[3])
input_R2.close()
output_R2.close()

