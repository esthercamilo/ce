# ################################
# AUTHOR: ESTHER CAMILO          #
#e-mail: esthercamilo@gmail.com #
#################################


import os
from threading import Thread

fcfg = open('config.txt')
folder = fcfg.readline().rstrip('\n')

wekalocation = fcfg.readline().rstrip('\n')

threads = []
end = 101


# Convert csv to arff
def convert():
    print '***********CONVERTING FROM CSV TO ARFF'
    os.system(
        "java -cp " + wekalocation + " weka.core.converters.CSVLoader " + folder + "files/completeTraining.csv > " + folder + "weka/completeTraining.arff")
    for i in range(1, end):
        os.system(
            "java -cp " + wekalocation + " weka.core.converters.CSVLoader " + folder + "weka/auxo/csv/" + str(
                i) + ".csv > " + folder + "weka/auxo/arff/" + str(i) + ".arff")
        os.system(
            "java -cp " + wekalocation + " weka.core.converters.CSVLoader " + folder + "weka/rich/csv/" + str(
                i) + ".csv > " + folder + "weka/rich/arff/" + str(i) + ".arff")
        os.system(
            "java -cp " + wekalocation + " weka.core.converters.CSVLoader " + folder + "weka/both/csv/" + str(
                i) + ".csv > " + folder + "weka/both/arff/" + str(i) + ".arff")


#J48 output result, dot, model
def j48():
    print '***********J48 output result, dot, model '
    for i in range(1, end):
        tstr1 = "java -cp " + wekalocation + " -Xmx1000m weka.classifiers.trees.J48 -d  " + folder + "weka/auxo/model/" + str(
            i) + ".model -M 64 -t " + folder + "weka/auxo/arff/" + str(
            i) + ".arff -i  > " + folder + "weka/auxo/result/" + str(i) + "-result.txt"
        os.system(tstr1)

        tstr2 = "java -cp " + wekalocation + " -Xmx1000m weka.classifiers.trees.J48 -M 64 -g -t " + folder + "weka/auxo/arff/" + str(
            i) + ".arff -i  > " + folder + "weka/auxo/dot/" + str(i) + "-result.dot"
        os.system(tstr2)

    for i in range(1, end):
        os.system(
            "java -cp " + wekalocation + " -Xmx1000m weka.classifiers.trees.J48 -d  " + folder + "weka/rich/model/" + str(
                i) + ".model -M 64 -t " + folder + "weka/rich/arff/" + str(
                i) + ".arff -i  > " + folder + "weka/rich/result/" + str(i) + "-result.txt")
        os.system(
            "java -cp " + wekalocation + " -Xmx1000m weka.classifiers.trees.J48 -M 64 -g -t " + folder + "weka/rich/arff/" + str(
                i) + ".arff -i  > " + folder + "weka/rich/dot/" + str(i) + "-result.dot")

    for i in range(1, end):
        os.system(
            "java -cp " + wekalocation + " -Xmx1000m weka.classifiers.trees.J48 -d  " + folder + "weka/both/model/" + str(
                i) + ".model -M 64 -t " + folder + "weka/both/arff/" + str(
                i) + ".arff -i  > " + folder + "weka/both/result/" + str(i) + "-result.txt")
        os.system(
            "java -cp " + wekalocation + " -Xmx1000m weka.classifiers.trees.J48 -M 64 -g -t " + folder + "weka/both/arff/" + str(
                i) + ".arff -i  > " + folder + "weka/both/dot/" + str(i) + "-result.dot")


#It is important to keep the class order in training files
def setClassOrder(namefile):
    file = open(namefile)
    lines = file.readlines()
    s = [x for x in lines if '@attribute class' in x][0]
    index = lines.index(s)

    typeOfClass = '{CE,ESSENTIAL,NORMAL}'
    newLine = s.replace('numeric', typeOfClass)
    lines[index] = newLine
    namefile1 = namefile.replace("weka","weka/both")
    output = open(namefile1.replace('.arff', '-CE.arff'), 'w')
    for i in range(len(lines)):
        output.write(lines[i])

    typeOfClass = '{CE-AUX,ESSENTIAL,NORMAL}'
    newLine = s.replace('numeric', typeOfClass)
    lines[index] = newLine
    namefile2 = namefile.replace("weka","weka/auxo")
    output = open(namefile2.replace('.arff', '-AUX.arff'), 'w')
    for i in range(len(lines)):
        output.write(lines[i])

    typeOfClass = '{CE-RICH,ESSENTIAL,NORMAL}'
    newLine = s.replace('numeric', typeOfClass)
    lines[index] = newLine
    namefile3 = namefile.replace("weka","weka/rich")
    output = open(namefile3.replace('.arff', '-RICH.arff'), 'w')
    for i in range(len(lines)):
        output.write(lines[i])


#Draw trees		
def drawTrees(type):
    print '***********DRAWING TREES '
    for i in range(1, end):
        os.system("dot -Tpng " + folder + "weka/" + type + "/dot/" + str(
            i) + "-result.dot -o " + folder + "weka/" + type + "/png/" + str(
            i) + "result.png")


threadConvert = Thread(target=convert, args=())

threadj48 = Thread(target=j48, args=())

address = [folder + 'weka/completeTraining.arff']
threadOrder1 = Thread(target=setClassOrder, args=(address))
threadOrder2 = Thread(target=setClassOrder, args=(address))
threadOrder3 = Thread(target=setClassOrder, args=(address))

threadDrawTreesAux = Thread(target=drawTrees, args=(['auxo']))
threads.append(threadDrawTreesAux)
threadDrawTreesRich = Thread(target=drawTrees, args=(['rich']))
threads.append(threadDrawTreesRich)
threadDrawTreesBoth = Thread(target=drawTrees, args=(['both']))
threads.append(threadDrawTreesBoth)

# Convert from csv to arff
threadConvert.start()
threadConvert.join()

# Start j48
threadj48.start()
threadj48.join()

# Order class
threadOrder1.start()
threadOrder1.join()
threadOrder2.start()
threadOrder2.join()
threadOrder3.start()
threadOrder3.join()

# Start drawTrees
[x.start() for x in threads]
[x.join() for x in threads]


