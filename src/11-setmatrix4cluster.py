# ################################
# AUTHOR: ESTHER CAMILO          #
#e-mail: esthercamilo@gmail.com #
#################################

import os

fcfg = open('config.txt')
folder = fcfg.readline().rstrip('\n')
wekalocation = fcfg.readline().rstrip('\n')

# get the data generated by java_weka and make a matrix for further clustering

types = [('auxo', 'CE-AUX'), ('both', 'CE'), ('rich', 'CE-RICH')]

#For J48 - objective is to find the representative tree
# for t in types:
#     strinput = "java -cp " + wekalocation + ":. prob " + folder + "weka/" + t[0] + "/completeTraining-" + t[1] + ".arff out model"
#     os.system(strinput)
#     saida = open(folder + 'weka/' + t[0] + '/matrix.csv', 'w')
#     listas = []
#     for i in range(1, 101):
#         f = open(folder + 'weka/' + t[0] + '/out/' + str(i) + '.out')
#         l = []
#         for line in f:
#             l.append(line[74:79])
#         listas.append(l)
#
#     primer = "inst1"
#     for j in range(len(listas[0]) - 1):
#         primer = primer + ",inst" + str(j + 2)
#
#     saida.write(primer + "\n")
#
#     for elem in listas:
#         line = ','.join([str(x) for x in elem])
#         saida.write(line + "\n")



#For meta vote - objetive is finding the probabilities


for t in types:
    strinput = "java -cp " + wekalocation + ":. prob " + folder + "weka/" + t[0] + "/completeTraining-" + t[1] + ".arff out_vote model_vote"
    os.system(strinput)

