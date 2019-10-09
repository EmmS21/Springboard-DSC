import luigi
import pandas as pd
class data_filter(luigi.Task):
    file = luigi.Parameter()
    def run(self):
        file_pd = pd.read_csv(self.file)
        actions = file_pd.state.unique()
        for current in actions:
            filter_file = file_pd.loc[file_pd.state.str.contains(current,na=False)]
            filter_file.to_csv('/Users/emmanuels/Documents/AttributionData/Data/'+str(current)+'.csv')
    def requires(self):
        return []
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/AttributionData/Data/complete.csv')

