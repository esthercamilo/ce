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
    makedir('weka/' + ce + '/arff_rnd')
    makedir('weka/' + ce + '/csv')
    makedir('weka/' + ce + '/csv_rnd')
    makedir('weka/' + ce + '/dot')
    makedir('weka/' + ce + '/model')
    makedir('weka/' + ce + '/out')
    makedir('weka/' + ce + '/png')
    makedir('weka/' + ce + '/result')
    makedir('weka/' + ce + '/result_rnd')
    makedir('weka/' + ce + '/vote_result')
    makedir('weka/' + ce + '/vote_result_rnd')


folders('auxo')
folders('rich')
folders('both')

#Read files 
fcent = open(folder + 'files/cegoterms.csv')  #centralites
headerCent = fcent.readline()
strHeader = (headerCent.rstrip().replace('gene,', '')) + ',class\n'
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
    data = elem.rstrip('\n').split(',')
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

def executa(tipo,classe,dic): #('auxo','CE-AUX',dicaux)

    dicComp = {}

    for gene in allgenes:
        try:
            dicComp[gene] = diccent[gene] + [dic[gene]]
        except Exception as e:
            print 'Ex3: ', e
    li = dicComp.values()
    size = len(dicComp.values())
    ceaux = [x for x in li if x[len(x) - 1] == classe]
    essen = [x for x in li if x[len(x) - 1] == 'ESSENTIAL']
    norma = [x for x in li if x[len(x) - 1] == 'NORMAL']
    minSize = min(min(len(ceaux), len(essen)), len(norma))

    for i in range(1, 101):
        output = open(folder + 'weka/'+tipo+'/csv/' + str(i) + '.csv', 'w')
        output_rnd = open(folder + 'weka/'+tipo+'/csv_rnd/' + str(i) + '.csv', 'w')
        output.write(strHeader)
        output_rnd.write(strHeader)
        rm.shuffle(ceaux)
        rm.shuffle(essen)
        rm.shuffle(norma)
        tclasses = [classe,'ESSENTIAL','NORMAL']

        for j in range(minSize):
            rm.shuffle(tclasses)
            strA = ','.join(ceaux[j])
            strB = ','.join(essen[j])
            strC = ','.join(norma[j])

            output.write(strA + '\n')
            output.write(strB + '\n')
            output.write(strC + '\n')

            t0 = tclasses[0]
            t1 = tclasses[1]
            t2 = tclasses[2]

            c0 = strA.rstrip('\n').split(',')[-1]
            c1 = strB.rstrip('\n').split(',')[-1]
            c2 = strC.rstrip('\n').split(',')[-1]

            output_rnd.write(strA.replace(c0,t0) + '\n')
            output_rnd.write(strB.replace(c1,t1) + '\n')
            output_rnd.write(strC.replace(c2,t2) + '\n')


executa('auxo','CE-AUX',dicaux)
executa('rich','CE-RICH',dicrich)
executa('both','CE',dicce)

#Set complete training set with "?" as class
fcompletSet = open(folder + 'files/completeTraining.csv', 'w')
fcompletSet.write(strHeader)

a = diccent.values()

for v in diccent.values():
    fcompletSet.write(','.join(v) + ',?\n')
	
		
