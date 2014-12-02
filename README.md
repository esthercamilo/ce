PREDICTION OF CONDITIONAL ESSENTIAL GENES
============================================

To follow this workflow, first you need to satisfy all requirements described in the file "requirement.txt".

Below, all the Python scripts needed to reproduce the experiment described in the article:
<strong>"Prediction of Conditional Essential genes in <i>Escherichia coli</i> using network topology
and machine learning"</strong>

01-networks-ppi-reg-met.py
Build dictionaries from data from DIP, Regulon and BIGG to create ppi.tab files, reg.tab, met.tab.

02-integrated-interactions.py
Read files ppi.tab, reg.tab and met.tab. Build int.tab integrated network.
The file int.tab contains the intersection of the three networks.

03-centralities.py
The degree, betweeness, closeness and load are calculated for each gene for each network (ppi, reg, met,
int). The output is the file "centralites.tab".

04-goterms.py
Create the file "cegoterms.tab" containing each gene and F or T for each term combined to centralities values.

05-classE-CE.py
The output files "ceaux.tab", "cerich.tab" and "ceboth.tab" are created from original data in xls file.

06-wekatraining.py
The folder structure is set up inside Weka folder. The csv folder is filled up with 100 training set.

07-wekaclassifier.py
Convert all csv files to arff by removing the column "gene". Apply J48 where the output is result, model and dot.
Correct arff umbalanced. 

08-metavote.py
weka.classifiers.meta.Vote: Cannot handle multi-valued nominal class! This part was skipped.

09-over_result.py
Create the folder "oversampling" inside each folder experiment and fill it with the oversampled training set.

10-weka4over.py
Apply J48 in the oversampled training set.

11-setmatrix4cluster.py
This script contains two steps: first, apply the model generated by the step 05 (it runs a java program - to the 
original training sets. Next it generates the matrix input for clustering experiment.

12-wekacluster.py
Create the file "cluster_assign.txt" for each experiment which column 1 contains the tree (0-99) and the column 2 
contains the cluster (0-3).

13-summarizeclusters.py
Create the file "repTree.csv". This file contains the representative tree for each cluster. It is possible to infer 
the dominant cluster.

14-stat_metrics.py
summary for all metrics in the output file: "metrics.txt"

15-resume_probs.py
create the file "prior.txt" with the probabilities of a gene be CE from meta vote. 

The remaining analyses were performed using R. The R scripts can be found at: <a href="http://rpubs.br/esthercamilo/"></a>

Now you're all set to reproduce the experiment. Have fun!