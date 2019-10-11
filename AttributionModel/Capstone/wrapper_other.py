import gaussian_kdefit as gkde
import state_to_state_transitions2  as st
import separate_csv as sep
import pandas as pd
import luigi
class wrapper(luigi.WrapperTask):
    def requires(self):
        files_two = [sep.data_filter(file='/Users/emmanuels/Desktop/Attribution/finalcleanattributiondata.csv')]
        return files_two
    def run(self):
        pd.DataFrame().to_csv('/Users/emmanuels/Documents/AttributionData/Data/wrangler1.csv')
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/AttributionData/Data/wrangler1.csv')
if __name__ == '__main__':
    luigi.build([wrapper()],workers=8,local_scheduler=True)


