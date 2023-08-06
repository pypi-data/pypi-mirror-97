from mle_training_housing.utils import *


def main():
    """ 
    Trained model is validated using test data in the function. 
    The function can be invoked from Command Line Interface (CLI). 

    CLI Syntax : **score_test -Folder <user_input>**

    *(Folder is an optional parameter. Default value is 'housing_run_v1'.)*

    Inputs Files required : 

    - /<user_input>/model/input/test_data.csv    
    - /<user_input>/model/pickle/pickle.p

    Output Files created :

    - /<user_input>/model/output/pickle.p

    Raises
    ------
    FileNotFoundError
        If the test_data.csv or model pickle file (pickle.p) is not available in the model/input folder. 
    """
    logger = configure_logger()
    logger.info("Model Validation is started.")

    model_output_path_final = MODEL_OUTPUT_PATH
    model_input_path_final = MODEL_INPUT_PATH
    model_dump_final = MODEL_DUMP_PATH

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-Folder", nargs="?", help="Mention the folder to load the files."
    )
    args = parser.parse_args()
    if args.Folder:
        logger.info(
            "User argument is specified. The files will be saved in the user specified folder."
        )
        # print(args.Path)
        model_output_path_final = os.path.join(args.Folder, "data/model", "output")
        model_input_path_final = os.path.join(args.Folder, "data/model", "input")
        model_dump_final = os.path.join(args.Folder, "data/model", "pickle")
    else:
        logger.info(
            "User argument is not specified. The files will be saved in the default folder."
        )

    try:
        test_data = read_data("test_data.csv", model_input_path_final)
        final_model = pickle.load(
            open(os.path.join(model_dump_final, "pickle.p"), "rb")
        )
    except:
        raise FileNotFoundError(
            "Either test_data.csv or pickle.p is not present in the model folder. Please create and try again."
        )
        sys.exit(1)

    test_prepared, test_labels = data_preprocessing(test_data.copy())

    final_predictions = final_model.predict(test_prepared)
    test_prepared["Actual_house_price"] = test_labels
    test_prepared["Predicted_house_price"] = final_predictions
    save_data(test_prepared, "predictions.csv", model_output_path_final)
    final_mse = mean_squared_error(test_labels, final_predictions)
    final_rmse = np.sqrt(final_mse)
    logger.info("Final RMSE - " + str(np.round(final_rmse, 2)))
    logger.info(
        "Model is validated using the saved model and the predictions are store in the path - "
        + model_output_path_final
    )
