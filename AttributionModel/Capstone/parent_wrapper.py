import pandas as pd
import numpy as np
import scipy.stats
import pickle
from scipy import stats
import luigi
import random
import state_to_state_machine as ssm
class wrapper(luigi.WrapperTask):
    def requires(self):
        file_tag = ['Sessiontolead','leadtoopportunity','opportunitytocomplete']
        size = 10000
        task_list = []
        for i in range(0,len(file_tag)):
            for j in range(1,size):
                task_list.append(ssm.state_machine(file_tag=file_tag[i],size=size,obs_nums=j))
        return task_list
    def run(self):
        print('The wrapper is complete')
        pd.DataFrame().to_csv('/Users/emmanuels/Documents/AttributionData/Data/Checkpoints/datawranglerwrapper3.csv') #never returns anything
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/AttributionData/Data/Checkpoints/datawranglerwrapper3.csv')
if __name__ == '__main__':
    luigi.build([wrapper()],workers=8,local_scheduler=True)

