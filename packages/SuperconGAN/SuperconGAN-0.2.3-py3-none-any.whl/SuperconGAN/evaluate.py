"""
Module serves to evaluate the quality of data produced by the Synthesizer.
"""

from sdv.evaluation import evaluate
import pandas as pd

class Evaluator():
    """
    Class serves to evaluate the quality of data produced by the Synthesizer.
    """

    def __init__(self, synthetic_data):
        """
        Method to initialize class.
        """
        print("Started importing data!")

        url_1 = "https://raw.githubusercontent.com/RajeevAtla/Superconductivity-Dataset/master/train.csv"
        url_2 = "https://raw.githubusercontent.com/RajeevAtla/Superconductivity-Dataset/master/unique_m.csv"

        material_data = pd.read_csv(url_1, header = 0, sep = ",")
        material_data.pop("critical_temp")

        element_data = pd.read_csv(url_2, header = 0, sep = ",")
        element_data.pop("material")
        element_data.pop("critical_temp")

        data = material_data.join(element_data)

        print("Finished importing data!")

        self.synthetic_data = synthetic_data
        self.real_data = data

    def evaluate_data(self,
                      aggregate = True,
                      metrics = None):
        """
        Method to evaluate data
        """

        evaluate(synthetic_data = self.synthetic_data,
                 real_data = self.real_data,
                 metrics = metrics,
                 aggregate = aggregate)
