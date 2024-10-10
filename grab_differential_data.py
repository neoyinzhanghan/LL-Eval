import os
import time
import random
import pandas as pd
from PIL import Image
from tqdm import tqdm
from get_copath_data import get_diff, get_path_data
from LLRunner.config import pipeline_run_history_path

non_error_dir_csv_path = "/media/hdd3/neo/non_error_dirs.csv"


def get_pipeline(pipeline_result_dir):
    return os.path.basename(pipeline_result_dir).split("_")[0]


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


# turn the result_dir_path column into a list
non_error_dirs_df = pd.read_csv(non_error_dir_csv_path)
non_error_dirs = non_error_dirs_df["result_dir_path"].tolist()

accession_numbers = []
for result_dir_path in tqdm(non_error_dirs, desc="Extracting accession numbers:"):
    wsi_name = get_slide_bar_code(result_dir_path)
    accession_number = wsi_name.split("_")[0]
    accession_numbers.append(accession_number)

print("Getting copath data from database...")
copath_df = get_path_data(accession_numbers)
print("Extracting differential data from copath data...")
diff_df = get_diff(accession_numbers)

# save the copath_df and diff_df to csv files
copath_df.to_csv("/media/hdd3/neo/copath_data_2024-10-09.csv", index=False)
diff_df.to_csv("/media/hdd3/neo/differential_data_2024-10-09.csv", index=False)
