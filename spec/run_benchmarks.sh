#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# All available benchmarks
BENCHMARKS=(
    "110.dynamic-html"
    "120.uploader"
    "210.thumbnailer"
    "220.video-processing"
    "311.compression"
    "411.image-recognition"
    "501.graph-pagerank"
    "502.graph-mst"
    "503.graph-bfs"
    "504.dna-visualisation"
)

# Check if platform parameter is provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: Platform parameter is required${NC}"
    echo "Usage: $0 <platform> [specific_benchmark]"
    exit 1
fi

PLATFORM=$1
SPECIFIC_BENCHMARK=$2
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESULTS_DIR="results-${PLATFORM}-${TIMESTAMP}"

# Create main results directory
mkdir -p "$RESULTS_DIR"

run_benchmark() {
    local benchmark=$1
    echo -e "\n${YELLOW}=====================================${NC}"
    echo -e "${GREEN}Running benchmark: ${benchmark}${NC}"
    echo -e "${YELLOW}=====================================${NC}"
    
    local OUTPUT_DIR="${RESULTS_DIR}/${benchmark}"
    mkdir -p "$OUTPUT_DIR"
    
    # Run the benchmark and capture both stdout and stderr
    ./sebs.py benchmark invoke $benchmark test \
        --config config/local_deployment.json \
        --deployment $PLATFORM \
        --repetitions 50 \
        --verbose \
        --output-dir "$OUTPUT_DIR" 2>&1 | tee "${OUTPUT_DIR}/benchmark.log"
    
    if [ -e "${OUTPUT_DIR}/experiments.json" ]; then
        echo -e "${GREEN}✓ Results saved to ${OUTPUT_DIR}/experiments.json${NC}"
    else
        echo -e "${RED}✗ Error: experiments.json not found for benchmark $benchmark${NC}"
        echo "Check ${OUTPUT_DIR}/benchmark.log for details"
    fi
}

# Print start time
echo -e "${GREEN}Starting benchmark run at $(date)${NC}"
echo -e "${GREEN}Results will be saved in: ${RESULTS_DIR}${NC}"

if [ -n "$SPECIFIC_BENCHMARK" ]; then
    if [[ " ${BENCHMARKS[@]} " =~ " ${SPECIFIC_BENCHMARK} " ]]; then
        run_benchmark "$SPECIFIC_BENCHMARK"
    else
        echo -e "${RED}Error: Benchmark $SPECIFIC_BENCHMARK not found in the list of available benchmarks.${NC}"
        echo "Available benchmarks:"
        printf '%s\n' "${BENCHMARKS[@]}"
        exit 1
    fi
else
    # Run all benchmarks
    for benchmark in "${BENCHMARKS[@]}"; do
        run_benchmark "$benchmark"
    done
fi

# Print summary
echo -e "\n${YELLOW}=====================================${NC}"
echo -e "${GREEN}Benchmark run completed at $(date)${NC}"
echo -e "${GREEN}Results saved in: ${RESULTS_DIR}${NC}"
echo -e "${YELLOW}=====================================${NC}"
