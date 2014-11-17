import networkx as nx


fileLog = open('filelog.txt', 'w')

# read ppi,reg,met
fppi = open('files/ppi.tab')
freg = open('files/reg.tab')
fmet = open('files/met.tab')
fint = open('files/int.tab')


def readfile(file):
    listtuple = []
    for line in file:
        data = line.split()
        listtuple.append((data[0], data[1]))
    return listtuple


listppi = readfile(fppi)
listreg = readfile(freg)
listmet = readfile(fmet)
listInt = readfile(fint)

#Each gene has associated two centralities (degree and betweeness)
#related to 4 networks: Int, ppi, reg and met resulting in 8 dictionaries
#plus regin,regout and metin,metout

llca = ['degint', 'degppi', 'degreg', 'degmet', 'betint', 'betppi', \
        'betreg', 'betmet', 'regin', 'regout', 'metin', 'metout', 'cloint', \
        'cloppi', 'cloreg', 'clomet', 'loaint', 'loappi', 'loareg', 'loamet']  #list with labels

#Initialize a dictionary for each centrality
exec ("\n".join(["dic" + x + "={}" for x in llca]))

# Setting up graphs
GInt = nx.Graph()
Gppi = nx.Graph()
Greg = nx.DiGraph()  #directed graph
Gmet = nx.DiGraph()  #directed graph
#Fill graphs: Int is made of all networks
for nodes in listInt:
    GInt.add_edge(nodes[0], nodes[1])
for nodes in listppi:
    Gppi.add_edge(nodes[0], nodes[1])
for nodes in listreg:
    Greg.add_edge(nodes[0], nodes[1])
for nodes in listmet:
    Gmet.add_edge(nodes[0], nodes[1])

#Nodes : list of nodes
nodesGInt = GInt.nodes()
nodesGppi = Gppi.nodes()
nodesGreg = Greg.nodes()
nodesGmet = Gmet.nodes()

#my variabl 'allpairs' are all possible genes pairs and the score is unknown "?"
allpairs = {}
size = len(nodesGInt)
for i in range(size):
    for j in range(i + 1, size):  #avoid redundant interactions
        n1 = nodesGInt[i]
        n2 = nodesGInt[j]
        allpairs[(n1, n2)] = "?"

#Sizes: how many gene are there
lenGInt = len(nodesGInt)
lenGppi = len(nodesGppi)
lenGreg = len(nodesGreg)
lenGmet = len(nodesGmet)


#Missing values will be zero (string)
for g in nodesGInt:
    exec ("\n".join(['dic' + x + '[g]=0' for x in llca]))


#centralities calculation
dicdegint.update(GInt.degree())
dicdegppi.update(Gppi.degree())
dicdegreg.update(Greg.degree())
dicdegmet.update(Gmet.degree())
dicregin.update(Greg.in_degree())
dicregout.update(Greg.out_degree())
dicmetin.update(Gmet.in_degree())
dicmetout.update(Gmet.out_degree())

#betweeness calculation
dicbetint.update(nx.algorithms.centrality.betweenness_centrality(GInt))
dicbetppi.update(nx.algorithms.centrality.betweenness_centrality(Gppi))
dicbetreg.update(nx.algorithms.centrality.betweenness_centrality(Greg))
dicbetmet.update(nx.algorithms.centrality.betweenness_centrality(Gmet))

#closeness calculation
diccloint.update(nx.closeness_centrality(GInt))
diccloppi.update(nx.closeness_centrality(Gppi))
diccloreg.update(nx.closeness_centrality(Greg))
dicclomet.update(nx.closeness_centrality(Gmet))

#load calculation
dicloaint.update(nx.load_centrality(GInt))
dicloappi.update(nx.load_centrality(Gppi))
dicloareg.update(nx.load_centrality(Greg))
dicloamet.update(nx.load_centrality(Gmet))

#Save attributes file
fileCent = open('files/centralites.tab', 'w')
fileCent.write("gene\t" + ("\t".join(llca)) + '\n')
q1 = (("%s\t") * (len(llca) + 1)).rstrip("\t") + "\n"
q2 = "n," + (",".join(["dic" + x + "[n]" for x in llca])) + "\n"
for n in nodesGInt:
    fileCent.write(q1 % (eval(q2)))
fileCent.close()


#List of genes
fileNodes = open('files/genes.tab', 'w')
for g in nodesGInt:
    fileNodes.write(g + '\n')







