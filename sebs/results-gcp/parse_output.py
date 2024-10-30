"""
parse_output
---------------------------------------------------------------------
This program parses the JSON output from SeBS and creates graphs
"""
import json
import matplotlib.pyplot as plt
import seaborn as sns


#BENCHMARKS = ["120.uploader", "210.thumbnailer", "220.video-processing", "311.compression", "501.graph-pagerank", "502.graph-mst", "503.graph-bfs", "504.dna-visualisation"]
BENCHMARKS = ["120.uploader"]


def main():
    """
    main
    ----------------------------------------------------------
    This function opens a file and parses it to create a graph
    """
    for benchmark in BENCHMARKS:
        jsonBenchmark = benchmark + ".json"
        with open(jsonBenchmark) as json_results:
            fileName = benchmark.replace(".", "_").replace("-", "_")
            parsed = json.load(json_results)
            runs = parsed['_invocations'][f'function-{fileName}_python_3_8']
            x = []
            cold_run = -1
            for run in parsed['_invocations'][f'function-{fileName}_python_3_8']:
                measurement = runs[run]["output"]["result"]["measurement"]
                if runs[run]["output"]["is_cold"]:
                    cold_run = measurement["compute_time"]
                x.append(measurement["compute_time"])
            sns.boxplot(data=[x, x, x])
            plt.show()
            """
            plt.boxplot(data = [x, x])
            if cold_run != -1:
                plt.plot(1, cold_run, 'ro', mfc='none')
            plt.savefig(fileName)
            plt.close()
            """


if __name__ == "__main__":
    main()
