import pandas as pd
import get_samples as gs
import luigi
import random
class state_machine(luigi.Task):
    obs_nums = luigi.Parameter() #directly get element - don't write to file
    size = luigi.Parameter()
    def run(self):
        path = '/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'

        def generic_state_machine(obs_nums,tag):
            #if file.split('/')[7][:-4] == tag:
            file = path +tag+'.csv'
            state_machine = pd.read_csv(file)
            if state_machine.ix[:,1][obs_nums] > random.uniform(0,1):
                return True
            else:
                return False

        session_to_leads = generic_state_machine(obs_nums=self.obs_nums,tag='Sessiontolead+sampleprobabs')
        lead_to_opps = False
        opps_to_comp = False
        if session_to_leads != False:
            lead_to_opps = generic_state_machine(obs_nums=self.obs_nums, tag='leadtoopportunity+sampleprobabs')

        if lead_to_opps != False:
            opps_to_comp = generic_state_machine(obs_nums=self.obs_nums, tag='opportunitytocomplete+sampleprobabs')
        output_df = pd.DataFrame([[session_to_leads],[lead_to_opps],[opps_to_comp]]).transpose()
        output_df.columns = ['session_to_leads','lead_to_opps','oops_to_comp']
        output_df.to_csv('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/sims/'+str(self.obs_nums)+'statemachine.csv')
    def requires(self):
        return [gs.sample_output(file_tag='Sessiontolead',size=self.size),
                gs.sample_output(file_tag='leadtoopportunity',size=self.size),
                gs.sample_output(file_tag='opportunitytocomplete',size=self.size)]
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/sims/'+str(self.obs_nums)+'statemachine.csv')

        #same thing in output - dependent to obs nums -include in path obs_nums


