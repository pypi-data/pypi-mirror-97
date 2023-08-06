from mle_training_housing.utils import *


def main():
    """ 
    Feature generation and model training is done in the function. 
    The function can be invoked from Command Line Interface (CLI).

    CLI Syntax : **train_model -Folder <user_input>**

    *(Folder is an optional parameter. Default value is 'housing_run_v1'.)*

    Inputs required :
    
    - /<user_input>/model/input/train_data.csv    
    - /<user_input>/model/input/test_data.csv

    Outputs :

    - /<user_input>/model/pickle/pickle.p

    Raises
    ------
    FileNotFoundError
        If the train_data.csv is not available in the model/input folder. 
    """
    logger = configure_logger()
    logger.info("Model Training is started.")

    model_dump_final = MODEL_DUMP_PATH
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
        model_dump_final = os.path.join(args.Folder, "data/model", "pickle")
        model_input_path_final = os.path.join(args.Folder, "data/model", "input")
    else:
        logger.info(
            "User argument is not specified. The files will be saved in the default folder."
        )

    try:
        train_data = read_data("train_data.csv", model_input_path_final)
    except:
        raise FileNotFoundError(
            "train_data.csv is not present in the "
            + model_input_path_final
            + ". Please create and try again."
        )
        sys.exit(1)

    housing_prepared, housing_labels = data_preprocessing(train_data.copy())

    lin_reg = LinearRegression()
    lin_reg.fit(housing_prepared, housing_labels)

    housing_predictions = lin_reg.predict(housing_prepared)
    lin_mse = mean_squared_error(housing_labels, housing_predictions)
    lin_rmse = np.sqrt(lin_mse)
    logger.info("Linear Regression RMSE - " + str(np.round(lin_rmse, 2)))

    # lin_mae = mean_absolute_error(housing_labels, housing_predictions)
    # lin_mae

    tree_reg = DecisionTreeRegressor(random_state=42)
    tree_reg.fit(housing_prepared, housing_labels)

    housing_predictions = tree_reg.predict(housing_prepared)
    tree_mse = mean_squared_error(housing_labels, housing_predictions)
    tree_rmse = np.sqrt(tree_mse)
    logger.info("Decision Tree RMSE - " + str(np.round(tree_rmse, 2)))

    param_distribs = {
        "n_estimators": randint(low=1, high=200),
        "max_features": randint(low=1, high=8),
    }

    forest_reg = RandomForestRegressor(random_state=42)
    rnd_search = RandomizedSearchCV(
        forest_reg,
        param_distributions=param_distribs,
        n_iter=10,
        cv=5,
        scoring="neg_mean_squared_error",
        random_state=42,
    )
    rnd_search.fit(housing_prepared, housing_labels)
    cvres = rnd_search.cv_results_
    for mean_score, params in zip(cvres["mean_test_score"], cvres["params"]):
        print(np.sqrt(-mean_score), params)

    param_grid = [
        # try 12 (3×4) combinations of hyperparameters
        {"n_estimators": [3, 10, 30], "max_features": [2, 4, 6, 8]},
        # then try 6 (2×3) combinations with bootstrap set as False
        {"bootstrap": [False], "n_estimators": [3, 10], "max_features": [2, 3, 4]},
    ]

    forest_reg = RandomForestRegressor(random_state=42)
    # train across 5 folds, that's a total of (12+6)*5=90 rounds of training
    grid_search = GridSearchCV(
        forest_reg,
        param_grid,
        cv=5,
        scoring="neg_mean_squared_error",
        return_train_score=True,
    )
    grid_search.fit(housing_prepared, housing_labels)

    grid_search.best_params_
    cvres = grid_search.cv_results_
    # for mean_score, params in zip(cvres["mean_test_score"], cvres["params"]):
    #    print(np.sqrt(-mean_score), params)

    feature_importances = grid_search.best_estimator_.feature_importances_
    sorted(zip(feature_importances, housing_prepared.columns), reverse=True)

    final_model = grid_search.best_estimator_
    # print(type(final_model))
    save_model_pickle(final_model, model_dump_final)
    logger.info(
        "The model is trained using the training data and the model pickle file is stored in the path - "
        + model_dump_final
    )
