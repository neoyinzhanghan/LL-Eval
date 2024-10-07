import os
import time
import random
import pandas as pd
from PIL import Image
from tqdm import tqdm
data_dir = "/media/hdd3/neo/results_dir"

# get the list of all subdirectories in the data directory
all_subdirs = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]

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

print (f"Number of error dirs: {num_errors}")
print (f"Number of non-error dirs: {len(non_error_dirs)}")

error_df_dict = {
    "result_dir_name": [],
    "error_message": [],
    "specimen_type": [],
}

for error_dir in tqdm(error_dirs, desc="Extracting error messages:"):
    with open(os.path.join(error_dir, "error.txt"), "r") as f:
        error_message = f.read()
    
    error_df_dict["result_dir_name"].append(os.path.basename(error_dir))
    error_df_dict["error_message"].append(error_message)
    error_df_dict["specimen_type"].append("BMA" if "BMA-diff" in error_dir else "PBS")

error_df = pd.DataFrame(error_df_dict)

# save the error dataframe to a csv file at /media/hdd3/neo/pipeline_error_df.csv
error_df.to_csv("/media/hdd3/neo/pipeline_error_df.csv", index=False) 
