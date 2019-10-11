import luigi
import pandas as pd
from itertools import chain
from collections import Counter
import separate_csv as sep
class ad_probabilities(luigi.Task):
    file = luigi.Parameter()
    source = luigi.Parameter()
    def run(self):
        path = '/Users/emmanuels/Documents/AttributionData/Data/'
        file_read = pd.read_csv(path+self.file)
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
        ad_probabilities = transitions.to_csv('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/total_probabilities.csv')
    def requires(self):
        return [sep.data_filter(file='/Users/emmanuels/Desktop/Attribution/finalcleanattributiondata.csv',source=self.source)]
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/total_probabilities.csv')