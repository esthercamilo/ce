##################################
#AUTHOR: ESTHER CAMILO           #
#e-mail: esthercamilo@gmail.com  #
##################################

from string import *
import numpy as np

fcfg = open('config.txt')
folder = fcfg.readline().rstrip('\n')

types = ['auxo','rich']

#Read result and return the averages:  TP, FP, Precision, Recall, F, AUC for the cross-validation
def readWeka(att, folder_result):
    listFiles = []
    for i in range(1, 101):
        file = open(folder + "weka/" + att + "/" + folder_result + "/" + str(i) + "-result.txt")
        thisLine = ''
        while 'Stratified cross-validation' not in thisLine:
            thisLine = file.readline()
        while 'Detailed Accuracy By Class' not in thisLine:
            thisLine = file.readline()
        for j in range(2):
            thisLine = file.readline()
        dic = {}
        for l in range(4):
            avg = file.readline()
            TP = float(avg[16:24].strip())
            FP = float(avg[25:35].strip())
            Precision = float(avg[35:45].strip())
            Recall = float(avg[45:55].strip())
            F = float(avg[55:65].strip())
            ROC = float(avg[65:75].strip())
            classe = avg[75:85].strip()
            if classe == '':
                classe = 'AVG'
            dic[classe] = [TP, FP, Precision, Recall, F, ROC]
        listFiles.append(dic)
    return listFiles


def avgListArrays(listArrays):
    summation = 0
    for elem in listArrays:
        summation = summation + elem
    return summation / len(listArrays)


def metricas(tipo,name_output):

    output = open(folder + 'weka/' + tipo + '/'+name_output, 'w')

    output.write(tipo+"\n\n")

    output.write("Respectively, the J48 experiment, J48 random, Meta Vote experiment and Meta Vote random\n")
    output.write("========================================================================================\n")

    #Average Experiment

    for resulttype in ["result","result_rnd","vote_result","vote_result_rnd"]:
        arrayDeg = readWeka(tipo, resulttype)
        arrayexpNO = []
        arrayexpES = []
        arrayexpCE = []
        arrayexpAV = []
        classe = 'CE'
        if tipo =='auxo':
            classe = 'CE-AUX'
        elif tipo == 'rich':
            classe = 'CE-RICH'

        for elem in arrayDeg:
            arrayexpNO.append(np.array(elem['NORMAL']))
            arrayexpES.append(np.array(elem['ESSENTI']))
            arrayexpCE.append(np.array(elem[classe]))
            arrayexpAV.append(np.array(elem['AVG']))

        avgexpNO = avgListArrays(arrayexpNO)
        avgexpES = avgListArrays(arrayexpES)
        avgexpCE = avgListArrays(arrayexpCE)
        avgexpAV = avgListArrays(arrayexpAV)

        output.write(resulttype+'\n')
        output.write('TP\t&\tFP\t&\tPrecision\t&\tRecall\t&\tF\t&\tAUC\n')
        output.write('\nNORMAL\n')
        output.write('\t&\t'.join([str(x) for x in avgexpNO]))
        output.write('\nESSENTIAL\n')
        output.write('\t&\t'.join([str(x) for x in avgexpES]))
        output.write('\n'+classe+'\n')
        output.write('\t&\t'.join([str(x) for x in avgexpCE]))
        output.write('\nAVG\n')
        output.write('\t&\t'.join([str(x) for x in avgexpAV]))
        output.write('\n\n\n\n')
    output.close()



for t in types:
    metricas(t,"metrics.txt")


