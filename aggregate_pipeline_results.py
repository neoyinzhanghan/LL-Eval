import os
import time
import random
import pandas as pd
from PIL import Image
from tqdm import tqdm
data_dir = "/media/hdd3/neo/results_dir"

cellnames = [
    "B1",
    "B2",
    "E1",
    "E4",
    "ER1",
    "ER2",
    "ER3",
    "ER4",
    "ER5",
    "ER6",
    "L2",
    "L4",
    "M1",
    "M2",
    "M3",
    "M4",
    "M5",
    "M6",
    "MO2",
    "PL2",
    "PL3",
    "U1",
    "U4",
]

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

nonerror_df_dict = {
    "result_dir_name": [],
    "num_cells": [],
    "num_regions": [],
    "specimen_type": [],
}

for cell_name in cellnames:
    nonerror_df_dict[str("num"+cell_name)] = []

for non_error_dir in tqdm(non_error_dirs, desc="Gathering aggregate pipeline results for non-error directories"):
    specimen_type = "BMA" if "BMA-diff" in non_error_dir else "PBS"

    cell_detection_csv_path = os.path.join(non_error_dir,"cells" , "cell_detection.csv")

    cell_det_df = pd.read_csv(cell_detection_csv_path, header=None, index_col=0)

    num_cells_detected = int(cell_det_df.loc["num_cells_detected", 1])
    num_focus_regions_scanned = int(cell_det_df.loc["num_focus_regions_scanned", 1])

    nonerror_df_dict["result_dir_name"].append(os.path.basename(non_error_dir))
    nonerror_df_dict["num_cells"].append(num_cells_detected)
    nonerror_df_dict["num_regions"].append(num_focus_regions_scanned)
    nonerror_df_dict["specimen_type"].append(specimen_type)

    for cell_name in cellnames:
        cellclass_path = os.path.join(non_error_dir, "cells", cell_name)

        # if the directory for the cell class exists
        if os.path.exists(cellclass_path):
            cellclass_dir = os.listdir(cellclass_path)
            # only keep the jpg files
            cellclass_jpgs = [f for f in cellclass_dir if f.endswith(".jpg")]

            nonerror_df_dict[str("num"+cell_name)].append(len(cellclass_jpgs))
        else:
            nonerror_df_dict[str("num"+cell_name)].append(0)

nonerror_df = pd.DataFrame(nonerror_df_dict)

# save the non-error dataframe to a csv file at /media/hdd3/neo/pipeline_nonerror_aggregate_df.csv
nonerror_df.to_csv("/media/hdd3/neo/pipeline_nonerror_aggregate_df.csv", index=False)