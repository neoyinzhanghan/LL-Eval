import pandas as pd
from tqdm import tqdm

cell_metadata_path = "/Users/neo/Downloads/deepheme_metadata.csv"

cell_metadata = pd.read_csv(cell_metadata_path)

deidentified_cell_df_dict = {
    "cell_id": [],
    "cell_type": [],
    "institution": [],
}

cell_pseudo_id = 0

# iterate over the rows in the cell_metadata dataframe
for idx, row in tqdm(cell_metadata.iterrows(), desc="Deidentifying cell metadata:"):
    original_path = row["original_path"]

    # if UCSF_repo is in the path, the institution is UCSF
    if "UCSF_repo" in original_path:
        institution = "UCSF"
    elif "MSK_repo_normal" in original_path:
        institution = "MSK_normal"
    elif "MSK_repo_mixed" in original_path:
        institution = "MSK_mixed"
    else:  # skip the row if the institution is not UCSF or MSK
        continue

    # the path is formatted like /media/ssd2/dh_labelled_data/DeepHeme1/UCSF_repo/ER2/45823.png
    cell_type = original_path.split("/")[-2]

    # append the deidentified cell metadata to the deidentified_cell_df_dict
    deidentified_cell_df_dict["cell_id"].append(cell_pseudo_id)
    deidentified_cell_df_dict["cell_type"].append(cell_type)
    deidentified_cell_df_dict["institution"].append(institution)

    cell_pseudo_id += 1

# create a dataframe from the deidentified_cell_df_dict
deiden_df = pd.DataFrame(deidentified_cell_df_dict)

# save the deidentified cell metadata to a csv file
deiden_df.to_csv("deidentified_cell_metadata.csv", index=False)
