import pandas as pd
import numpy as np
import scipy.stats
import pickle
from scipy import stats
import luigi
import random
class save_distributions(luigi.Task):
    file = luigi.Parameter()
    def run(self):
        data = pd.read_csv(self.file)
        kernel = stats.gaussian_kde(data['probability'])
        #we fit the distribution and save as a pickle
        pickle.dump(kernel,open('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.file.split('/')[10][:-4]+'probabs'+'.pck'),'wb'))
    def requires(self):
        return []
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.file.split('/')[10][:-4]+'probabs'+'.pck'))