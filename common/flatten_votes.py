import sys
sec_id_index = int(sys.argv[1])
seq_start_index = int(sys.argv[2])
chunk_len = int(sys.argv[3])
filename = sys.argv[4]
with open(filename) as file:
	for line in file.readlines():

		vals = line.rstrip().split(";")
		sec_id = vals[sec_id_index]
		votes = vals[seq_start_index:]
		for i in range(len(votes)):
			if i % chunk_len == 0 :
				out = []
				out.extend([sec_id])
				out.extend(votes[i:i+chunk_len])
				sys.stdout.write(";".join(out)+'\n')
	#print pref
