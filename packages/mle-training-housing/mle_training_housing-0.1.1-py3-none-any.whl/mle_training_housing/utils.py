import argparse
import logging
import logging.config
import os
import pickle
import tarfile

import numpy as np
import pandas as pd
import pandas.api.types as ptypes
from logging_tree import printout
from scipy.stats import randint
from six.moves import urllib
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import (GridSearchCV, RandomizedSearchCV,
                                     StratifiedShuffleSplit, train_test_split)
from sklearn.tree import DecisionTreeRegressor

from mle_training_housing.config import *

# Function to read the data from the URL and save it in the path.


def fetch_housing_data(housing_url, housing_path):
    """
    Raw data is downloaded from the URL and saved. 

    Parameters
    ----------
    housing_url : str
        URL containing the raw housing data.
    housing_path : str
        Path where the downloaded file is to be saved.
    """
    os.makedirs(housing_path, exist_ok=True)
    tgz_path = os.path.join(housing_path, "housing.tgz")
    urllib.request.urlretrieve(housing_url, tgz_path)
    housing_tgz = tarfile.open(tgz_path)
    housing_tgz.extractall(path=housing_path)
    housing_tgz.close()


def save_data(df, file_name, path):
    """
    Saves the data in the mentioned path. 

    Parameters
    ----------
    df : pandas dataframe
        Pandas dataframe which is to be saved. 
    file_name : str
        Name of the file which is to be created. 
    path : str
        Path where the file is to be saved. 
    """
    os.makedirs(path, exist_ok=True)
    df.to_csv(os.path.join(path, file_name), index=False)


def save_model_pickle(model_name, model_dump_path):
    """
    Saves the model pickle file in the mentioned path which can be re-used for the test data. 

    Parameters
    ----------
    model_name : 
        Final trained model which is to be used to predict the test data. 
    model_dump_path : str
        Path where the model file is to saved. 
    """
    os.makedirs(model_dump_path, exist_ok=True)
    pickle.dump(model_name, open(os.path.join(model_dump_path, "pickle.p"), "wb"))


def read_data(file_name, path):
    """
    Function to read a csv file. 

    Parameters
    ----------
    file_name : str
        File name to be read. 
    path : str
        Path where the file is saved. 

    Returns
    -------
    pandas dataframe
        File is read as a pandas dataframe and returned as a function output.
    """
    return pd.read_csv(os.path.join(path, file_name))


def data_preprocessing(housing):
    """Data preprocessing is done in this function for the model. 

    Parameters
    ----------
    housing : pandas dataframe 
        Raw dataframe which has the dependent (median_house_value column) and independent variables.
        
    Returns
    -------
    housing_prepared : pandas dataframe
        Pandas dataframe having the independent variables. 
    housing_labels : pandas dataframe
        Pandas dataframe having the dependent variable. 
    """

    housing_labels = housing["median_house_value"].copy()
    housing = housing.drop("median_house_value", axis=1)  # drop labels for training set

    imputer = SimpleImputer(strategy="median")

    housing_num = housing.drop("ocean_proximity", axis=1)

    imputer.fit(housing_num)
    X = imputer.transform(housing_num)

    housing_tr = pd.DataFrame(X, columns=housing_num.columns, index=housing.index)
    housing_tr["rooms_per_household"] = (
        housing_tr["total_rooms"] / housing_tr["households"]
    )
    housing_tr["bedrooms_per_room"] = (
        housing_tr["total_bedrooms"] / housing_tr["total_rooms"]
    )
    housing_tr["population_per_household"] = (
        housing_tr["population"] / housing_tr["households"]
    )

    housing_cat = housing[["ocean_proximity"]]
    housing_prepared = housing_tr.join(pd.get_dummies(housing_cat, drop_first=True))
    return housing_prepared, housing_labels


def configure_logger(
    logger=None, cfg=None, log_file=None, console=True, log_level="DEBUG"
):
    """
    Function to setup configurations of logger through function.

    The individual arguments of `log_file`, `console`, `log_level` will overwrite the ones in cfg.

    Parameters
    ----------
    logger:
        Predefined logger object if present. If None a ew logger object will be created from root.
    cfg: dict()
        Configuration of the logging to be implemented by default
    log_file: str
        Path to the log file for logs to be stored
    console: bool
        To include a console handler(logs printing in console)
    log_level: str
        One of `["INFO","DEBUG","WARNING","ERROR","CRITICAL"]`
        default - `"DEBUG"`

    Returns
    -------
    logging.Logger
    """
    if not cfg:
        logging.config.dictConfig(LOGGING_DEFAULT_CONFIG)
    else:
        logging.config.dictConfig(cfg)

    logger = logger or logging.getLogger()

    if log_file or console:
        for hdlr in logger.handlers:
            logger.removeHandler(hdlr)

        if log_file:
            fh = logging.FileHandler(log_file)
            fh.setLevel(getattr(logging, log_level))
            logger.addHandler(fh)

        if console:
            sh = logging.StreamHandler()
            sh.setLevel(getattr(logging, log_level))
            logger.addHandler(sh)

    return logger

