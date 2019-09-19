class wrapper(luigi.WrapperTask):
    def requires(data):
        files = ['Sessiontolead.csv','leadtoopportunity.csv','opportunitytocomplete.csv']
        task_list = []
        for i in range(1,len(files)):
            file_path = '/Users/emmanuels/Documents/GitHub/Springboard-DSC/Springboard-DSC/AttributionModel/Data/Probabilities/'
            task_list.append(save_distributions(file=file_path+str(files[i])))
        yield task_list
    def run(self):
        print('The wrapper is complete')
        pd.DataFrame().to_csv('/Users/emmanuels/Documents/GitHub/Springboard-DSC/Springboard-DSC/AttributionModel/Data/datawranglerwrapper3.csv')
    def output(self):
        return luigi.LocalTarget('/Users/emmanuels/Documents/GitHub/Springboard-DSC/Springboard-DSC/AttributionModel/Data/datawranglerwrapper3.csv')
if __name__ == '__main__':
    luigi.build([wrapper()],workers=8,local_scheduler=True)