import pandas as pd
import state_to_state_machine as ssm
import luigi
import random
class compare(luigi.Task):
    file_tag = luigi.Parameter()
    ppltn_file = luigi.Parameter()
    def run(self):
        file_tag
        monte_carlo = '/Users/emmanuels/Documents/AttributionData/Data/fullmcsims.csv'
        sims = pd.read_csv(monte_carlo, index_col=0)
        def func(sims, tag, col_name):
            sims *= 1
            path = '/Users/emmanuels/Documents/AttributionData/Data/Probabilities/'
            actuals = pd.read_pickle(path + tag + '.pck')
            y = np.linspace(start=stats.norm.ppf(0.1), stop=stats.norm.ppf(0.99), num=100)
            fig, ax = plt.subplots()
            ax.plot(y, actuals.pdf(y), linestyle='dashed', c='red', lw=2, alpha=0.8)
            ax.set_title(tag + ' Stats v Actual comparison', fontsize=15)
            # sims plot
            ax_two = ax.twinx()
            # simulations
            ax_two = plt.hist(sims[col_name])
            return fig.savefig(path + str(tag) + '.png')

        for actual, cols in zip(files, sims_list):
            #     print(val1,val2)
            func(sims=sims, tag=str(actual), col_name=str(cols))


        path = '+sampleprobabs'

# save state to file
# create another luigi class to read
# will compare simulated to original population
# read last state of customers in simulated ppltn
# read actual ppltn data
# create hist of those two in the same graph
# if customer fails first then others will be false all the time -> exclude this part of ppltn from histogram, exclude ones that failed previous stages in current
# e.g if failed in state 1 exclude in state 2
# when rolling dice failed - in which state was customer in
# seeing if our simulation is correct - we want to be able mimic the actual data, compare with real data, if we can't we forgot something
# if success we add filters and start simulating