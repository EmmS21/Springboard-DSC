import numpy as np
import scipy.stats
from scipy import stats
import luigi
class sample_distribution(luigi.Task):
    file = luigi.Parameter()
    def run(self):
        def get_distributions(data=self.file):
            kernel = stats.gaussian_kde(data,bw_method=None)
            class rv(stats.rv_continuous):
                def rvs(self, x):
                    return kernel.sample(n=10000) #random variates
                def cdf(self, x):
                    return kernel.integrate_box_1d(0,max(x)) #Integrate pdf between two bounds (-inf to x here!)
                def pdf(self, x):
                    return kernel.evaluate(x)  #Evaluate the estimated pdf on a provided set of points
            return rv(name='kdedist')
        test_data = sample['probability']
        distribution_data = getDistribution(test_data)
        pdf_data = distribution_data.pdf(test_data)
        pdf_data.to_csv('/Users/emmanuels/Documents/GitHub/Springboard-DSC/Springboard-DSC/AttributionModel/Data/Probabilities/'+str(self.file.split('/')[10][:-4]+'.csv'))
    def requires(self):
        return []
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/GitHub/Springboard-DSC/Springboard-DSC/AttributionModel/Data/Probabilities/'+str(self.file.split('/')[10][:-4]+'.csv'))
class wrapper(luigi.WrapperTask):
    def requires(data):
        files = ['Sessiontolead.csv','leadtoopportunity.csv','opportunitytocomplete.csv']
        task_list = []
        for i in range(1,len(files)):
            file_path = '/Users/emmanuels/Documents/GitHub/Springboard-DSC/Springboard-DSC/AttributionModel/Data/Probabilities/'
            task_list.append(sample_distribution(file=file_path+str(files[i])))
        yield task_list
    def run(self):
        print('The wrapper is complete')
        pd.DataFrame().to_csv('/Users/emmanuels/Documents/GitHub/Springboard-DSC/Springboard-DSC/AttributionModel/Data/datawranglerwrapper3.csv')
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/GitHub/Springboard-DSC/Springboard-DSC/AttributionModel/Data/datawranglerwrapper3.csv')
if __name__ == '__main__':
    luigi.build([wrapper()],workers=8,local_scheduler=True)
