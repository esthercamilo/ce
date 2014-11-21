# ################################
# AUTHOR: ESTHER CAMILO          #
#e-mail: esthercamilo@gmail.com #
#################################


import os
import random as rm

fcfg = open('config.txt')
folder = fcfg.readline().rstrip('\n')


def makedir(namedir):
    f = folder + namedir
    if not os.path.exists(f):
        os.makedirs(f)


# Cria estrutura de arquivos

def folders(ce):
    makedir('weka/' + ce + '/arff')
    makedir('weka/' + ce + '/csv')
    makedir('weka/' + ce + '/dot')
    makedir('weka/' + ce + '/model')
    makedir('weka/' + ce + '/out')
    makedir('weka/' + ce + '/png')
    makedir('weka/' + ce + '/result')


folders('auxo')
folders('rich')
folders('both')

#Read files 
fcent = open(folder + 'files/centralites.tab')  #centralites
headerCent = fcent.readline()
strHeader = (headerCent.rstrip().replace('gene\t', '').replace('\t', ',')) + ',class\n'
fclassaux = open(folder + 'files/ceaux.tab')  #auxotrophic
fclassric = open(folder + 'files/cerich.tab')  #rich
fclassce = open(folder + 'files/ceboth.tab')  #both aux and rich
fessential = open(folder + 'files/essential.tab')  #essential genes (300)

#dictionaries
dicaux = {}
dicrich = {}
dicce = {}
dicE = {}
diccent = {}

for elem in fcent:
    data = elem.split()
    diccent[data[0]] = data[1:len(data)]

allgenes = diccent.keys()

#Set all genes as NORMAL

for gene in allgenes:
    dicaux[gene] = 'NORMAL'
    dicrich[gene] = 'NORMAL'
    dicce[gene] = 'NORMAL'


#Set classes CE
def fillDic(file, dic, type):
    for elem in file:
        data = elem.split()
        try:
            dic[data[0]] = type
        except Exception as e:
            print 'Ex1: ', data, e, type


fillDic(fclassaux, dicaux, 'CE-AUX')
fillDic(fclassric, dicrich, 'CE-RICH')
fillDic(fclassce, dicce, 'CE')

#For each dic CE set ESSENTIAL
listE = [x.rstrip() for x in fessential.readlines()]


def setEssential(dic):
    for elem in listE:
        try:
            data = elem.split()
            dic[elem] = 'ESSENTIAL'
        except Exception as e:
            print 'Ex2: ', elem, e


setEssential(dicaux)
setEssential(dicrich)
setEssential(dicce)

#Complete set for each CE

dicCompAux = {}
# outCompAux=open('files/trainingCE-AUX.csv','w')
# outCompAux.write(strHeader)
for gene in allgenes:
    try:
        dicCompAux[gene] = diccent[gene] + [dicaux[gene]]
    #outCompAux.write(','.join(dicCompAux[gene])+'\n')
    except Exception as e:
        print 'Ex3: ', e
li = dicCompAux.values()
size = len(dicCompAux.values())
ceaux = [x for x in li if x[len(x) - 1] == 'CE-AUX']
essen = [x for x in li if x[len(x) - 1] == 'ESSENTIAL']
norma = [x for x in li if x[len(x) - 1] == 'NORMAL']
minSize = min(min(len(ceaux), len(essen)), len(norma))
for i in range(1, 101):
    output = open(folder + 'weka/auxo/csv/' + str(i) + '.csv', 'w')
    output.write(strHeader)
    rm.shuffle(ceaux)
    rm.shuffle(essen)
    rm.shuffle(norma)
    for j in range(minSize):
        output.write(','.join(ceaux[j]) + '\n')
        output.write(','.join(essen[j]) + '\n')
        output.write(','.join(norma[j]) + '\n')

dicCompRich = {}
# outCompRich=open('files/trainingCE-RICH.csv','w')
# outCompRich.write(strHeader)
for gene in allgenes:
    try:
        dicCompRich[gene] = diccent[gene] + [dicrich[gene]]
    # outCompRich.write(','.join(dicCompRich[gene])+'\n')
    except Exception as e:
        print 'Ex4: ', e
li = dicCompRich.values()
size = len(dicCompRich.values())
ceric = [x for x in li if x[len(x) - 1] == 'CE-RICH']
essen = [x for x in li if x[len(x) - 1] == 'ESSENTIAL']
norma = [x for x in li if x[len(x) - 1] == 'NORMAL']
minSize = min(min(len(ceric), len(essen)), len(norma))
for i in range(1, 101):
    output = open(folder + 'weka/rich/csv/' + str(i) + '.csv', 'w')
    output.write(strHeader)
    rm.shuffle(ceric)
    rm.shuffle(essen)
    rm.shuffle(norma)
    for j in range(minSize):
        output.write(','.join(ceric[j]) + '\n')
        output.write(','.join(essen[j]) + '\n')
        output.write(','.join(norma[j]) + '\n')

dicCompCE = {}
# outCompCE=open('files/trainingCE.csv','w')
# outCompCE.write(strHeader)
for gene in allgenes:
    try:
        dicCompCE[gene] = diccent[gene] + [dicce[gene]]
    # outCompCE.write(','.join(dicCompCE[gene])+'\n')

    except Exception as e:
        print 'Ex5: ', e
li = dicCompCE.values()
size = len(dicCompCE.values())
ce = [x for x in li if x[len(x) - 1] == 'CE']
essen = [x for x in li if x[len(x) - 1] == 'ESSENTIAL']
norma = [x for x in li if x[len(x) - 1] == 'NORMAL']
minSize = min(min(len(ce), len(essen)), len(norma))
for i in range(1, 101):
    output = open(folder + 'weka/both/csv/' + str(i) + '.csv', 'w')
    output.write(strHeader)
    rm.shuffle(ce)
    rm.shuffle(essen)
    rm.shuffle(norma)
    for j in range(minSize):
        output.write(','.join(ce[j]) + '\n')
        output.write(','.join(essen[j]) + '\n')
        output.write(','.join(norma[j]) + '\n')

#Set complete training set with "?" as class
fcompletSet = open(folder + 'files/completeTraining.csv', 'w')
fcompletSet.write(strHeader)
for v in diccent.values():
    fcompletSet.write(','.join(v) + ',?\n')
	
		
