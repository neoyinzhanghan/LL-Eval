import os
import csv
import pandas as pd
from tqdm import tqdm


def csv_to_dict(file_path: str) -> dict:
    result_dict = {}
    with open(file_path, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:  # Ensure there are exactly two columns
                key, value = row[0], int(row[1])
                result_dict[key] = value
    return result_dict


Dx_metadata_path = "/media/hdd3/neo/MDS_all_wsi_names.csv"
dx_df = pd.read_csv(Dx_metadata_path)


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

group_names = [
    "blast",
    "blast-equivalents",
    "promyelocytes",
    "myelocytes",
    "metamyelocytes",
    "neutrophils/bands",
    "monocytes",
    "eosinophils",
    "erythroid precursors",
    "lymphocytes",
    "plasma cells",
]

result_dirs = [
    "/media/hdd3/neo/MDS_EB1_EB2_results",
    "/media/hdd3/neo/MDS_non_EB1_EB2_results",
]

# first get the paths of all the subdirs of all the result_dirs
subdirs = []

for result_dir in result_dirs:
    for subdir in os.listdir(result_dir):
        subdirs.append(os.path.join(result_dir, subdir))

diff_dict = {
    "wsi_name": [],
    "Dx": [],
    "sub_Dx": [],
}

for cellname in cellnames:
    diff_dict[cellname] = []

for subdir in tqdm(subdirs, desc="Processing subdirs:"):

    diff_csv_path = os.path.join(subdir, "differential_full_class_count.csv")

    diff_mapp = csv_to_dict(diff_csv_path)

    for cellname in cellnames:
        if cellname in diff_mapp:
            diff_dict[cellname].append(diff_mapp[cellname])
        else:
            diff_dict[cellname].append(0)

    wsi_name = os.path.basename(subdir) + ".ndpi"

    diff_dict["wsi_name"].append(wsi_name)

    dx_row = dx_df[dx_df["wsi_name"] == wsi_name]
    assert len(dx_row) >= 1, f"Expected 1 row, but got {len(dx_row)} rows"

    # take the first row
    dx_row = dx_row.iloc[0]

    Dx = dx_row["Dx"]
    sub_Dx = dx_row["sub_Dx"]

    diff_dict["Dx"].append(Dx)
    diff_dict["sub_Dx"].append(sub_Dx)

diff_df = pd.DataFrame(diff_dict)

# save the diff_df to a csv file
diff_df.to_csv("/media/hdd3/neo/MDS_BMA_diff_results.csv", index=False)
