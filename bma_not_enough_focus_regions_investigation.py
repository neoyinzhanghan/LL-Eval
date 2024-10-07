import os
import time
import random
import shutil
import pandas as pd
from PIL import Image
from tqdm import tqdm
data_dir = "/media/hdd3/neo/results_dir"

# get the list of all subdirectories in the data directory
all_subdirs = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]

# onlu keep the one that starts with BMA and PBS
result_dirs = [d for d in all_subdirs if "BMA-diff" in d or "PBS-diff" in d]

all_result_dir_paths = [os.path.join(data_dir, d) for d in result_dirs]


save_dir = "/media/hdd3/neo/not_enough_focus_regions_topviews"
os.makedirs(save_dir, exist_ok=True)
os.makedirs(os.path.join(save_dir, "BMA_grid_rep"), exist_ok=True)
os.makedirs(os.path.join(save_dir, "BMA_heat_map", "topviews"), exist_ok=True)


num_errors = 0
num_dirs = len(all_result_dir_paths)
non_error_dirs = []
error_dirs = []

all_cell_paths = []
for result_dir_path in tqdm(all_result_dir_paths, desc="Filtering out error dirs and gathering topviews:"):
    # check if the result_dir_path contains a file called "error.txt"
    if not os.path.exists(os.path.join(result_dir_path, "error.txt")):
        non_error_dirs.append(result_dir_path)

    else:
        error_dirs.append(result_dir_path)

        # error message is read from the error.txt file
        with open(os.path.join(result_dir_path, "error.txt"), "r") as f:
            error_message = f.read()
        
        error_message = str(error_message)

        # check if the error message contains the string "Too few focus regions found."
        if "Too few focus regions found." in error_message:
            topview_grid_rep_path = os.path.join(result_dir_path, "top_view_grid_rep.png")
            topview_heat_map_path = os.path.join(result_dir_path, "confidence_heatmap.png")

            # copy the topview_grid_rep.png and topview_heat_map.png to the save_dir using shutil.copy
            shutil.copy(topview_grid_rep_path, os.path.join(save_dir, "BMA_grid_rep", os.path.basename(result_dir_path) + ".png"))
            shutil.copy(topview_heat_map_path, os.path.join(save_dir, "BMA_heat_map", "topviews", os.path.basename(result_dir_path) + ".png"))
        num_errors += 1

print (f"Number of error dirs: {num_errors}")
print (f"Number of non-error dirs: {len(non_error_dirs)}")