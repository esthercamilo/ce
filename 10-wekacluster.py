import os
types=['auxo','rich','both']
def clustering():
	for t in types:
		os.system('java weka.clusterers.SimpleKMeans -p 0 -N 4 -t weka/'+t+'/matrix.csv > weka/'+t+'/cluster_assign.txt')
clustering()