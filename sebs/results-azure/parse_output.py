"""
parse_output
---------------------------------------------------------------------
This program parses the JSON output from SeBS and creates graphs
"""
import json
import matplotlib.pyplot as plt


BENCHMARKS = ["120.uploader", "210.thumbnailer", "220.video-processing", "311.compression", "411.image-recognition", "501.graph-pagerank", "502.graph-mst", "503.graph-bfs", "504.dna-visualisation"]


def main():
    """
    main
    ----------------------------------------------------------
    This function opens a file and parses it to create a graph
    """
    for benchmark in BENCHMARKS:
        jsonBenchmark = benchmark + ".json"
        with open(jsonBenchmark) as json_results:
            fileName = benchmark.replace(".", "-")
            parsed = json.load(json_results)
            runs = parsed['_invocations'][f'{fileName}-python-3-8-5ff7ed86']
            x = []
            cold_run = -1
            for run in parsed['_invocations'][f'{fileName}-python-3-8-5ff7ed86']:
                measurement = runs[run]["output"]["result"]["measurement"]
                if runs[run]["output"]["is_cold"]:
                    cold_run = measurement["compute_time"]
                    print("cold")
                x.append(measurement["compute_time"])
            plt.boxplot(x)
            plt.plot(1, cold_run, 'ro', mfc='none')
            plt.savefig(fileName)
            plt.close()


if __name__ == "__main__":
    main()