import pandas as pd
import luigi
import comparesims as com
class wrapper(luigi.WrapperTask):
    def requires(self):
        file_tag = ['Sessiontolead','leadtoopportunity','opportunitytocomplete']
        size = 20000
        for j in range(1,int(size)):
            return[com.compare(file_tag=i,size=size,obs_nums=j)for i in file_tag]
    def run(self):
        print('The wrapper is complete')
        pd.DataFrame().to_csv('/Users/emmanuels/Documents/AttributionData/Data/datawranglerwrapper3.csv') #never returns anything
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/AttributionData/Data/datawranglerwrapper3.csv')
if __name__ == '__main__':
    luigi.build([wrapper()],workers=8,local_scheduler=True)



# return [sst.state_to_state(first_file=files[i - 1], second_file=files[i]) for i in range(1, len(files))]


# return [sst.state_to_state(first_file=files[i - 1], second_file=files[i]) for i in range(1, len(files))]
