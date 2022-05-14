<center><h1>Evaluating student writing</h1></center>

<h2> About </h2>

TODO

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
