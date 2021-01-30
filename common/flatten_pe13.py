import sys

with open(sys.argv[1]) as file:
	for line in file.readlines():

		vals = line.rstrip().split(";")
		pref = vals[0]
		# print(pref)

		for i in range(len(vals[1:])):
			if((i+1) % 2 == 0):
				out = []
				out.append(pref)
				out.extend(vals[i:i+2])
				sys.stdout.write(";".join(out)+'\n')