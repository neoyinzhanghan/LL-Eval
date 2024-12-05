import os
import pandas as pd
import shutil
from tqdm import tqdm


result_dir = "/media/glv3/hdd3/neo/results_dir"
non_error_pipeline_aggregate_df_path = "pipeline_nonerror_aggregate_df.csv"
save_dir = "/media/hdd3/neo/results_dir_to_copy"

num_per_batch = 100

os.makedirs(save_dir, exist_ok=True)

# open the pipeline_run_history.csv file as a dataframe
pipeline_run_history_df = pd.read_csv(
    os.path.join(result_dir, "pipeline_run_history.csv")
)

# create a new column in pipeline_run_history_df called "result_dir_name" that is pipeline underscore datetime_processed
pipeline_run_history_df["result_dir_name"] = (
    pipeline_run_history_df["pipeline"]
    + "_"
    + pipeline_run_history_df["datetime_processed"]
)

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


def create_list_of_batches_from_list(list, batch_size):
    """
    This function creates a list of batches from a list.

    :param list: a list
    :param batch_size: the size of each batch
    :return: a list of batches

    >>> create_list_of_batches_from_list([1, 2, 3, 4, 5], 2)
    [[1, 2], [3, 4], [5]]
    >>> create_list_of_batches_from_list([1, 2, 3, 4, 5, 6], 3)
    [[1, 2, 3], [4, 5, 6]]
    >>> create_list_of_batches_from_list([], 3)
    []
    >>> create_list_of_batches_from_list([1, 2], 3)
    [[1, 2]]
    """

    list_of_batches = []

    for i in range(0, len(list), batch_size):
        batch = list[i : i + batch_size]
        list_of_batches.append(batch)

    return list_of_batches


# create a list of lists where each list contains num_per_batch number of result_dir_names, make sure to not leave any result_dir_name behind, so that last batch might have less than num_per_batch number of result_dir_names
result_dir_names_batches = create_list_of_batches_from_list(
    result_dir_names, num_per_batch
)

for batch_idx, batch in tqdm(enumerate(result_dir_names_batches)):
    # create a subdirectory in the save_dir named batch_idx
    batch_save_dir = os.path.join(save_dir, str(batch_idx))
    os.makedirs(batch_save_dir, exist_ok=True)

    for result_dir_name in tqdm(batch, desc="Getting symbolic link"):
        result_dir_path = os.path.join(result_dir, result_dir_name)
        save_path = os.path.join(batch_save_dir, result_dir_name)
        os.symlink(result_dir_path, save_path)

    # crop the pipeline_run_history_df to only include the result_dir_names in the batch
    cropped_pipeline_run_history_df = pipeline_run_history_df[
        pipeline_run_history_df["result_dir_name"].isin(batch)
    ]

    # save the df to a csv file named pipeline_run_history_{batch_idx}.csv
    cropped_pipeline_run_history_df.to_csv(
        os.path.join(batch_save_dir, f"pipeline_run_history_{batch_idx}.csv"),
        index=False,
    )

# save the whole pipeline_run_history_df to a csv file named pipeline_run_history.csv
pipeline_run_history_df.to_csv(
    os.path.join(save_dir, "pipeline_run_history.csv"), index=False
)
