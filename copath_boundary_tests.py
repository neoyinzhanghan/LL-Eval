import json
import pandas as pd
import numpy as np
import os
from tqdm import tqdm
from sklearn.metrics import confusion_matrix

# Load JSON file containing reference range tests
ref_range_tests_json_path = "/Users/neo/Documents/MODS/LL-Eval/ref_range_tests.json"
with open(ref_range_tests_json_path, "r") as f:
    ref_range_tests = json.load(f)

# Load CSV files
diff_result_path = "/Users/neo/Documents/MODS/LL-Eval/2024-10-10/test_diff_results.csv"
ground_truth_diff_data_path = (
    "/Users/neo/Documents/MODS/LL-Eval/2024-10-10/differential_data_2024-10-10.csv"
)
diff_result = pd.read_csv(diff_result_path)
ground_truth_diff_data = pd.read_csv(ground_truth_diff_data_path)

# Drop unnecessary columns
ground_truth_diff_data = ground_truth_diff_data.drop(
    columns=["part_description", "text_data_final"]
)

# Output directory for saving confusion matrices
output_dir = "/Users/neo/Documents/MODS/LL-Eval/bdry_tests_results/2024-10-10"
os.makedirs(output_dir, exist_ok=True)


# Mapping reference ranges
def parse_range(range_str):
    """Converts a string range like '[0,5)' into a tuple (0, 5, True, False) for comparison."""
    left_inclusive = range_str.startswith("[")
    right_inclusive = range_str.endswith("]")
    left, right = map(float, range_str.strip("[]()").split(","))
    return left, right, left_inclusive, right_inclusive


def in_range(value, range_str):
    """Checks if a value is within the given range."""
    left, right, left_inclusive, right_inclusive = parse_range(range_str)
    if left_inclusive and right_inclusive:
        return left <= value <= right
    elif left_inclusive:
        return left <= value < right
    elif right_inclusive:
        return left < value <= right
    else:
        return left < value < right


# Aggregating data for comparison
def aggregate_classes(data, class_mapping):
    """Aggregates data based on class mapping."""
    total = 0
    for cls in class_mapping:
        total += data.get(cls, 0)
    return total


# Store confusion matrices for each test case
confusion_matrices = {}

# Iterate through each test case in the reference ranges and create confusion matrix entries
for test_name, test_details in ref_range_tests.items():
    y_true = []
    y_pred = []

    cell_classes = test_details["cell_classes"]
    diff_classes = test_details["diff_classes"]
    test_range = test_details["range"]

    # Filter diff_result and ground_truth_diff_data to match test cases
    for idx, row in tqdm(diff_result.iterrows(), desc=f"Processing {test_name}"):
        wsi_name = row["wsi_name"]
        specnum_formatted = wsi_name.split(";")[0]

        # Retrieve corresponding ground truth row
        ground_truth_row = ground_truth_diff_data[
            ground_truth_diff_data["specnum_formatted"] == specnum_formatted
        ]

        if len(ground_truth_row) > 0:
            # Aggregate sums based on mapped classes
            pred_total = aggregate_classes(row.to_dict(), cell_classes)
            gt_total = aggregate_classes(
                ground_truth_row.iloc[0].to_dict(), diff_classes
            )

            # Check if totals fall within the specified range
            pred_label = in_range(pred_total, test_range)
            gt_label = in_range(gt_total, test_range)

            # Store results for confusion matrix
            y_pred.append(pred_label)
            y_true.append(gt_label)

    # Generate and store the confusion matrix for the current test case
    conf_matrix = confusion_matrix(y_true, y_pred, labels=[True, False])
    confusion_matrices[test_name] = conf_matrix

    # Convert the confusion matrix to a DataFrame for saving
    conf_matrix_df = pd.DataFrame(
        conf_matrix,
        index=["True (In Range)", "True (Out of Range)"],
        columns=["Predicted (In Range)", "Predicted (Out of Range)"],
    )
    # Save each confusion matrix as a CSV file named after the test_name
    conf_matrix_df.to_csv(
        os.path.join(output_dir, f"{test_name.replace(' ', '_')}_confusion_matrix.csv")
    )

    print(f"\nConfusion Matrix for {test_name}:")
    print(f"Labels: [True, False]")
    print(conf_matrix)

print(f"Confusion matrices saved to: {output_dir}")
