import luigi
import pandas as pd
import numpy as np
import os
from itertools import chain
from collections import Counter
from scipy.stats import gaussian_kde
import probabilities_step1
import probabilities_step2
class wrapper(luigi.WrapperTask):
    def requires(self):
        #list of states
        files = ['Session.csv','lead.csv','opportunity.csv','complete.csv']
        files_two = [ad_probabilities(file='/Users/emmanuels/Desktop/Attribution/finalcleanattributiondata.csv')]
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
