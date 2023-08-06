from mle_training_housing.utils import *

# housing_url - Path where the data resides.
# housing_path - Path where the data should be saved.


def main():
    """ 
    Pulls the raw data and creates train and test data.
    The function can be invoked from Command Line Interface (CLI).
    
    CLI Syntax : **pull_data -Folder <user_input>**

    *(Folder is an optional parameter. Default value is 'housing_run_v1'.)*

    Output Files created :

    - /<user_input>/data/raw/housing/housing.csv
    - /<user_input>/data/model/input/train_data.csv
    - /<user_input>/data/model/input/test_data.csv
    """
    logger = configure_logger()

    logger.info("Data pull is started.")
    housing_path_final = HOUSING_PATH
    model_input_path_final = MODEL_INPUT_PATH

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-Folder", nargs="?", help="Mention the folder to load the files."
    )
    args = parser.parse_args()
    if args.Folder:
        # print(args.Path)
        logger.info(
            "User argument is specified. The files will be saved in the user specified folder."
        )
        housing_path_final = os.path.join(args.Folder, "data/raw", "housing")
        model_input_path_final = os.path.join(args.Folder, "data/model", "input")
    else:
        logger.info(
            "User argument is not specified. The files will be saved in the default folder."
        )

    fetch_housing_data(HOUSING_URL, housing_path_final)
    housing = read_data("housing.csv", housing_path_final)
    # housing = load_housing_data(housing_path_final)

    logger.info("Raw Data is pulled and saved in the path - " + housing_path_final)

    housing["income_cat"] = pd.cut(
        housing["median_income"],
        bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
        labels=[1, 2, 3, 4, 5],
    )

    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

    for train_index, test_index in split.split(housing, housing["income_cat"]):
        strat_train_set = housing.loc[train_index]
        strat_test_set = housing.loc[test_index]

    save_data(strat_train_set, "train_data.csv", model_input_path_final)
    save_data(strat_test_set, "test_data.csv", model_input_path_final)

    logger.info(
        "Train and test data are created and saved in the below path - "
        + model_input_path_final
    )
