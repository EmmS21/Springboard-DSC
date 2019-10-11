import pandas as pd
import luigi
import glob
import state_to_state_machine as ssm
class wrapper(luigi.WrapperTask):
    source = luigi.Parameter()
    def requires(self):
        size = 100
        return[ssm.state_machine(size=size,obs_nums=i,source=self.source)for i in range(0, size)]
    def run(self):
        full_mc_sim = pd.concat([pd.read_csv(f, index_col=0) for f in glob.glob('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/sims/*statemachine.csv')])
        full_mc_sim.to_csv('/Users/emmanuels/Documents/AttributionData/Data/fullmcsims.csv')
        # pd.DataFrame().to_csv('/Users/emmanuels/Documents/AttributionData/Data/datawranglerwrapper3.csv') #never returns anything
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/AttributionData/Data/fullmcsims.csv')
if __name__ == '__main__':
    luigi.build([wrapper(source = 'facebook')],workers=8,local_scheduler=True)



# return [sst.state_to_state(first_file=files[i - 1], second_file=files[i]) for i in range(1, len(files))]


# return [sst.state_to_state(first_file=files[i - 1], second_file=files[i]) for i in range(1, len(files))]



#external parameters
#filter