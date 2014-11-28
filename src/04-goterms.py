# ###############################
# AUTHOR: ESTHER CAMILO         #
#e-mail: esthercamilo@gmail.com #
#################################

import os

fcfg = open('config.txt')
folder = fcfg.readline().rstrip('\n')

listvars = []

listfiles = os.listdir(folder+"EcocycData")

for elem in listfiles:
    strvar = elem[:-4].replace('-', '')
    listvars.append(strvar)
    fgot = open(folder+"EcocycData/"+elem).readlines()
    exec(strvar+" = [x.rstrip() for x in fgot]")

output=open(folder+'files/cegoterms.csv','w')

fcent = (open(folder+'files/centralites.tab')).readlines()
labelcent=fcent[0].split()
lcent = [x.split() for x in fcent[1:]]

label = ",".join(labelcent)+","+",".join(listvars)+"\n"
output.write(label)

for c in lcent:
    g = c[0] #gene
    strgo = ""
    for goname in listvars:
        listprov = eval(goname)
        if g in listprov:
            strgo = strgo+",V"
        else:
            strgo = strgo+",F"
    thisline = ",".join(c)+strgo+'\n'
    output.write(thisline)


