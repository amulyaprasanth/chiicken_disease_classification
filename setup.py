import setuptools

__version__ = "0.0.0"
REPO_NAME = "chiicken_disease_classification"
AUTHOR_NAME = "amulyaprasanth"
SRC_REPO = "cnnClassifier"
AUTHOR_EMAIL = "amulyaprasnath301@gmail.com"

setuptools.setup(
    name = SRC_REPO,
    VERSION= __version__,
    author = AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    DESCRIPTION = 'A small python package for CNN app',
    url = f'https://github.com/{AUTHOR_NAME}/{REPO_NAME}',
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src")
    )