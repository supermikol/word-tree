# word-tree
word-tree text analysis for large sets of amazon reviews
# Pre-req
Dataset files. This repo does not include a dataset

Make sure current version of python is *3.6 or above*

If a virtual environment is necesary, first generate a new virtual environment with:
1. `python -m venv venv` 
2. `pip install -r requirements.txt `
3. `source venv/bin/activate`

If no venv is required, simply run `pip install -r requirements.txt ` 

`source venv/bin/activate`

```
$ flask db init
$ flask db migrate
$ flask db upgrade
```