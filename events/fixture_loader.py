import json
import os

from sqlalchemy import Table, select, func

from settings import get_app, db

app = get_app()

FIXTURES_DIR = "./fixtures"


class Loader(object):
    """
    Reusable class for loading fixture data into databases.
    Initialize with an in-context application and database engine.
    """

    def __init__(self, fixtures):
        self.data = None
        self.app = get_app()
        self.connection = db.engine.connect()
        self.fixtures = fixtures
        self.metadata = db.metadata

    def load(self):
        for filename in self.fixtures:
            filepath = os.path.join(FIXTURES_DIR, filename)
            with open(filepath) as file_in:
                self.data = json.load(file_in)
                try:
                    self.load_from_file()
                except Exception as err:
                    print("{0} Load Error on {1}".format(err, filename))

    def load_from_file(self):
        table_name = self.data[0]["table"]
        records = self.data[0]["records"]

        table = Table(table_name, self.metadata)
        primary_keys = self.get_primary_keys(table)

        with self.connection.begin():
            for record in records:
                existing_record = self.get_existing_record(table, primary_keys, record)
                if existing_record:
                    where_conditions = [getattr(table.c, pk) == record[pk] for pk in primary_keys]
                    update_statement = table.update().where(*where_conditions).values(**record)
                    self.connection.execute(update_statement)
                    print("{0} Updated".format(table_name))
                else:
                    self.connection.execute(table.insert().values(**record))
                    print("{0} Loaded".format(table_name))

        # Adjust sequence
        max_id = self.get_max_id(table)
        if max_id:
            sequence_name = f"{table_name}_id_seq"
            self.connection.execute(f"ALTER SEQUENCE {sequence_name} RESTART WITH {max_id + 1}")

    def get_primary_keys(self, table):
        return [col.name for col in table.primary_key.columns]

    def get_existing_record(self, table, primary_keys, record):
        select_query = select([table]).where(
            *[getattr(table.c, pk) == record[pk] for pk in primary_keys]
        )
        result = self.connection.execute(select_query)
        return result.fetchone()

    def get_max_id(self, table):
        max_id_query = select([func.max(table.c.id)])
        result = self.connection.execute(max_id_query)
        return result.scalar()


@app.cli.command("loaddata")
def loaddata():
    """
    Load the test data fixtures into database
    """
    print("Loading data into database...")
    fixtures = [
    ]
    loader = Loader(fixtures)
    try:
        loader.load()
    except Exception as e:
        print(e, "error")


@app.cli.command("load_templates")
def load_templates():
    """
    Load data into the specified table.
    """
    with open('fixtures/templates.py', 'r') as file:
        code = compile(file.read(), 'fixtures/templates.py', 'exec')
        # Execute the parsed code in a new namespace
        exec(code, globals())

        print("Loading templates into database...")
        loader = Loader([])
        try:
            loader.data = [
                {
                    "table": "email_template",
                    "records": templates_list
                }
            ]
            loader.load_from_file()
        except Exception as e:
            print(e, "error")
