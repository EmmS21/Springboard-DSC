import pandas as pd
import numpy as np
import scipy.stats
import pickle
from scipy import stats
import luigi
class save_distributions(luigi.Task):
    file = luigi.Parameter()
    def run(self):
        data = pd.read_csv(self.file)
        kernel = stats.gaussian_kde(data['probability'])
        #we fit the distribution and save as a pickle
        pickle.dump(kernel,open('/Users/emmanuels/Documents//GitHub/Springboard-DSC/Springboard-DSC/AttributionModel/Data/Probabilities/'+str(self.file.split('/')[10][:-4]+'probabs'+'.pck'),'wb'))
    def requires(self):
        return []
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents//GitHub/Springboard-DSC/Springboard-DSC/AttributionModel/Data/Probabilities/'+str(self.file.split('/')[10][:-4]+'probabs'+'.pck'))
class sample_output(luigi.Task):
    file = luigi.Parameter()
    size = luigi.Parameter()
    def run(self):
        kernel = pickle.load('/Users/emmanuels/Documents//GitHub/Springboard-DSC/Springboard-DSC/AttributionModel/Data/Probabilities/'+str(self.file.split('/')[10][:-4]+'probabs'+'.pck'))
        #we get samples from the distributions- going to use when simulating MCMC model
        kernel = kernel.sample(int(self.size))
        return kernel.to_csv('/Users/emmanuels/Documents//GitHub/Springboard-DSC/Springboard-DSC/AttributionModel/Data/Probabilities/'+str(self.file.split('/')[10][:-4]+'probabs'+'.csv'))
    def requires(self):
        return wrapper(file = self.file)
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents//GitHub/Springboard-DSC/Springboard-DSC/AttributionModel/Data/Probabilities/'+str(self.file.split('/')[10][:-4]+'probabs'+'.csv'))
class wrapper(luigi.WrapperTask):
    def requires(data):
        files = ['Sessiontolead.csv','leadtoopportunity.csv','opportunitytocomplete.csv']
        task_list = []
        for i in range(0,len(files)):
            file_path = '/Users/emmanuels/Documents/GitHub/Springboard-DSC/Springboard-DSC/AttributionModel/Data/Probabilities/'
            task_list.append(save_distributions(file=file_path+str(files[i])))
        yield task_list
    def run(self):
        print('The wrapper is complete')
        pd.DataFrame().to_csv('/Users/emmanuels/Documents/GitHub/Springboard-DSC/Springboard-DSC/AttributionModel/Data/datawranglerwrapper3.csv')
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/GitHub/Springboard-DSC/Springboard-DSC/AttributionModel/Data/datawranglerwrapper3.csv')
if __name__ == '__main__':
    luigi.build([wrapper()],workers=8,local_scheduler=True)
