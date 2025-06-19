from sqlalchemy import insert, Table, Column, Integer, String, MetaData, Float, inspect, create_engine


class PlanktonDB:
    """ This is the main class for interacting with the Plankton database. It does not allow creation
    of tables yet. Just consulting them and inserting data in them."""

    data_phytoplankton_format = {"Species":None, #String
                                 "Date":None, #String of format %Y-%m-%d 00:00:00
                                 "Min_Lon": None, #Float
                                 "Max_Lon": None, # Float
                                 "Min_Lat": None, # Float
                                 "Max_Lat": None, #Float
                                 "Mean_Conc": None, # Float
                                 "Std_Conc": None # Float
                                }

    def __init__(self, database_url, database_name, username, password):
        self.engine = self.connect_to_database(database_url,database_name, username, password)
        self.list_tables = return_list_tables
        self.metadata = MetaData()
        self.table = get_table('blooms')
        

    def connect_to_database(self, database_url,database_name, username, password):
        engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{database_url}:5432/{database_name}')
        return engine

    def return_list_tables():
        inspector = inspect(self.engine)
        return inspector.get_table_names(schema="public")

    def get_table(self, table_name):
        return Table(table_name, self.metadata, autoload_with=self.engine)

    def insert_data(self, data):
    
        with engine.connect() as conn:
             conn.execute(insert(self.table), data)
             conn.commit()

def create_table(engine, name):
    metadata = MetaData()
    
    table = Table(
    name, metadata,
    Column('id',Integer, primary_key = True),
    Column('Species', String),
    Column('Date', String),
    Column('Min_Lon',Integer),
    Column('Max_Lon',Integer),
    Column('Min_Lat',Integer),
    Column('Max_Lat',Integer),
    Column('Mean_Conc',Float),
    Column('Std_Conc',Float))

    metadata.create_all(engine)
    
    return table


