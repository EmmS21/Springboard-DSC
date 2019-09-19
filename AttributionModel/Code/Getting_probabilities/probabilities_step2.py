import luigi
import pandas as pd
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
