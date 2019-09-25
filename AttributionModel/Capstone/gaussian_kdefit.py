import pandas as pd
import numpy as np
import scipy.stats
import pickle
from scipy import stats
import luigi
import random
class save_distributions(luigi.Task):
    file_tag = luigi.Parameter()
    def run(self):
        path = '/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'
        data = pd.read_csv(path+self.file_tag+'.csv')
        kernel = stats.gaussian_kde(data['probability'])
        #we fit the distribution and save as a pickle
        pickle.dump(kernel,open('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.file_tag)+'probabs'+'.pck','wb'))
    def requires(self):
        return []
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.file_tag)+'probabs'+'.pck')