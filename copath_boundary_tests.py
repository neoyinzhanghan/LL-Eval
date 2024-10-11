import json
import pandas as pd
from tqdm import tqdm

ref_range_tests_json_path = "/Users/neo/Documents/MODS/LL-Eval/ref_range_tests.json"
# first open the ref_range_tests.json file
with open(ref_range_tests_json_path, "r") as f:
    ref_range_tests = json.load(f)

diff_result_path = "/Users/neo/Documents/MODS/LL-Eval/test_diff_results.csv"

ground_truth_diff_data_path = "/Users/neo/Documents/MODS/LL-Eval/test_diff_data.csv"

# load the ground truth differential data
ground_truth_diff_data = pd.read_csv(ground_truth_diff_data_path)
diff_result = pd.read_csv(diff_result_path)


# remove the columns part_description and text_data_final from ground_truth_diff_data
ground_truth_diff_data = ground_truth_diff_data.drop(
    columns=["part_description", "text_data_final"]
)


num_rows = len(diff_result)
num_rows_with_ground_truth = 0

# iterate over rows of diff_result
for idx, row in tqdm(diff_result.iterrows(), desc="Iterating over diff_result:"):
    row_dict = row.to_dict()

    wsi_name = row_dict["wsi_name"]

    specnum_formatted = wsi_name.split(";")[0]

    # look for the row in ground_truth_diff_data that has the same specnum_formatted
    ground_truth_row = ground_truth_diff_data[
        ground_truth_diff_data["specnum_formatted"] == specnum_formatted
    ]

    # if a row is found in ground_truth_diff_data, increment num_rows_with_ground_truth
    if len(ground_truth_row) > 0:
        num_rows_with_ground_truth += 1

print(f"Number of rows in diff_result: {num_rows}")
print(f"Number of rows with ground truth: {num_rows_with_ground_truth}")
