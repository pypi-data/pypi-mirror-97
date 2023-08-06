import os
from glob import glob
from unittest import TestCase

from sqlalchemy import MetaData

from openmodule.config import database_folder
from openmodule.database.database import Database

_first_start = True


def delete_all_tables(database: Database):
    assert any(x in database.db_folder for x in ["test"]), "deleting all tables is only for testing"
    metadata = MetaData(bind=database._engine)
    metadata.reflect()
    with database._engine.connect() as con:
        trans = con.begin()

        for table in reversed(metadata.sorted_tables):
            con.execute(table.delete())
        trans.commit()


class SQLiteTestMixin(TestCase):
    """
    Mixin for database cleanup in test cases
    * use create_database = True for an automatic generation of a database
    * use create_database = False and set the database directly
    """
    create_database = True
    database = None
    database_folder = database_folder()
    alembic_path = "../src/database"
    database_name = "database"

    @classmethod
    def setUpClass(cls) -> None:
        # we only know which databases are in use on tear down, so truncating only works in teardown
        # but in order to not be annoyed by failed tests which left broken databases, we delete all databases
        # once initially
        global _first_start
        if _first_start:
            for file in glob(os.path.join(cls.database_folder, "*.sqlite3")):
                os.unlink(file)
                _first_start = False
        if cls.create_database:
            cls.database = Database(cls.database_folder, cls.database_name, cls.alembic_path)
        return super().setUpClass()

    def tearDown(self):
        super().tearDown()
        delete_all_tables(self.database)

    @classmethod
    def tearDownClass(cls):
        if cls.database:
            cls.database.shutdown()
        super().tearDownClass()
