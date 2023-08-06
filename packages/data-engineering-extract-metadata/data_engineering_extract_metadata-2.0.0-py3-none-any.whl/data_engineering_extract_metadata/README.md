# File guide
**connect.py** contains `create_oracle_connection`, which returns an Oracle database connection

**metadata.py** contains functions for getting metadata from tables, plus wrapper functions for running the whole extraction process

**table_list.py** contains functions for extracting a list of tables from a database

**utils.py** is helper functions for reading and writing json, and creating OS directories where needed when writing files