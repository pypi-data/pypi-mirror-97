import cx_Oracle

from data_engineering_extract_metadata.utils import read_json


def create_oracle_connection(settings_file, location, oracle_client_lib=None):
    """Connects to an Oracle database, with settings taken from a specified json file

    Returns a cx_Oracle connection object.

    Parameters
    ----------
    settings_file (str):
        Filename of a json file with database login details.
        See readme for what the file should contain and how it should be structured

    location (str or Path):
        Location of the settings_file

    oracle_client_lib (str or None):
        Absolute path to your Oracle client libraries. Only needed if they're not in
        a place cx_Oracle already looks. See:
        https://cx-oracle.readthedocs.io/en/latest/user_guide/initialization.html
    """
    db_settings = read_json(settings_file, location)

    if oracle_client_lib:
        cx_Oracle.init_oracle_client(lib_dir=oracle_client_lib)

    dsn = cx_Oracle.makedsn(
        host=db_settings["host"],
        port=db_settings["port"],
        service_name=db_settings["service_name"],
    )
    connection = cx_Oracle.connect(
        user=db_settings["user"],
        password=db_settings["password"],
        dsn=dsn,
        encoding="UTF-8",
    )
    return connection
