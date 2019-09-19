#takes n samples and saves sample in csv
class sample_output(luigi.Task):
    file = luigi.Parameter()
    size = luigi.Parameter()
    def run(self):
        kernel = pickle.load('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.file.split('/')[10][:-4]+'probabs'+'.pck'))
        #we get samples from the distributions- going to use when simulating MCMC model
        kernel = kernel.sample(int(self.size))
        return kernel.to_csv('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.file.split('/')[10][:-4]+'probabs'+'.csv'))
    def requires(self):
        return wrapper(file = self.file)
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'+str(self.file.split('/')[10][:-4]+'probabs'+'.csv'))