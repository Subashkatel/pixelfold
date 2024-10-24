#! /bin/bash

#BENCHMARKS=("110.dynamic-html" "120.uploader" "210.thumbnailer" "220.video-processing" "311.compression" "411.image-recognition" "501.graph-pagerank" "502.graph-mst" "503.graph-bfs" "504.dna-visualisation")
BENCHMARKS=("220.video-processing" "411.image-recognition" "504.dna-visualisation")

PLATFORM=$1

mkdir -p "results-${PLATFORM}"

run_benchmark () {
  local benchmark=$1
  if [ "$benchmark" == "311.compression" ]; then
    ./sebs.py benchmark invoke $benchmark test --config config/example.json --deployment $PLATFORM --repetitions 25 --verbose --output-dir $benchmark
  else
    ./sebs.py benchmark invoke $benchmark test --config config/example.json --deployment $PLATFORM --repetitions 50 --verbose --output-dir $benchmark
  fi
  if [ -e "${benchmark}/experiments.json" ]; then
    mv "${benchmark}/experiments.json" "results-${PLATFORM}"/"${benchmark}.json"
    rm -rf $benchmark
  fi
}

for benchmark in ${BENCHMARKS[@]}; do
  if [ "$benchmark" == "411.image-recognition" ] && [ "$PLATFORM" == "gcp" ]; then
    continue
  else
    run_benchmark $benchmark &
  fi
done

wait
