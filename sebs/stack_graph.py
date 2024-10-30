"""
parse_output
---------------------------------------------------------------------
This program parses the JSON output from SeBS and creates graphs
"""
import json
import matplotlib.pyplot as plt


BENCHMARKS = ["120.uploader", "210.thumbnailer", "220.video-processing",
              "311.compression", "411.image-recognition", "501.graph-pagerank",
              "502.graph-mst", "503.graph-bfs", "504.dna-visualisation"]


def extract_data(folder, benchmark):
    """
    Extract compute time from json file
    """
    data = []
    path = folder + "/" + benchmark + ".json"
    try:
        with open(path) as json_results:
            file_name = benchmark.replace(".", "_").replace("-", "_")
            parsed = json.load(json_results)
            extract = ''
            if 'aws' in folder:
                extract = f'{file_name}_python_3_8'
            elif 'azure' in folder:
                file_name = benchmark.replace(".", "-")
                extract = f'{file_name}-python-3-8-5ff7ed86'
            elif 'gcp' in folder:
                extract = f'function-{file_name}_python_3_8'
            elif 'kvm' in folder:
                extract = f'{benchmark}-python-3.7'
            runs = parsed['_invocations'][extract]
            cold_run = -1
            for run in parsed['_invocations'][extract]:
                measurement = runs[run]["output"]["result"]["measurement"] if 'kvm' not in folder else runs[run]["output"]["result"]["output"]["measurement"]
                if runs[run]["output"]["is_cold"]:
                    if measurement["compute_time"] > cold_run:
                        cold_run = measurement["compute_time"]
                data.append(measurement["compute_time"])
        data.append(cold_run)
        return data
    except FileNotFoundError:
        print(f"File not found {path}")
        return []


def main():
    """
    main
    ----------------------------------------------------------
    This function opens a file and parses it to create a graph
    """
    for benchmark in BENCHMARKS:
        gcp = extract_data("results-gcp", benchmark)
        aws = extract_data("results-aws", benchmark)
        azure = [] #extract_data("results-azure", benchmark)
        kvm = extract_data("results-kvm", benchmark)
        _, axes = plt.subplots()

        label = []
        names = []
        if len(aws) != 0:
            aws_plot = axes.boxplot(aws[:-1], positions=[0],
                                    patch_artist=True,
                                    boxprops=dict(facecolor="C0"))
            label.append(aws_plot["boxes"][0])
            names.append("aws")
            if aws[-1] != -1:
                plt.plot(0, aws[-1], 'ro', mfc='none')
        if len(gcp) != 0:
            gcp_plot = axes.boxplot(gcp[:-1], positions=[1], patch_artist=True,
                                    boxprops=dict(facecolor="C3"))
            label.append(gcp_plot["boxes"][0])
            names.append("gcp")
            if gcp[-1] != -1:
                plt.plot(1, gcp[-1], 'ro', mfc='none')
        if len(azure) != 0:
            azure_plot = axes.boxplot(azure[:-1], positions=[2],
                                      patch_artist=True,
                                      boxprops=dict(facecolor="C2"))
            label.append(azure_plot["boxes"][0])
            names.append("azure")
            if azure[-1] != -1:
                plt.plot(2, azure[-1], 'ro', mfc='none')
        if len(kvm) != 0:
            kvm_plot = axes.boxplot(kvm[:-1], positions=[2],
                                    patch_artist=True,
                                    boxprops=dict(facecolor="C4"))
            label.append(kvm_plot["boxes"][0])
            names.append("kvm")
            if kvm[-1] != -1:
                plt.plot(2, kvm[-1], 'ro', mfc='none')

        axes.legend(label, names, loc='best')

        plt.gca().ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        plt.ylabel("Time (µs)")
        plt.xlabel("Memory (MB)")
        plt.title(f"Compute Time for {benchmark}")
        plt.grid(linestyle='--')

        if benchmark == '120.uploader':
            plt.xticks([0, 1, 2], ['512', '128', '2048'])
        elif benchmark == '210.thumbnailer':
            plt.xticks([0, 1, 2], ['256', '256', '2048'])
        elif benchmark == '220.video-processing':
            plt.xticks([0, 1, 2], ['512', '512', '2048'])
        elif benchmark == '311.compression':
            plt.xticks([0, 1, 2], ['512', '256', '2048'])
        elif benchmark == '411.image-recognition':
            plt.xticks([0], ['512'])
        elif benchmark == '501.graph-pagerank':
            plt.xticks([0, 1], ['512', '512'])
        elif benchmark == '502.graph-mst':
            plt.xticks([0, 1], ['512', '512'])
        elif benchmark == '503.graph-bfs':
            plt.xticks([0, 1], ['512', '512'])
        elif benchmark == '504.dna-visualisation':
            plt.xticks([0, 1, 2], ['2048', '2048', '2048'])
        plt.savefig(benchmark.replace(".", "_").replace("-", "_"))
        plt.close()
        axes.clear()


if __name__ == "__main__":
    main()
