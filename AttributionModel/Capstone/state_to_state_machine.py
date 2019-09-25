import pandas as pd
import numpy as np
import scipy.stats
import pickle
from scipy import stats
import luigi
import random
class state_machine(luigi.Task):
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