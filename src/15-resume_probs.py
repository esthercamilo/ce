##################################
#AUTHOR: ESTHER CAMILO           #
#e-mail: esthercamilo@gmail.com  #
##################################

import re
import numpy as np

fcfg = open('config.txt')
folder = fcfg.readline().rstrip('\n')

def resumeOut(tipo,classe):

    f_gene_order = open(folder+'files/centralites.tab')
    f_gene_order.readline()

    list_gene_order = [x.split()[0] for x in f_gene_order.readlines()]

    fout = open(folder+'weka/'+tipo+'/prior.txt','w')

    pattern = re.compile(classe+" :  \d.\d\d\d")

    completeVector = []

    for i in range(1,101):
        v = []
        f = open(folder+'weka/'+tipo+'/out_vote/'+str(i)+'.out')
        for line in f:
            val = re.findall(pattern, line)[0].split()
            prob = val[-1]
            v.append(float(prob))
        completeVector.append(v)

    avg_array = []

    for i in range(len(completeVector[0])):
        sum_a = 0
        for j in range(100):
            sum_a = sum_a + completeVector[j][i]
        avg_array.append((list_gene_order[i],sum_a))


    navg_array = sorted(avg_array,key=lambda student: student[1],reverse=True)

    cegenes = open(folder+'files/ce'+tipo+'.tab')
    list_ce_gene = [x.split()[0] for x in cegenes.readlines()]

    for l in navg_array:
        boo = "F"
        if l[0] in list_ce_gene:
            boo = "T"
        fout.write('%s,%s,%s\n' %(l[0],l[1],boo))




#t = [('auxo','CE-AUX'),('rich','CE-RICH'),('both','CE')]


t = [('rich','CE-RICH')]

for tipo in t:
    resumeOut(tipo[0],tipo[1])