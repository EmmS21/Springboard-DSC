import luigi
import pandas as pd
import numpy as np
import os
from itertools import chain
from collections import Counter
class ad_probabilities(luigi.Task):
    file = luigi.Parameter()
    def run(self):
        file_read = pd.read_csv(self.file)
        #count occurences of each sequence of transitions
        grouped = (file_read
                  .sort_values(by='ts')
                  .groupby('anonymous_id').utm_source
                  .agg(list)
                  .reset_index()
                  )
        grouped['transitions'] = grouped.utm_source.apply(lambda x: list(zip(x,x[1:])) if len(x) > 1 else list(x))
        all_transitions = Counter(chain(*grouped.transitions.tolist()))
        transitions = pd.DataFrame.from_dict(all_transitions,orient='index').reset_index()
        ad_probabilities = transitions.to_csv('/Users/emmanuels/Documents/GitHub/Springboard-DSC/Springboard-DSC/AttributionModel/Data/Probabilities/total_probabilities.csv')
    def requires(self):
        return []
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/GitHub/Springboard-DSC/Springboard-DSC/AttributionModel/Data/Probabilities/total_probabilities.csv')
class state_to_state(luigi.Task):
    first_file = luigi.Parameter()
    second_file = luigi.Parameter()
    def run(self):
        #iterate through states and find probability of anonymous id existing in next state
        first = pd.read_csv(self.first_file)
        second = pd.read_csv(self.second_file)
        first['probability'] = first.anonymous_id.isin(second.anonymous_id).astype(int)
        #save anonymous id along with probability (1,0) of whether or not it exists in the next state
        state_to_state = first[['anonymous_id','probability']].to_csv('/Users/emmanuels/Documents/GitHub/Springboard-DSC/Springboard-DSC/AttributionModel/Data/Probabilities/'+str(self.first_file.split('/')[9][:-4]+'to'+self.second_file.split('/')[9][:-4]+'.csv'))
    def requires(self):
        return []
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/GitHub/Springboard-DSC/Springboard-DSC/AttributionModel/Data/Probabilities/'+str(self.first_file.split('/')[9][:-4]+'to'+self.second_file.split('/')[9][:-4]+'.csv'))
class wrapper(luigi.WrapperTask):
    def requires(self):
        #list of states
        files = ['Session.csv','lead.csv','opportunity.csv','complete.csv']
        files_two = [ad_probabilities(file='/Users/emmanuels/Desktop/Attribution/finalfullcleanattribution.csv')]
        task_list = []
        for i in range(1,len(files)):
            file_path = '/Users/emmanuels/Documents/GitHub/Springboard-DSC/Springboard-DSC/AttributionModel/Data/'
            first = file_path+str(files[i-1])
            second = file_path+str(files[i])
            task_list.append(state_to_state(first_file=first,second_file=second))
        yield task_list
        yield files_two        
    def run(self):
        print('Wrapper is complete')
        pd.DataFrame().to_csv('/Users/emmanuels/Documents/GitHub/Springboard-DSC/Springboard-DSC/AttributionModel/Data/datawranglerwrapper2.csv')
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/GitHub/Springboard-DSC/Springboard-DSC/AttributionModel/Data/datawranglerwrapper2.csv')
if __name__ == '__main__':
    luigi.build([wrapper()],workers=8,local_scheduler=True)
