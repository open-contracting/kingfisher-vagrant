import os
import sys
import pgpasslib
import configparser

config = configparser.ConfigParser()
# User level config file.
config.read(os.path.expanduser('~/.config/ocdsdata/config.ini'))


# Loads database details or defaults
host = config.get('DBHOST', 'HOSTNAME', fallback='localhost')
port = config.get('DBHOST', 'PORT', fallback='5432')
user = config.get('DBHOST', 'USERNAME', fallback='ocdsdata')
dbname = config.get('DBHOST', 'DBNAME', fallback='ocdsdata')
dbpass = config.get('DBHOST', 'PASSWORD', fallback='ocdsdata')


def __gen_dburi(user, password, host, port, dbname):
    return 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, dbname)


try:
    fetched_pass = pgpasslib.getpass(host, port, user, dbname)
    password = fetched_pass if fetched_pass else dbpass
    database_uri = __gen_dburi(user, password, host, port, dbname)
except pgpasslib.FileNotFound:
    # Fail silently when no files found.
    password = dbpass
    database_uri = __gen_dburi(user, password, host, port, dbname)
except pgpasslib.InvalidPermissions:
    print("Your pgpass file has the wrong permissions, for your safety this file will be ignored. Please fix the permissions and try again.")
    password = dbpass
    database_uri = __gen_dburi(user, password, host, port, dbname)
except pgpasslib.PgPassException:
    print("Unexpected error:", sys.exc_info()[0])
    password = dbpass
    database_uri = __gen_dburi(user, password, host, port, dbname)

# Overwrites if DB_URI is specified.
DB_URI = os.environ.get('DB_URI', database_uri)
