"""
spec_graph
-----------------------------------------------------------
Create a bar graph of rates from results of running intrate
test using runcpu2017
-----------------------------------------------------------
INPUTS
  csv file with results
-----------------------------------------------------------
OUTPUTS
  Bar graph
----------------------------------------------------------
USAGE: python3 spec_graph.py
"""
import pandas
from matplotlib import pyplot

if __name__ == "__main__":
    CSV_KVM = 'cores/chroot.7bigmed.first.intrate.csv'
    #CSV_NATIVE = 'cores/chroot.2medcores.first.intrate.csv'
    CSV_NATIVE = 'cpu2017.android.8copy.csv'
    DATA_KVM = pandas.read_csv(CSV_KVM)
    DATA_NATIVE = pandas.read_csv(CSV_NATIVE)
    DATAFRAME_KVM = pandas.DataFrame(DATA_KVM)
    DATAFRAME_NATIVE = pandas.DataFrame(DATA_NATIVE)

    BENCHMARK = DATAFRAME_KVM['Benchmark']
    BASE_RATE_KVM = DATAFRAME_KVM['Base Rate'].to_numpy()
    BASE_RATE_NATIVE = DATAFRAME_NATIVE['Base Rate'].to_numpy()

    COMBINED_DF = pandas.DataFrame({'All Cores': BASE_RATE_NATIVE,
                                   'Big and Medium Cores': BASE_RATE_KVM},
                                   index=BENCHMARK)
    AXES = COMBINED_DF.plot.barh()
    AXES.set_xlabel('Base Rate')
    AXES.set_title('Pixel Fold SPEC Intrate Benchmark')
    pyplot.yticks(rotation=45)
    pyplot.subplots_adjust(left=0.20, bottom=0.15)
    pyplot.savefig("bigmed_native8")
    pyplot.show()
