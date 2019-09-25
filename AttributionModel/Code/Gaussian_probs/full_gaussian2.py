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
#takes n samples and saves sample in csv
class sample_output(luigi.Task):
    file_tag = luigi.Parameter()
    size = luigi.Parameter()
    def run(self):
        kernel = pd.read_pickle('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.file_tag)+'probabs'+'.pck')
        #we get samples from the distributions, going to use when simulating MCMC model
        kernel = kernel.resample(int(self.size))
        pd.DataFrame(kernel).transpose().to_csv('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.file_tag)+'+sampleprobabs'+'.csv')
    def requires(self):
        return save_distributions(file_tag=self.file_tag)
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.file_tag)+'+sampleprobabs'+'.csv')
class state_machine(luigi.Task):
    # read the file with session to lead param
    # one of obs where file is session to lead
    # compare this with random number between 0 & 1
    # if its smaller do nothing, if bigger read the file where we have lead to opp
    # read observation - the one I need to compare
    # compare to 0 & 1 again
    # fails -nothing, succeeds next step
    # 3 copies of function for different state changes
    #this is the monte carlo part
    # session_to_lead
    # save dummy csv for success
    # call leads_to_opps if it succeeds inside session to lead
    file_tag = luigi.Parameter()
    obs_nums = luigi.Parameter() #directly get element - don't write to file
    size = luigi.Parameter()
    def run(self):
        path = '/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'
        file = path+self.file_tag+'sampleprobs.csv'
        def generic_state_machine(tag,file=file,obs_nums=self.obs_nums):
            if file.split('/')[7][:4] == tag:
                statemachine = pd.read_csv(file)
                return statemachine.ix[:,0][obs_nums] > random.uniform(0,1)
        session_to_leads = []
        lead_to_opps = []
        opps_to_comp = []
        session_to_leads.append(generic_state_machine(tag='Sessiontolead+sampleprobabs'))
        lead_to_opps.append(generic_state_machine(tag='leadtoopportunity+sampleprobabs')) if session_to_leads == True else lead_to_opps.append(False)
        opps_to_comp.append(generic_state_machine(tag='opportunitytocomplete+sampleprobabs')) if lead_to_opps == True else opps_to_comp.append(False)
        pd.DataFrame().to_csv('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.file_tag)+'statemachine.csv')
    def requires(self):
        return sample_output(file_tag = self.file_tag,size=self.size) #absolute path not file tag
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.file_tag)+'statemachine'+'.csv') #same thing in output - dependent to obs nums -include in path obs_nums
class wrapper(luigi.WrapperTask):
    def requires(self):
        file_tag = ['Sessiontolead','leadtoopportunity','opportunitytocomplete']
        size = 10000
        task_list = []
        for i in range(0,len(file_tag)):
            for j in range(1,size):
                task_list.append(state_machine(file_tag=file_tag[i],size=size,obs_nums=j))
        return task_list
    def run(self):
        print('The wrapper is complete')
        pd.DataFrame().to_csv('/Users/emmanuels/Documents/AttributionData/Data/Checkpoints/datawranglerwrapper3.csv') #never returns anything
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/AttributionData/Data/Checkpoints/datawranglerwrapper3.csv')
if __name__ == '__main__':
    luigi.build([wrapper()],workers=8,local_scheduler=True)


#file_tag - rename -> consistent
# remove return from run