import sqlalchemy as sa
import os
import datetime


class MetadataDB(object):

    def __init__(self, directory_path = None):
        self.base_path = directory_path
        self.metadata_file = os.path.join(directory_path, "scrapedb.sqlite3")

        ## if no path, "debug mode" with in memory db and echo SQL generated.
        if (directory_path == None):
            self.engine = sa.create_engine("sqlite:///:memory:", echo=True)
        else:
            self.engine = sa.create_engine("sqlite:///"+self.metadata_file)
        self.metadata = sa.MetaData()


        self.session = sa.Table('session', self.metadata,
            sa.Column('publisher_name', sa.Text),
            sa.Column('data_version', sa.Text),
            sa.Column('base_url', sa.Text),
            sa.Column('sample', sa.Boolean),
            sa.Column('session_start_datetime', sa.DateTime),

            sa.Column('gather_start_datetime', sa.DateTime, nullable=True),
            sa.Column('gather_finished_datetime', sa.DateTime, nullable=True),
            sa.Column('gather_errors', sa.Text, nullable=True),
            sa.Column('gather_success', sa.Boolean, nullable=False, default=False),

            sa.Column('fetch_start_datetime', sa.DateTime, nullable=True),
            sa.Column('fetch_finished_datetime', sa.DateTime, nullable=True),
            sa.Column('fetch_errors', sa.Text, nullable=True),
            sa.Column('fetch_success', sa.Boolean, nullable=False, default=False),
        )

        self.filestatus = sa.Table('filestatus', self.metadata,
            sa.Column('filename', sa.Text, primary_key=True),
            sa.Column('url', sa.Text, nullable=False),
            sa.Column('data_type', sa.Text, nullable=False),

            sa.Column('gather_error', sa.Text),

            sa.Column('fetch_start_datetime', sa.DateTime, nullable=False),
            sa.Column('fetch_finished_datetime', sa.DateTime, nullable=True),
            sa.Column('fetch_errors', sa.Text, nullable=True),
            sa.Column('fetch_success', sa.Boolean, nullable=False, default=False),
        )

        self.conn = self.engine.connect()
        self.metadata.create_all(self.engine)

    def create_session_metadata(self, publisher_name, sample, url, data_version):
        return self.conn.execute(self.fetch_session.insert(),
            publisher_name = publisher_name,
            sample = sample,
            base_url = url,
            session_start_datetime = datetime.datetime.utcnow(),
            data_version = data_version
            )

    def add_filestatus(self, **kwargs):
        return self.conn.execute(self.filestatus.insert(), **kwargs)
        # dbhandle.add_filestatus(filename = "asdf2", url="fasd", data_type="record", fetch_start_datetime=datetime.datetime.now(), fetch_success=True, store_start_datetime=datetime.datetime.now(), store_success = True)

    """Returns a list of dicts of each filestatus."""
    def list_filestatus(self):
        pass

    """Updates filestatus with start time"""
    def update_filestatus_fetch_start(self, filename):
        pass

    """Updates filestatus when fetched, takes boolean success flag, and json string of errors."""
    def update_filestatus_fetch_end(self, filename, success, errors):
        pass

    """Returns a dict with all keys of the current session."""
    def get_session(self):
        pass

    def update_session_gather_start(self):
        pass

    """Updates session when done gathering, takes boolean success flag, and json string of errors."""
    def update_session_gather_end(self, success, errors):
        pass

    def update_session_fetch_start(self):
        pass

    """Updates session when done fetching, takes boolean success flag, and json string of errors."""
    def update_session_fetch_end(self, success, errors):
        pass
