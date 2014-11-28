import java.io.FileNotFoundException;
import java.util.Formatter;
import weka.classifiers.Classifier;
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;

public class prob{

/* args are the complete path for umbalanced-???.arff*/

public static void main(String[] args) {

			String modelFileSerialized; 
			String testFileARFF = args[0];
            String toutput = args[1];
			//split path in the slash and find the parent folder
			String[] parts = testFileARFF.split("/");
			int lastIndex = parts.length;
			String parentFolder ="";
			for(int i = 0; i < lastIndex-1; i++) {
				parentFolder = parentFolder + "/" + parts[i];
			}

			Formatter fmt;
			prob p = new prob();
			String outputfile;
			for (int i = 0; i < 100; i++) {
				modelFileSerialized = parentFolder+"/model/"+(i+1)+".model";
				outputfile = parentFolder+"/"+toutput+"/"+(i+1)+".out";
				try {
					fmt = new Formatter(outputfile);
				
					try {
						p.test(modelFileSerialized,testFileARFF,fmt);
					} catch (Exception e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
					fmt.close();
				
				} catch (FileNotFoundException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
				}
			
		

		}	
	}

public void test(String modelFileSerialized, String testFileARFF, Formatter output) 
    throws Exception
{
	
    // Deserialize the classifier.
    Classifier classifier = 
        (Classifier) weka.core.SerializationHelper.read(
            modelFileSerialized);

    // Load the test instances.
    Instances testInstances = DataSource.read(testFileARFF);

    // Mark the last attribute in each instance as the true class.
    testInstances.setClassIndex(testInstances.numAttributes()-1);

    int numTestInstances = testInstances.numInstances();
    //System.out.printf("There are %d test instances\n", numTestInstances);

    // Loop over each test instance.
    for (int i = 0; i < numTestInstances; i++)
    {
        // Get the true class label from the instance's own classIndex.
        String trueClassLabel = 
            testInstances.instance(i).toString(testInstances.classIndex());

        // Make the prediction here.
        double predictionIndex = 
            classifier.classifyInstance(testInstances.instance(i)); 

        // Get the predicted class label from the predictionIndex.
        String predictedClassLabel =
            testInstances.classAttribute().value((int) predictionIndex);

        // Get the prediction probability distribution.
        double[] predictionDistribution = 
            classifier.distributionForInstance(testInstances.instance(i)); 

        // Print out the true label, predicted label, and the distribution.
        output.format("%5d: true=%-10s, predicted=%-10s, distribution=", 
                i, trueClassLabel, predictedClassLabel); 

        // Loop over all the prediction labels in the distribution.
        for (int predictionDistributionIndex = 0; 
             predictionDistributionIndex < predictionDistribution.length; 
             predictionDistributionIndex++)
        {
            // Get this distribution index's class label.
            String predictionDistributionIndexAsClassLabel = 
                testInstances.classAttribute().value(
                    predictionDistributionIndex);

            // Get the probability.
            double predictionProbability = 
                predictionDistribution[predictionDistributionIndex];

           output.format("[%10s : %6.3f]", 
                    predictionDistributionIndexAsClassLabel, 
                    predictionProbability );
           
        }
        output.format("\n");

    }
}
}
