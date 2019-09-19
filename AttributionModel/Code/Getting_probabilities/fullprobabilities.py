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
    file = luigi.Parameter()
    size = luigi.Parameter()
    def run(self):
        kernel = pickle.load('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.file.split('/')[7][:-4]+'probabs'+'.pck'))
        #we get samples from the distributions- going to use when simulating MCMC model
        kernel = kernel.sample(int(self.size))
        return kernel.to_csv('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.file.split('/')[7][:-4]+'probabs'+'.csv'))
    def requires(self):
        return wrapper(file = self.file)
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.file.split('/')[7][:-4]+'probabs'+'.csv'))
class state_machine(luigi.Task):
    size = luigi.Parameter()
    csv_path = luigi.Parameter()
    def run(self):
        csv_file = pd.read_csv(sef.csv_path)
        obs = csv_file.pop()  # pop first observation
        csv_file.to_csv(csv_file)
        func = lambda x: x if x > random.uniform(0, 1) else False
        states = dict(state_leads=func(obs))
        states['lead_opps'] = func(states['state_leads'])
        states['opp_comp'] = func(states['lead_opps'])
        states_df = pd.DataFrame([results],columns=results.keys())
        return states_df.to_csv('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.csv_path.split('/')[7][:-4]+'states'+'.csv'))
    def requires(self):
        yield sample_output(size=self.size)
        yield wrapper(csv_path=self.csv_path)
    def output(self):
        return states_df.to_csv('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.csv_path.split('/')[7][:-4]+'states'+'.csv'))
class wrapper(luigi.WrapperTask):
    def requires(data):
        files = ['Sessiontolead.csv','leadtoopportunity.csv','opportunitytocomplete.csv']
        csv_path = '/Users/emmanuels/Documents/AttributionData/Data/Probabilities/Sessiontolead.csv'
        task_list = []
        for i in range(1,len(files)):
            file_path = '/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'
            task_list.append(save_distributions(file=file_path+str(files[i])))
        yield task_list
        yield csv_path
    def run(self):
        print('The wrapper is complete')
        return pd.DataFrame().to_csv('/Users/emmanuels/Documents/AttributionData/Data/Checkpoints/datawranglerwrapper3.csv')
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/AttributionData/Data/Checkpoints/datawranglerwrapper3.csv')
if __name__ == '__main__':
    luigi.build([wrapper()],workers=8,local_scheduler=True)



    #then call state machine function for the next state change
    #roll dice etc
    #etc

    # roll a dice num between 0 and 1
    # run one customer at a time
    # pull a probability from csv file for state change (initial to lead) - 1 sample
    # for single sample check dice state we rolled, is it smaller than this probability or not
    # if smaller, then customer goes to next state
    #3rd state change


#exploratory analysis
#how the distributions are looking - different distr for diff state changes
# visualise fitted gaussian KDEs for each state
#sample 10k samples and visualise 10k samples to confirm that sample looks like gaussian KDE

#create characteristics of distributions (mean, median, probabilities etc)

#taking samples from observations -> creating the model itself -> inside luigi, loading sample output class, pipeline that goes through diff states, bring if