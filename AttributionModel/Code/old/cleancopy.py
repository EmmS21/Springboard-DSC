#categorise unique user actions into separate csv files
import luigi
import pandas as pd
import numpy as np
import os
class data_filter(luigi.Task):
        task = luigi.Parameter()
        def run(self):
                full_file = pd.read_csv('/Users/emmanuels/Desktop/Attribution/finalfullcleanattribution.csv')
                data_filter = full_file.loc[full_file.state.str.contains(self.task, na=False)]
                data_filter.to_csv('/Users/emmanuels/Documents/GitHub/Springboard-DSC/Springboard-DSC/AttributionModel/Data/'+str(self.task)+'.csv')
        def requires(self):
                return []
        def output(self):
                return luigi.LocalTarget('/Users/emmanuels/Documents/GitHub/Springboard-DSC/Springboard-DSC/AttributionModel/Data/'+str(self.task)+'.csv')
#chaining tasks with wrapper
class wrapper(luigi.WrapperTask):
        def requires(self):
                file = pd.read_csv('/Users/emmanuels/Desktop/Attribution/finalfullcleanattribution.csv')
                actions = file.state.unique()
                task_list = []
                for current_task in actions:
                        task_list.append(data_filter(task=current_task))
                return task_list
        def run(self):
                print ('Wrapper has ended')
                pd.DataFrame().to_csv('/Users/emmanuels/Documents/GitHub/Springboard-DSC/Springboard-DSC/AttributionModel/Data/datawranglerwrapper.csv') 
        def output(self):
                return luigi.LocalTarget('/Users/emmanuels/Documents/GitHub/Springboard-DSC/Springboard-DSC/AttributionModel/Data/datawranglerwrapper.csv') 
if __name__ == '__main__':
    luigi.build([wrapper()],workers=8,local_scheduler=True)








