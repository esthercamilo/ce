# ################################
# AUTHOR: ESTHER CAMILO          #
#e-mail: esthercamilo@gmail.com #
#################################
import os

fcfg = open('config.txt')
folder = fcfg.readline().rstrip('\n')

# Read files
fcent = open(folder + 'files/cegoterms.csv')  #centralities
headerCent = fcent.readline()
strHeader = (headerCent.rstrip().replace('gene,', '')) + ',class\n'

list_cent = [x.rstrip('\n') for x in fcent.readlines()]

fclassaux = open(folder + 'files/ceaux.tab')  #auxotrophic
fclassric = open(folder + 'files/cerich.tab')  #rich
fclassce = open(folder + 'files/ceboth.tab')  #both aux and rich
fessential = open(folder + 'files/essential.tab')  #essential genes (300)

listaux = [x.rstrip().split()[0] for x in fclassaux.readlines()]
listric = [x.rstrip().split()[0] for x in fclassce.readlines()]
listess = [x.rstrip().split()[0] for x in fessential.readlines()]

listboth = listaux + listric


def setoutsample(list_ce, tipo, classe, name_output):
    if not os.path.exists(folder + 'weka/' + tipo + '/oversampling/'):
        os.makedirs(folder + 'weka/' + tipo + '/oversampling/')
    output = open(folder + 'weka/' + tipo + '/oversampling/' + name_output, 'w')
    output.write(headerCent.replace('\t', ',').replace('\n', ',classe\n'))
    listce = []
    listes = []
    listno = []
    for elem in list_cent:
        d = elem.split(',')
        if d[0] in list_ce:
            listce.append(elem)
        elif d[0] in listess:
            listes.append(elem)
        else:
            listno.append(elem)

    l_max = max(len(listno), (max(len(listce), len(listes))))
    l_min = min(len(listce), len(listes))
    lenCE = l_max / (len(listce))
    lenES = l_max / (len(listes))
    lenNO = l_max / (len(listno))

    print lenCE, lenES, lenNO

    for i in range(lenCE):
        for j in listce:
            output.write(j.replace('\t', ',') + ',' + classe + '\n')

    for i in range(lenES):
        for j in listes:
            output.write(j.replace('\t', ',') + ',ESSENCIAL\n')

    for i in range(lenNO):
        for j in listno:
            output.write(j.replace('\t', ',') + ',NORMAL\n')


setoutsample(listaux, 'auxo', 'CE-AUX', 'over_CE_aux.csv')
setoutsample(listric, 'rich', 'CE-RICH', 'over_CE_rich.csv')
setoutsample(listboth, 'both', 'CE', 'over_CE.csv')
