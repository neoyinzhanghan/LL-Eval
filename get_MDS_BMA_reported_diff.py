import pandas as pd
from get_copath_data import get_diff, get_path_data

wsi_names_csv_path = "/media/hdd3/neo/MDS_all_wsi_names.csv"

# get the wsi_name column of the wsi_names.csv file as a list
wsi_names_df = pd.read_csv(wsi_names_csv_path)
wsi_names = wsi_names_df["wsi_name"].tolist()

# get the accession numbers from the wsi_names
accession_numbers = [wsi_name.split(";")[0] for wsi_name in wsi_names]

print("Getting copath data from database...")
copath_df = get_path_data(accession_numbers)

print("Extracting differential data from copath data...")
diff_df = get_diff(copath_df)

# print the number of rows in the copath_df and diff_df
print(f"Number of accession numbers requested: {len(accession_numbers)}")

print(f"Number of rows in copath_df: {len(copath_df)}")
print(f"Number of rows in diff_df: {len(diff_df)}")

# save the copath_df and diff_df to csv files
copath_df.to_csv("/media/hdd3/neo/MDS_copath_data_2024-10-16.csv", index=False)
diff_df.to_csv("/media/hdd3/neo/MDS_differential_data_2024-10-16.csv", index=False)
