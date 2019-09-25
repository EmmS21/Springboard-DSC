import luigi
import pandas as pd
import numpy as np
import os
class data_filter(luigi.Task):
        full_file = pd.read_csv('/Users/emmanuels/Desktop/Attribution/finalfullcleanattribution.csv')
        def run(self):
            def split(task,full_file=self.full_file):
                full_file = pd.read_csv('/Users/emmanuels/Desktop/Attribution/finalfullcleanattribution.csv')
                data_filter = full_file.loc[full_file.state.str.contains(self.task, na=False)]
                return data_filter.to_csv('/Users/emmanuels/Documents/AttributionData/Data/'+str(task)+'.csv')
            actions = full_file.state.unique()
            for current_task in actions:
                split(task=current_task)