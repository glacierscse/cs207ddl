## Similarity Search
This file provides several functionality, including generate random timeseries data, randomly select vantage timeseries points and create a database for each of the point, and most importantly find closest timeseries points to a given timeseries input.

### Generate random timeseries data
Run `genTS.py` to generate randome timeseries data.
```
$ python genTS.py --help

Usage: genTS.py [OPTIONS]

  generate n standardized time series, each stored in a file in ts_data/.

Options:
  -n INTEGER   number of ts to generate, default 1000
  --n INTEGER  number of ts to generate, default 1000
  --help       Show this message and exit.
```
For example, run `python genTS.py --n 500` to generate 500 timeseries data.

The generated data would be stored as `.dat` files in `ts_data/`.

### Select vantage timeseries points and create databases
Run `genVantage.py` to randomly select vantage points and create corresponding database.
```
$ python genVantage.py --help

Usage: genVantage.py [OPTIONS]

  generate n vantage points for our ts data

Options:
  -n INTEGER   number of vantage points to generate, default 20
  --n INTEGER  number of vantage points to generate, default 20
  --help       Show this message and exit.
```
For example, run `python genVantage.py --n 10` to randomly select 10 timeseries data points and create corresponding database. Each database is stored as `.db` file in  `ts_db_index/`. 

### Find similar timeseries points
Run `find_closest.py` to find closest timeseries points to a given point. 
```
$ python find_closest.py --help

Usage: find_closest.py [OPTIONS]

  search for n closest points to input ts, results are stored as .dat file
  in search_res/

Options:
  --input TEXT  name of your input ts file
  --n INTEGER   number of similar points to find, default 10
  -n INTEGER    number of similar points to find, default 10
  --show-dist   set this flag to show (and store) corresponding distance from
                similar points to input point
  --clear-dir   set this flag to clear the search result directory
  --help        Show this message and exit.
```
For example, run `python find_closest.py 10` to find 10 closest points.
  
By default, the function would return only the name of the timseries files. You can add `--show-dist` to return the distance associated with these files. The results will be saved to `search_res/` directory.

If you want to clear the `search_res/` directory in order to store new search results, you can add `--clear-dir` flag when you run the command.
