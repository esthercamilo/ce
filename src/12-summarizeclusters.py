# ################################
# AUTHOR: ESTHER CAMILO          #
#e-mail: esthercamilo@gmail.com  #
##################################


##########################################################################################
# We have 100 trees. Each tree contains the probability of classification of each        #
# instance. These instances in turn, are pairs of genes. One matrix whose rows represent #
# each tree was constructed and the columns are instances. Thus, each column             #
# shows how each training set generates different probabilities of classifying a         #
# single instance. It would be desirable that the values in the same column              #
# were the same, but are not, because even if the samples were derived from the          #
# same set, they are different (undersampling consequence). Thus, we find the            #
# average for each column within each cluster. By minimization of distances,             #
# we find the tree that is closest to that center.                                       #
##########################################################################################


fcfg = open('config.txt')
folder = fcfg.readline().rstrip('\n')

wekalocation = fcfg.readline().rstrip('\n')

from string import *
import numpy as np

def dist(x,y):
    return np.sqrt(np.sum((x-y)**2))

def getTree(m): #(m vem com o numero da tree e linha)

	#gerar lista de arvores no cluster
	treesnocluster=[]
	for am in m:
		treesnocluster.append(am[0])
	#gerar matrix somente com linha
	mat = []
	for a in m:
		mat.append(a[1])
	npmat = np.array(mat)
	tmat = np.transpose(npmat)

	matavg = []
	for line in tmat:
		av = np.mean(line)
		matavg.append(av)
	matavg = np.array(matavg)

	dist
	#Arvore mais proxima
	distancia = dist(npmat[0],matavg) #faz a primeira pra ter comparativo
	menorTree = m[0][0]
	for j in range(len(npmat)):
		tdist = dist(npmat[j],matavg)
		if tdist<distancia:
			distancia = tdist
			menorTree = m[j][0]
	#importante somar +1 pois a numeracao das arvores nao comeca em zero.
	return (treesnocluster,menorTree)


def outputf(b,i):
	mp = getTree(b)
	treesnocluster = mp[0]
	menorTree = mp[1]
	s1 = ""
	for k in treesnocluster:
		s1 = s1 + str(k) + ', '
	output.write("Cluster%s : %s\n" % (i,menorTree))
	output.write(s1.rstrip()+"\n\n\n")

types = ['rich', 'both', 'auxo']

for t in types:
    f1=open(folder+'weka/'+t+'/cluster_assign.txt')
    #um dicionario Key:tree e Value:cluster
    dicclust={}
    for line in f1:
        if line =="\n":
            continue
        try:
            d = line.rstrip().split(" ")
            tree = int(d[0])
            clust = int(d[1])
            dicclust[tree]=clust
        except:
            print "error reading line."

    f2 = open(folder+'weka/'+t+'/matrix.csv')

    m0=[]
    m1=[]
    m2=[]
    m3=[]

    f2.readline()
    i=0
    for line in f2:
        d = line.rstrip().split(',')
        linha = []
        for l in d:
            linha.append(float(l))
        n = dicclust[i]
        if n==0:
            m0.append((i,linha))
        elif n==1:
            m1.append((i,linha))
        elif n==2:
            m2.append((i,linha))
        elif n==3:
            m3.append((i,linha))
        else:
            print 'something wrong'
        i=i+1

    #OUTPUT
    output = open(folder+'weka/'+t+'/repTree.csv','w')
    # Cluster 1
    outputf(m0,0)
    outputf(m1,1)
    outputf(m2,2)
    outputf(m3,3)










