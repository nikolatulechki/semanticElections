import sys

with open (sys.argv[1]) as file:
	for line in file.readlines():

		vals = line.rstrip().split(";")
		pref = vals[0:2]
		#print pref

		for i in range(len(vals[2:])):
			if((i+5) % 5 == 0):
				out = []
				out.extend(pref) 
				out.extend(vals[i+2:i+7])
				sys.stdout.write(";".join(out)+'\n') 
