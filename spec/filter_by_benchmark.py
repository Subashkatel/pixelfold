"""
filter by benchmark
"""
BENCHMARKS = ['perlbench', 'gcc_r', 'mcf_r', 'omnetpp_r', 'xalancbmk_r',
              'x264_r', 'deepsjeng_r', 'leela_r', 'exchange2_r', 'xz_r']

#FOLDERS = ['2big', '2med', '4small', '7big', '7bigmed']
FOLDERS = ['7big']

if __name__ == "__main__":
    for folder in FOLDERS:
        for benchmark in BENCHMARKS:
            INPUT_FILE = f'{folder}/chroot.{folder}.ps2.csv'
            OUTPUT_FILE = f'{folder}/{folder}.{benchmark}.ps2.csv'
            with open(INPUT_FILE, 'r') as raw, open(OUTPUT_FILE, 'w') as csv:
                for line in raw:
                    if "%CPU" in line:
                        csv.write(line)
                    if f'{benchmark}' in line:
                        csv.write(line)
