#takes n samples and saves sample in csv
class sample_output(luigi.Task):
    file_tag = luigi.Parameter()
    size = luigi.Parameter()
    def run(self):
        kernel = pd.read_pickle('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.file_tag)+'probabs'+'.pck')
        #we get samples from the distributions, going to use when simulating MCMC model
        kernel = kernel.resample(int(self.size))
        pd.DataFrame(kernel).transpose().to_csv('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.file_tag)+'+sampleprobabs'+'.csv')
    def requires(self):
        return save_distributions(file_tag=self.file_tag)
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.file_tag)+'+sampleprobabs'+'.csv')