# Word-tree
Word-tree Text Analysis for large sets of review-based text

## Pre-req
*Dataset files*
This repo does not include a dataset. For instructions on how to load CSV data to a Postgres DB, please refer to the jupyter notebook [wordtree_tools.ipynb](https://github.com/supermikol/word-tree/blob/main/wordtree_tools.ipynb) AFTER setting up your database server.

Make sure current version of python is *3.6 or above*

## First Time
If you would prefer to set this up in a virtual environment:
1. `python -m venv venv` 
2. `pip install -r requirements.txt `
3. `source venv/bin/activate`

If no venv is required, simply run `pip install -r requirements.txt ` 

### Create credentials
In the root folder, create a file named `credentials.py` with the following values:

```
POSTGRESQL_USER = "YOUR_POSTGRES_USERNAME"
POSTGRESQL_PASSWORD = "YOUR_POSTGRES_PASSWORD"
POSTGRESQL_DB = "YOUR_DB_NAME"
POSTGRESQL_HOST = "YOUR_DB_HOST_ADDRESS"
```

### Setting up the Database

Default DB is Postgres.

Initialize your DB
```
$ flask db init
$ flask db migrate
$ flask db upgrade
```

For instructions on how to load CSV data to Postgres DB, please refer to the first section of the jupyter notebook [wordtree_tools.ipynb](https://github.com/supermikol/word-tree/blob/main/wordtree_tools.ipynb)

### Launch server

`$ FLASK_ENV=development flask run`

Visit [localhost:5000](localhost:5000)


## Relaunching server
Simply activate the virtual envinronment and launch
```
$ source venv/bin/activate
$ FLASK_ENV=development flask run
```

Will enable debug in development mode
