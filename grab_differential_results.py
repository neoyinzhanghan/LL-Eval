import os
import time
import random
import pandas as pd
from PIL import Image
from tqdm import tqdm
from LLRunner.config import pipeline_run_history_path

data_dir = "/media/hdd3/neo/results_dir"


def get_slide_bar_code(pipeline_result_dir):
    df = pd.read_csv(pipeline_run_history_path)

    # get the folder name from the pipeline_result_dir
    folder_name = os.path.basename(pipeline_result_dir)

    pipeline = folder_name.split("_")[0]
    datetime_processed = folder_name.split("_")[1]

    # look for the row in the dataframe that has the same pipeline and datetime_processed
    row = df[
        (df["pipeline"] == pipeline) & (df["datetime_processed"] == datetime_processed)
    ]

    # assert that exactly one row is found
    assert len(row) == 1, f"Expected 1 row, but got {len(row)} rows"

    # return the value of the wsi_name column in the row
    return row["wsi_name"].values[0]


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

all_cell_paths = []
for result_dir_path in tqdm(all_result_dir_paths, desc="Filtering out error dirs:"):
    # check if the result_dir_path contains a file called "error.txt"
    if not os.path.exists(os.path.join(result_dir_path, "error.txt")):
        non_error_dirs.append(result_dir_path)

        wsi_name = get_slide_bar_code(result_dir_path)

        print(wsi_name)

    else:
        num_errors += 1

print(f"Number of error dirs: {num_errors}")
print(f"Number of non-error dirs: {len(non_error_dirs)}")
