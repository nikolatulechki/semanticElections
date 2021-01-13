import sys

with open (sys.argv[1]) as file:
	for line in file.readlines():

		vals = line.rstrip().split(";")
		pref = vals[0]
		if pref[0] is "0":
			jur = pref[1:2]
		else:
			jur = pref[0:2]
		#print pref

		for i in range(len(vals[1:])-1):
			if(i % 2 == 0):
				out = []
				out.extend([pref,jur,str((i/2)+1)])
				out.extend(vals[i+1:i+3])
				sys.stdout.write(";".join(out)+'\n')
