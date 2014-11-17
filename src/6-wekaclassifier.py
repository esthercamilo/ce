import os
from threading import Thread


threads = []
end = 101


# Convert csv to arff
def convert():
    print '***********CONVERTING FROM CSV TO ARFF'
    os.system("java weka.core.converters.CSVLoader files/completeTraining.csv > weka/completeTraining.arff")
    for i in range(1, end):
        os.system(
            "java weka.core.converters.CSVLoader weka/auxo/csv/" + str(i) + ".csv > weka/auxo/arff/" + str(i) + ".arff")
        os.system(
            "java weka.core.converters.CSVLoader weka/rich/csv/" + str(i) + ".csv > weka/rich/arff/" + str(i) + ".arff")
        os.system(
            "java weka.core.converters.CSVLoader weka/both/csv/" + str(i) + ".csv > weka/both/arff/" + str(i) + ".arff")


#J48 output result, dot, model
def j48():
    print '***********J48 output result, dot, model '
    for i in range(1, end):
        os.system("java -Xmx1000m weka.classifiers.trees.J48 -d weka/auxo/model/" + str(
            i) + ".model -M 64 -t weka/auxo/arff/" + str(i) + ".arff -i  > weka/auxo/result/" + str(i) + "-result.txt")
        os.system("java -Xmx1000m weka.classifiers.trees.J48 -M 64 -g -t weka/auxo/arff/" + str(
            i) + ".arff -i  > weka/auxo/dot/" + str(i) + "-result.dot")

    for i in range(1, end):
        os.system("java -Xmx1000m weka.classifiers.trees.J48 -d weka/rich/model/" + str(
            i) + ".model -M 64 -t weka/rich/arff/" + str(i) + ".arff -i  > weka/rich/result/" + str(i) + "-result.txt")
        os.system("java -Xmx1000m weka.classifiers.trees.J48 -M 64 -g -t weka/rich/arff/" + str(
            i) + ".arff -i  > weka/rich/dot/" + str(i) + "-result.dot")

    for i in range(1, end):
        os.system("java -Xmx1000m weka.classifiers.trees.J48 -d weka/both/model/" + str(
            i) + ".model -M 64 -t weka/both/arff/" + str(i) + ".arff -i  > weka/both/result/" + str(i) + "-result.txt")
        os.system("java -Xmx1000m weka.classifiers.trees.J48 -M 64 -g -t weka/both/arff/" + str(
            i) + ".arff -i  > weka/both/dot/" + str(i) + "-result.dot")


#It is important to keep the class order in training files
def setClassOrder(namefile):
    file = open(namefile)
    lines = file.readlines()
    s = [x for x in lines if '@attribute class' in x][0]
    index = lines.index(s)

    typeOfClass = '{CE,ESSENTIAL,NORMAL}'
    newLine = s.replace('numeric', typeOfClass)
    lines[index] = newLine
    output = open(namefile.replace('.arff', '-CE.arff'), 'w')
    for i in range(len(lines)):
        output.write(lines[i])

    typeOfClass = '{CE-AUX,ESSENTIAL,NORMAL}'
    newLine = s.replace('numeric', typeOfClass)
    lines[index] = newLine
    output = open(namefile.replace('.arff', '-AUX.arff'), 'w')
    for i in range(len(lines)):
        output.write(lines[i])

    typeOfClass = '{CE-RICH,ESSENTIAL,NORMAL}'
    newLine = s.replace('numeric', typeOfClass)
    lines[index] = newLine
    output = open(namefile.replace('.arff', '-RICH.arff'), 'w')
    for i in range(len(lines)):
        output.write(lines[i])


#Draw trees		
def drawTrees(type):
    print '***********DRAWING TREES '
    for i in range(1, end):
        os.system("dot -Tpng weka/" + type + "/dot/" + str(i) + "-result.dot -o weka/" + type + "/png/" + str(
            i) + "result.png")


def setModel():
    print '***********APPLYING MODEL'
    for i in range(1, end):
        os.system(
            "java -Xmx1000m weka.classifiers.trees.J48 -p 0 -T weka/completeTraining-CE.arff -l weka/both/model/" + str(
                i) + ".model > weka/both/out/" + str(i) + ".out")
        os.system(
            "java -Xmx1000m weka.classifiers.trees.J48 -p 0 -T weka/completeTraining-AUX.arff -l weka/auxo/model/" + str(
                i) + ".model > weka/auxo/out/" + str(i) + ".out")
        os.system(
            "java -Xmx1000m weka.classifiers.trees.J48 -p 0 -T weka/completeTraining-RICH.arff -l weka/rich/model/" + str(
                i) + ".model > weka/rich/out/" + str(i) + ".out")


threadConvert = Thread(target=convert, args=())

threadj48 = Thread(target=j48, args=())

address = ['weka/completeTraining.arff']
threadOrder1 = Thread(target=setClassOrder, args=(address))
threadOrder2 = Thread(target=setClassOrder, args=(address))
threadOrder3 = Thread(target=setClassOrder, args=(address))

threadDrawTreesAux = Thread(target=drawTrees, args=(['auxo']))
threads.append(threadDrawTreesAux)
threadDrawTreesRich = Thread(target=drawTrees, args=(['rich']))
threads.append(threadDrawTreesRich)
threadDrawTreesBoth = Thread(target=drawTrees, args=(['both']))
threads.append(threadDrawTreesBoth)

threadSetModel = Thread(target=setModel, args=())

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

# Start setModel
threadSetModel.start()
threadSetModel.join()


