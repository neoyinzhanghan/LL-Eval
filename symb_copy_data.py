import os
import pandas as pd
import shutil
from tqdm import tqdm


result_dir = "/media/glv3/hdd1/neo/results_dir"
non_error_pipeline_aggregate_df_path = "pipeline_nonerror_aggregate_df.csv"
save_dir = "/media/hdd3/neo/results_dir_to_copy"

os.makedirs(save_dir, exist_ok=True)    

# read the pipeline_nonerror_aggregate_df.csv file as a dataframe
non_error_pipeline_aggregate_df = pd.read_csv(non_error_pipeline_aggregate_df_path)

# get the result_dir_name column of the non_error_pipeline_aggregate_df as a list
result_dir_names = non_error_pipeline_aggregate_df["result_dir_name"].tolist()

# only keeps the result_dir_names that contain "BMA-diff"
result_dir_names = [
    result_dir_name
    for result_dir_name in result_dir_names
    if "BMA-diff" in result_dir_name
]

for result_dir_name in tqdm(result_dir_names, desc="Getting symbolic link"):
    result_dir_path = os.path.join(result_dir, result_dir_name)
    save_path = os.path.join(save_dir, result_dir_name)
    os.symlink(result_dir_path, save_path)

# shutil copy the pipeline_run_history.csv file to the save_dir
shutil.copy(
    os.path.join(result_dir, "pipeline_run_history.csv"),
    os.path.join(save_dir, "pipeline_run_history.csv"),
)
