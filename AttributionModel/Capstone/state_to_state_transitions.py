import luigi
import pandas as pd
import numpy as np
import os
from itertools import chain
from collections import Counter
from scipy.stats import gaussian_kde
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