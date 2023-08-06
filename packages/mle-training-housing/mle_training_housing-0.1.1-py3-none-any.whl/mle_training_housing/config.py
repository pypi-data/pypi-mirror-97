# Default folders for the model run

DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml/master/"
HOUSING_URL = DOWNLOAD_ROOT + "datasets/housing/housing.tgz"

HOUSING_PATH = "housing_run_v1/data/raw/housing/"
MODEL_INPUT_PATH = "housing_run_v1/data/model/input"
MODEL_DUMP_PATH = "housing_run_v1/data/model/pickle"
MODEL_OUTPUT_PATH = "housing_run_v1/data/model/output"

# Logging Config
# More on Logging Configuration
# https://docs.python.org/3/library/logging.config.html
# Setting up a config
LOGGING_DEFAULT_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {"format": "%(message)s"},
    },
    "root": {"level": "DEBUG"},
}
