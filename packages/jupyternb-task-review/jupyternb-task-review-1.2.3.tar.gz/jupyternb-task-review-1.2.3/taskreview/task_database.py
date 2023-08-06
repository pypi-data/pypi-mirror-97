"""Module that contains a class to create an instance
to connect to the task database."""

import sqlite3
from sqlite3 import Error
try:
    import pandas as pd
except ModuleNotFoundError:
    pass


class TaskDatabase:
    """
    A class used to get the data from the task review database

    Attributes
    ----------
    conn: Connection
        Connection to sqlite3 Database
    db_file:
        Path to database file

    Methods
    -------
    create_connection(db_file)
        Create connection to sqlite3 database at path db_file
    fetch_task(query)
        Execute SQL query and return one task from database
    get_data_as_pd_dataframe(query)
        Execute SQL query and return data as pandas dataframe

    """

    def __init__(self, task_db):
        self.conn = self.create_connection(task_db)
        self.db_file = task_db

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
        specified by the db_file

        Parameters
        -------
        db_file
            database file

        Returns
        -------
        Connection
            Connection to the database or None
        """

        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as err:
            print(err)

        return conn

    def fetch_task(self, task_id):
        """ get task from database by id

        Parameters
        -------
        task_id
            id of task to get from database

        Returns
        -------
        sqlite3.Row
            information for task
        """
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()
        try:
            cursor.execute('SELECT * FROM TaskReview WHERE taskID={}'
                           .format(task_id))
        except Error as err:
            print(err)

        task_row = cursor.fetchone()
        return task_row

    def get_dataframe_from_query(self, query):
        """Execute an SQL query and get the data as a pandas dataframe
        from database

        Parameters
        -------
        query : String

        Returns
        -------
        DataFrame
            Data of the SQL query
        """

        try:
            pd_con = sqlite3.connect(self.db_file)
            pd.set_option('precision', 15)
            dataframe = pd.read_sql_query(query, pd_con)
            dataframe = dataframe.round(12)
            pd_con.close()
            return dataframe
        except NameError:
            print('Bitte installiere pandas und/oder spark, \
                um PandasDataframeTasks oder SparkDataframeTasks zu verwenden.')
