"""
parse_output
---------------------------------------------------------------------
This program parses the JSON output from SeBS and creates graphs
"""
import json
import matplotlib.pyplot as plt


BENCHMARKS = ["120.uploader", "210.thumbnailer", "220.video-processing", "311.compression", "411.image-recognition", "501.graph-pagerank", "502.graph-mst", "503.graph-bfs", "504.dna-visualisation"]

def extract_data(folder, benchmark):
    data = []
    path = folder + "/" + benchmark + ".json"
    with open(path) as json_results:
        fileName = benchmark.replace(".", "_").replace("-", "_")
        if 'azure' in folder:
            fileName = benchmark.replace(".", "-")
        parsed = json.load(json_results)
        extract = ''
        if 'aws' in folder:
            extract = f'{fileName}_python_3_8'
        elif 'azure' in folder:
            extract = f'{fileName}-python-3-8-5ff7ed86'
        else:
            extract = f'function-{fileName}_python_3_8'
        runs = parsed['_invocations'][extract]
        cold_run = -1
        for run in parsed['_invocations'][extract]:
            measurement = runs[run]["output"]["result"]["measurement"]
            if runs[run]["output"]["is_cold"]:
                if measurement["compute_time"] > cold_run:
                    cold_run = measurement["compute_time"]
            data.append(measurement["compute_time"])
    data.append(cold_run)
    return data
    


def main():
    """
    main
    ----------------------------------------------------------
    This function opens a file and parses it to create a graph
    """
    for benchmark in BENCHMARKS:
        gcp = [-1]
        if benchmark != '411.image-recognition':
            gcp = extract_data("results-gcp", benchmark)
        aws = extract_data("results-aws", benchmark)
        azure = extract_data("results-azure", benchmark)
        _, axes = plt.subplots()

        aws_plot = axes.boxplot(aws[:-1], positions=[0],
                                patch_artist=True,
                                boxprops=dict(facecolor="C0"))
        azure_plot = axes.boxplot(azure[:-1], positions=[2],
                                  patch_artist=True,
                                  boxprops=dict(facecolor="C2"))
        if benchmark != '411.image-recognition':
            gcp_plot = axes.boxplot(gcp[:-1], positions=[1], patch_artist=True,
                                    boxprops=dict(facecolor="C3"))
            axes.legend([aws_plot["boxes"][0], gcp_plot["boxes"][0], azure_plot["boxes"][0]], ['aws', 'gcp', 'azure'], loc='best')
        else:
            axes.legend([aws_plot["boxes"][0], azure_plot["boxes"][0]], ['aws', 'azure'], loc='best')

        if aws[-1] != -1:
            plt.plot(0, aws[-1], 'ro', mfc='none')
        if gcp[-1] != -1:
            plt.plot(0, gcp[-1], 'ro', mfc='none')
        if azure[-1] != -1:
            plt.plot(2, azure[-1], 'ro', mfc='none')

        plt.gca().ticklabel_format(axis='y', style='sci', scilimits=(0,0))
        plt.ylabel("Time (µs)")
        plt.title(f"Compute Time for {benchmark}")
        plt.savefig(benchmark.replace(".", "_").replace("-", "_"))
        plt.close()
        axes.clear()


if __name__ == "__main__":
    main()
