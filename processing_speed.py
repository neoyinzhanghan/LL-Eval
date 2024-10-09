import os
import time
import random
import pandas as pd
from PIL import Image
from tqdm import tqdm

data_dir = "/media/hdd3/neo/results_dir"

# get the list of all subdirectories in the data directory
all_subdirs = [
    d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))
]

# onlu keep the one that starts with BMA and PBS
result_dirs = [d for d in all_subdirs if "BMA-diff" in d or "PBS-diff" in d]

all_result_dir_paths = [os.path.join(data_dir, d) for d in result_dirs]

num_errors = 0
num_dirs = len(all_result_dir_paths)
non_error_dirs = []
error_dirs = []

all_cell_paths = []
for result_dir_path in tqdm(all_result_dir_paths, desc="Filtering out error dirs:"):
    # check if the result_dir_path contains a file called "error.txt"
    if not os.path.exists(os.path.join(result_dir_path, "error.txt")):
        non_error_dirs.append(result_dir_path)

    else:
        error_dirs.append(result_dir_path)
        num_errors += 1

print(f"Number of error dirs: {num_errors}")
print(f"Number of non-error dirs: {len(non_error_dirs)}")

bma_runtimes = []
pbs_runtimes = []

for non_error_dir in tqdm(non_error_dirs, desc="Extracting error messages:"):
    runtime_csv_path = os.path.join(non_error_dir, "runtime_data.csv")
    runtime_df = pd.read_csv(runtime_csv_path, header=None, index_col=0)

    runtime = int(runtime_df.loc["total_non_hoarding_time", 1])

    if "BMA-diff" in non_error_dir:
        bma_runtimes.append(runtime)
    else:
        pbs_runtimes.append(runtime)


print(f"Average runtime for BMA: {sum(bma_runtimes)/len(bma_runtimes)}")
print(f"Average runtime for PBS: {sum(pbs_runtimes)/len(pbs_runtimes)}")
