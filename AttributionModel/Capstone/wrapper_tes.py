import state_to_state_transitions2 as sst
import pandas as pd
import numpy as np
import luigi
class wrapper(luigi.WrapperTask):
    def requires(self):
        files = ['Session.csv','lead.csv','opportunity.csv','complete.csv']
        task_list = []
        for i in range(1,len(files)):
            path = '/Users/emmanuels/Documents/AttributionData/Data/'
            one = path+str(files[i-1])
            two = path+str(files[i])
            task_list.append(sst.state_to_state(first_file=one,second_file=two))
            return task_list
    def run(self):
        print('Wrapper ran')
        pd.DataFrame().to_csv('/Users/emmanuels/Documents/AttributionData/Data/wrangler1.csv')
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/AttributionData/Data/wrangler1.csv')
if __name__ == '__main__':
    luigi.build([wrapper()], workers=8, local_scheduler=True)
