<center><h1>Evaluating student writing</h1></center>

<h2> About </h2>

[Competition link](https://www.kaggle.com/c/feedback-prize-2021)

----

<h2> How to run </h2>

First create a conda environment using the following command:

```bash
conda env create -f env.yml
```

Activate the environment and run the following command:

```bash
./setup_repo.sh
```

This will prepare pre-commit hooks, download pretrained model for english lanugage for Spacy (accuracy) and extract dataset.

Make sure that the project root directory is added to the PYTHONPATH, to be able to import the code correctly. To add it simply run in project root directory:

```bash
. ./export_path.sh
```

To test if everything works run:

```bash
python src/test.py
```

----

<h2> About hooks </h2>

There are five hooks that are used to check the quality of the code before commiting changes. These are:
 - check-yaml - checks yaml files for parseable syntax
 - end-of-file-fixer - ensures that files ends with one newline
 - trailing-whitespace - trims trailing whitespace
 - black - runs black autoformatter on files
 - flake8 - checks consistency of code style

From time to time you can run the following command to check if everything is up to date:

```bash
pre-commit autoupdate
```

To run the hooks manually run:

```bash
pre-commit run --all-files
```
