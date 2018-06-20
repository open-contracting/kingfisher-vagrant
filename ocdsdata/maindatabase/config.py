import os
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

try:
    password = pgpasslib.getpass(host, port, user, dbname)
    database_uri = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, dbname)
except pgpasslib.FileNotFound:
    database_uri = 'postgresql://{}:{}@{}:{}/{}'.format(user, dbpass, host, port, dbname)

# Overwrites if DB_URI is specified.
DB_URI = os.environ.get('DB_URI', database_uri)
