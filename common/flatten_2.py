import sys

with open (sys.argv[1]) as file:
	for line in file.readlines():

		vals = line.rstrip().split(";")
		pref = vals[1]

		for i in range(len(vals[3:])):
			if(i % 2 == 0):
				out = []
				out.append(pref)
				out.extend(vals[i+3:i+5])
				sys.stdout.write(";".join(out)+'\n') 
