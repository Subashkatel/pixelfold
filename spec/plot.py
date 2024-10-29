"""
plot graph
"""
import csv
import matplotlib.pyplot as pyplot

BENCHMARKS = ['perlbench', 'gcc_r', 'mcf_r', 'omnetpp_r', 'xalancbmk_r',
              'x264_r', 'deepsjeng_r', 'leela_r', 'exchange2_r', 'xz_r']

#FOLDERS = ['2big', '2med', '4small', '7big', '7bigmed']
FOLDERS = ['7big']

if __name__ == "__main__":
    for folder in FOLDERS:
        data = dict()
        OUTPUT_FILE = f'{folder}/{folder}_benchmarks'
        for benchmark in BENCHMARKS:
            INPUT_FILE = f'{folder}/{folder}.{benchmark}.run.csv'
            data[benchmark] = list()
            with open(INPUT_FILE, 'r') as raw:
                reader = csv.DictReader(raw, delimiter=',')
                for line in reader:
                    check = 'CMD'
                    if folder == '2med':
                        check = 'COMMAND'
                    if 'ref' in line[check]:
                        data[benchmark].append(float(line['%CPU']))
            pyplot.plot(range(0, len(data[benchmark])), data[benchmark],
                        label=benchmark)
        pyplot.legend(loc='best')
        pyplot.xlabel('Time (sec)')
        pyplot.ylabel('%CPU usage')
        pyplot.grid(linestyle='--', axis='y')
        pyplot.savefig(OUTPUT_FILE)
        pyplot.close()
