from setuptools import find_packages, setup

setup(
    name="mle_training_housing",
    version="0.1.1",
    description="Training on python packaging and testing",
    classifiers=["Development Status :: 3 - Alpha"],
    keywords="MLE Training - Housing",
    url="http://github.com/vinithsrinivas/mle-training",
    author="Vinith",
    author_email="vinith.jegathees@tigeranalytics.com",
    license="TA",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "scipy",
        "sklearn",
        "logging",
        "logging_tree",
        "pytest",
        "six",
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "pull_data=mle_training_housing.ingest_data:main",
            "train_model=mle_training_housing.train:main",
            "score_test=mle_training_housing.score:main",
        ]
    },
)
