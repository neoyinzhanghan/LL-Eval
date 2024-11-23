import os
import time
import random
import pandas as pd
from PIL import Image
from tqdm import tqdm

data_dir = "/media/greg/534773e3-83ea-468f-a40d-46c913378014/neo/results_dir"

# get the list of all subdirectories in the data directory
all_subdirs = [
    d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))
]

# only keep the one that starts with BMA and PBS
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

# save the non-error directories to a csv file at /media/hdd3/neo/non_error_dirs.csv
non_error_dirs_df = pd.DataFrame({"result_dir_path": non_error_dirs})

non_error_dirs_df.to_csv("/media/hdd3/neo/non_error_dirs.csv", index=False)
