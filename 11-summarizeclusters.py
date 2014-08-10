types=['auxo','rich','both']
fsummary = open('weka/summary_clusters.txt','w')
for t in types:
	f=open('weka/'+t+'/cluster_assign.txt')
	group1 = []
	group2 = []
	group3 = []
	group4 = []
	for line in f:
		d = line.split()
		if len(d) < 2:
			continue
		if '0' in d[1]:
			group1.append(int(d[0])+1)
		elif '1' in d[1]:
			group2.append(int(d[0])+1)
		elif '2' in d[1]:
			group3.append(int(d[0])+1)
		elif '3' in d[1]:
			group4.append(int(d[0])+1)
		else:
			printf("only different zero\n");
	fsummary.write(t+'\n')
	
	fsummary.write('Group 1:\n')
	fsummary.write('.'.join([str(x) for x in group1]))

	fsummary.write('\nGroup 2:\n')
	fsummary.write('.'.join([str(x) for x in group2]))

	fsummary.write('\nGroup 3:\n')
	fsummary.write('.'.join([str(x) for x in group3]))

	fsummary.write('\nGroup 4:\n')
	fsummary.write('.'.join([str(x) for x in group4]))
	
	fsummary.write('\n\n')
	