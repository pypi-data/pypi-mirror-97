# Extract metadata for data engineering pipelines
This repo lets you extract metadata from a database and shape it into a folder of json files that [etl_manager](https://github.com/moj-analytical-services/etl_manager) can read. 

The `create_all_metadata` function will do most of the process in one go. See 'quickstart' below for a summary, or more detailed documentation below that. The end result will be: 

- a json file containing a filtered list of tables
- a subfolder for the metadata
- in that subfolder, a database.json file with overall metadata for the database
- also in that subfolder, another .json file listing the columns and other metadata for each table

## Requirements
This runs in Python 3.6+. You'll need to [install cx_Oracle 8.0.0+](https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html). 

Installing cx_Oracle also involves installing its client libraries. You can [download it from Oracle](https://www.oracle.com/database/technologies/instant-client/downloads.html) or, if you're on Mac, install by Homebrew:

`brew tap InstantClientTap/instantclient`
`brew install instantclient-basic`

### cx_Oracle problems 1: client host name
If you're on a Mac, you might get errors like "cx_Oracle.DatabaseError: ORA-24454: client host name is not set". If you do, you'll need to adjust your hosts file. To do this:

- go to system preferences, then sharing, and note the computer name at the top
- go to your hard disk, then the `etc` folder and find the `hosts` file
- back up your hosts file in case anything weird happens
- in hosts, find the line that says `127.0.0.1 localhost`
- under it, add a new line that says `127.0.0.01 computer_name`, where computer_name is the one you got from system preferences/sharing
- save the hosts file

### cx_Oracle problems 2: client library location
Depending on how you installed the Oracle client libraries, the create_oracle_connection function might not work with default parameters. 

If it won't connect, try specifying the location of your client libraries using the oracle_client_lib parameter.

## Quick start
Here's an example of creating a full metadata folder by using create_all_metadata and a custom function to filter the table list: 

``` python

from pathlib import Path
from extract_metadata.connect import create_oracle_connection
from extract_metadata.metadata import create_all_metadata


def table_filter(table_list):
    """Takes a list of (table, tablespace) tuples and filters it down to tables that have 'REPLICATION_TEST' in their name"""
    return [t[0] for t in table_list if "REPLICATION_TEST" in t[0]]


settings_location = Path.cwd().parent / "settings_folder"
connection = create_oracle_connection("delius_sandpit", settings_location)

create_all_metadata(
    connection,
    save_folder="delius",
    title="delius_sandpit_test",
    description="Here's a description",
    schema="DELIUS_ANALYTICS_PLATFORM",
    source_bucket="mojap-raw-hist-dev",
    source_folder="hmpps/delius/DELIUS_ANALYTICS_PLATFORM",
    filter_function=table_filter,
)

connection.close()
```

If you save this in a script called `get_metadata.py` in /metadata/ folder, you'll end up with this folder structure: 

```
metadata
|-- get_metadata.py
|-- delius
|   |-- delius_sandpit_test.json
|   |-- delius_sandpit_test
|   |   |-- database.json
|   |   |-- table1.json
|   |   |-- table2.json
```

## Step by step
There are 3 steps to getting metadata from a database: 
1. Connect using connect.create_oracle_connection
2. Make a list of all the tables and filter it to the ones you want - you can do both with table_list.get_table_list
3. Get metadata from the filtered list of tables using metadata.create_metadata_folder

### 1. Connecting
You'll need some database connection settings. These should be in a json file structured like this: 

``` json
{
    "host": "HOST",
    "password": "PASSWORD",
    "port": 1234,
    "service_name": "SERVICE_NAME",
    "user": "database_username"
}
```

Then pass this file and its location to create_oracle_connection in the connect module. You might also need to use the oracle_client_lib parameter to specify where your Oracle client libraries are. See the cx_Oracle connection problems, above. 

### 2. Making a list of tables
get_table_list in the table_list module will use your connection to get a list of tables from the database. 

It will create a timestamped json file listing the tables. Specify the file's save_folder and title when you call the function. 

Also specify the database schema to get the tables from.  

You might not want the file to list all the tables. In this case, pass a filter_function as well. This should be a function that takes a single argument - a list, in this format:

`[("TABLE_NAME", "TABLESPACE"), ("ANOTHER_TABLE_NAME", "TABLESPACE")]`

Return the tables you want as a list of table names. So if you only wanted the first one from this list, you'd want to return: 

`["TABLE_NAME"]`

### 3. Get the metadata for the tables
To read a folder with etl_manager, it must contain a database.json file specifying overall features of the database, plus a json file for each table. 

You can create these in one go using metadata.create_metadata_folder, or separately with metadata.create_json_for_database and metadata.create_json_for_tables.

## Tests
Unit tests are written for pytest. Run `pytest` from the root folder to start them.

Where functions involve SQL queries, the unit tests don't check these queries - only the Python surrounding them. 

## Githooks
This repo comes with some githooks to make standard checks before you commit files to Github. The checks are: 
- if you're using git-crypt, run `git-crypt status` and check for unencrypted file warnings 
- run Black on Python files
- run Flake8 on Python files
- run yamllint on yaml files

If you want to use these, run this command from the repo's root directory: 

`git config core.hooksPath githooks`

See the [data engineering template repo](https://github.com/moj-analytical-services/data-engineering-template) for details. 

## Licence
[MIT Licence](LICENCE.md)
# Extract metadata for data engineering pipelines
This repo lets you extract metadata from a database and shape it into a folder of json files that [etl_manager](https://github.com/moj-analytical-services/etl_manager) can read. 

The `create_all_metadata` function will do most of the process in one go. See 'quickstart' below for a summary, or more detailed documentation below that. The end result will be: 

- a json file containing a filtered list of tables
- a subfolder for the metadata
- in that subfolder, a database.json file with overall metadata for the database
- also in that subfolder, another .json file listing the columns and other metadata for each table

## Requirements
This runs in Python 3.6+. You'll need to [install cx_Oracle 8.0.0+](https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html). 

Installing cx_Oracle also involves installing its client libraries. You can [download it from Oracle](https://www.oracle.com/database/technologies/instant-client/downloads.html) or, if you're on Mac, install by Homebrew:

`brew tap InstantClientTap/instantclient`
`brew install instantclient-basic`

### cx_Oracle problems 1: client host name
If you're on a Mac, you might get errors like "cx_Oracle.DatabaseError: ORA-24454: client host name is not set". If you do, you'll need to adjust your hosts file. To do this:

- go to system preferences, then sharing, and note the computer name at the top
- go to your hard disk, then the `etc` folder and find the `hosts` file
- back up your hosts file in case anything weird happens
- in hosts, find the line that says `127.0.0.1 localhost`
- under it, add a new line that says `127.0.0.01 computer_name`, where computer_name is the one you got from system preferences/sharing
- save the hosts file

### cx_Oracle problems 2: client library location
Depending on how you installed the Oracle client libraries, the create_oracle_connection function might not work with default parameters. 

If it won't connect, try specifying the location of your client libraries using the oracle_client_lib parameter.

## Quick start
Here's an example of creating a full metadata folder by using create_all_metadata and a custom function to filter the table list: 

``` python

from pathlib import Path
from extract_metadata.connect import create_oracle_connection
from extract_metadata.metadata import create_all_metadata


def table_filter(table_list):
    """Takes a list of (table, tablespace) tuples and filters it down to tables that have 'REPLICATION_TEST' in their name"""
    return [t[0] for t in table_list if "REPLICATION_TEST" in t[0]]


settings_location = Path.cwd().parent / "settings_folder"
connection = create_oracle_connection("delius_sandpit", settings_location)

create_all_metadata(
    connection,
    save_folder="delius",
    title="delius_sandpit_test",
    description="Here's a description",
    schema="DELIUS_ANALYTICS_PLATFORM",
    source_bucket="mojap-raw-hist-dev",
    source_folder="hmpps/delius/DELIUS_ANALYTICS_PLATFORM",
    filter_function=table_filter,
)

connection.close()
```

If you save this in a script called `get_metadata.py` in /metadata/ folder, you'll end up with this folder structure: 

```
metadata
|-- get_metadata.py
|-- delius
|   |-- delius_sandpit_test.json
|   |-- delius_sandpit_test
|   |   |-- database.json
|   |   |-- table1.json
|   |   |-- table2.json
```

## Step by step
There are 3 steps to getting metadata from a database: 
1. Connect using connect.create_oracle_connection
2. Make a list of all the tables and filter it to the ones you want - you can do both with table_list.get_table_list
3. Get metadata from the filtered list of tables using metadata.create_metadata_folder

### 1. Connecting
You'll need some database connection settings. These should be in a json file structured like this: 

``` json
{
    "host": "HOST",
    "password": "PASSWORD",
    "port": 1234,
    "service_name": "SERVICE_NAME",
    "user": "database_username"
}
```

Then pass this file and its location to create_oracle_connection in the connect module. You might also need to use the oracle_client_lib parameter to specify where your Oracle client libraries are. See the cx_Oracle connection problems, above. 

### 2. Making a list of tables
get_table_list in the table_list module will use your connection to get a list of tables from the database. 

It will create a timestamped json file listing the tables. Specify the file's save_folder and title when you call the function. 

Also specify the database schema to get the tables from.  

You might not want the file to list all the tables. In this case, pass a filter_function as well. This should be a function that takes a single argument - a list, in this format:

`[("TABLE_NAME", "TABLESPACE"), ("ANOTHER_TABLE_NAME", "TABLESPACE")]`

Return the tables you want as a list of table names. So if you only wanted the first one from this list, you'd want to return: 

`["TABLE_NAME"]`

### 3. Get the metadata for the tables
To read a folder with etl_manager, it must contain a database.json file specifying overall features of the database, plus a json file for each table. 

You can create these in one go using metadata.create_metadata_folder, or separately with metadata.create_json_for_database and metadata.create_json_for_tables.

## Tests
Unit tests are written for pytest. Run `pytest` from the root folder to start them.

Where functions involve SQL queries, the unit tests don't check these queries - only the Python surrounding them. 

## How to update
Update and release new versions using Poetry. Make sure to change the version number in `pyproject.toml` and describe the change in `CHANGELOG.md`.

If you've changed any dependencies in `pyproject.yaml`, run `poetry update` to update `poetry.lock`.

Once you've created a release in GitHub, to publish the latest version to PyPI, run:

```
poetry build
poetry publish -u <username>
```

Here, you should replace `<username>` with your PyPI username. To publish to PyPI, you must be an owner of the project.

## Licence
[MIT Licence](LICENCE.md)
