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
        pickle.dump(kernel,open('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.file.split('/')[7][:-4]+'probabs'+'.pck'),'wb'))
    def requires(self):
        return []
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.file.split('/')[7][:-4]+'probabs'+'.pck'))
#takes n samples and saves sample in csv
class sample_output(luigi.Task):
    sample_file = luigi.Parameter()
    size = luigi.Parameter()
    def run(self):
        kernel = pd.read_csv('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.sample_file)+'.csv')
        # kernel = pickle.load('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.file)+'.pck')
        #we get samples from the distributions, going to use when simulating MCMC model
        kernel = kernel['probability'].sample(int(self.size))
        return kernel.to_csv('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.sample_file)+'+sampleprobabs'+'.csv')
    def requires(self):
        []
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.sample_file)+'+sampleprobabs'+'.csv')
class state_machine(luigi.Task):
    sampled = luigi.Parameter()
    def run(self):
        states = pd.read_csv(self.sampled)
        states['session-leads']  = states.ix[:, 1].apply(lambda x: x if x > random.uniform(0,2) else False)
        states['leads-opps'] = states['session-leads'].apply(lambda x: x if x > random.uniform(0,2) else False)
        states['opps-complete'] = states['leads-opps'].apply(lambda x: x if x > random.uniform(0,2)else False)
        return states.to_csv('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.sampled.split('/')[7][:-4]+'statemachine'+'.csv'))
    def requires(self):
        return []
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.sampled.split('/')[7][:-4]+'statemachine'+'.csv'))
class wrapper(luigi.WrapperTask):
    def requires(data):
        files = ['Sessiontolead.csv','leadtoopportunity.csv','opportunitytocomplete.csv']
        # pickle_file = 'Probabiliprobabs'
        csv_file = 'Sessiontolead'
        sampled_data = '/Users/emmanuels/Documents/AttributionData/Data/Probabilities/Sessiontolead+sampleprobabs.csv'
        size = 10000
        task_list = []
        for i in range(1,len(files)):
            file_path = '/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'
            task_list.append(save_distributions(file=file_path+str(files[i])))
        return [task_list,sample_output(sample_file=csv_file,size=int(size)),state_machine(sampled=sampled_data)]
    def run(self):
        print('The wrapper is complete')
        return pd.DataFrame().to_csv('/Users/emmanuels/Documents/AttributionData/Data/Checkpoints/datawranglerwrapper3.csv')
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/AttributionData/Data/Checkpoints/datawranglerwrapper3.csv')
if __name__ == '__main__':
    luigi.build([wrapper()],workers=8,local_scheduler=True)

