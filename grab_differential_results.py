import os
import csv
import time
import random
import pandas as pd
from PIL import Image
from tqdm import tqdm
from LLRunner.config import pipeline_run_history_path


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


omitted_classes = ["ER5", "ER6", "U4"]
removed_classes = ["U1", "PL2", "PL3"]

cellnames_to_keep = [cell for cell in cellnames if cell not in omitted_classes]
cellnames_to_keep = [cell for cell in cellnames_to_keep if cell not in removed_classes]

differential_df_dct = {
    "wsi_name": [],
    "result_dir_path": [],
}

for cellname in cellnames_to_keep:
    differential_df_dct[cellname] = []


def create_mapping_from_csv(file_path):
    mapping = {}
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            # Ensure there are at least two columns and parse them correctly
            if len(row) >= 2:
                key = row[0].strip()
                try:
                    value = float(row[1].strip())
                    mapping[key] = value
                except ValueError:
                    print(f"Invalid float value for {key}: {row[1]}")

    for cellname in cellnames_to_keep:
        if cellname not in mapping:
            mapping[cellname] = 0.0

    return mapping


def get_differential_dict_from_result_dir(pipeline_result_dir):

    # first make sure that the pipeline_result_dir is BMA-diff
    assert (
        "BMA-diff" in pipeline_result_dir
    ), f"Expected BMA-diff in {pipeline_result_dir}"

    csv_path = os.path.join(pipeline_result_dir, "differential_class.csv")

    # now remove all the classes that are in the omitted_classes and removed_classes
    mapping = create_mapping_from_csv(csv_path)

    for omitted_class in omitted_classes:
        mapping.pop(omitted_class, None)

    for removed_class in removed_classes:
        mapping.pop(removed_class, None)

    # renormalize the probabilities in the mapping
    total_prob = sum(mapping.values())

    for key in mapping:
        mapping[key] = mapping[key] / total_prob

    return mapping


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
for result_dir_path in tqdm(
    all_result_dir_paths, desc="Filtering out error dirs and processing differential:"
):
    # check if the result_dir_path contains a file called "error.txt"
    if not os.path.exists(os.path.join(result_dir_path, "error.txt")):
        non_error_dirs.append(result_dir_path)

        if "BMA-diff" in result_dir_path:
            wsi_name = get_slide_bar_code(result_dir_path)

            differential_dict = get_differential_dict_from_result_dir(result_dir_path)

            differential_df_dct["wsi_name"].append(wsi_name)
            differential_df_dct["result_dir_path"].append(result_dir_path)
            for cellname in cellnames_to_keep:
                differential_df_dct[cellname].append(differential_dict[cellname])

    else:
        num_errors += 1

print(f"Number of error dirs: {num_errors}")
print(f"Number of non-error dirs: {len(non_error_dirs)}")

differential_df = pd.DataFrame(differential_df_dct)

differential_df.to_csv("/media/hdd3/neo/test_differential_df.csv", index=False)
