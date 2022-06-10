from pandas.io.sql import to_sql
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
import sys
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.exc import SQLAlchemyError


# reading data into memory before database population
air_data, schema_data = 'bristol-air-quality-data/clean.csv', 'bristol-air-quality-data/schema.csv'

#stations table, without duplicates
station_df = pd.read_csv(air_data, sep=';', 
   usecols=('SiteID', 'Location', 'geo_point_2d'))
station_df = station_df.drop_duplicates()


#readings table
reading_df = pd.read_csv(air_data, sep=';',
   usecols=('Date Time', 'NOx', 'NO2', 'NO', 'PM10', 'NVPM10',
   'VPM10', 'NVPM2.5', 'PM2.5', 'VPM2.5', 'CO', 'O3', 'SO2', 'Temperature',
   'RH', 'Air Pressure', 'DateStart', 'DateEnd', 'Current', 'Instrument Type', 'SiteID'
   ), 
   low_memory=False)

# the name and order of the headings in the dataframe must match the table schema already implemented in MariaDB
reading_df = reading_df[['Date Time', 'NOx', 'NO2', 'NO', 'PM10', 'NVPM10',
'VPM10', 'NVPM2.5', 'PM2.5', 'VPM2.5', 'CO', 'O3', 'SO2', 'Temperature',
'RH', 'Air Pressure', 'DateStart', 'DateEnd', 'Current', 'Instrument Type', 'SiteID']]
#reading_df.rename(columns={'SiteID':'SiteID-fk'}, inplace=True)

# duplicates are dropped if they exist
reading_df = reading_df.drop_duplicates()
reading_df.index = reading_df.index + 1

# schema table
schema_df = pd.read_csv(schema_data, sep=';',
   usecols=('Measure', 'Description', 'Unit'))
try:
   engine = create_engine("mysql://root:@localhost/pollution-db2?charset=utf8mb4")
   if not database_exists(engine.url):
      create_database(engine.url)

   # populate tables
   # stations table
   station_df.to_sql(con=engine, name='stations', if_exists='append', index=False)

   # schema table
   schema_df.to_sql(con=engine, name='schema', if_exists='append', index=True, index_label='SchemaID')

   # readings table
   reading_df.to_sql(con=engine, name='readings', if_exists='append', index=True, index_label='ReadingID',
      dtype={'Date Time':sqlalchemy.DateTime(), 'DateStart':sqlalchemy.DateTime(), 'DateEnd':sqlalchemy.DateTime()})

   with engine.connect() as con:
      con.execute('ALTER TABLE `stations` ADD PRIMARY KEY (`SiteID`);')
      con.execute('ALTER TABLE `readings` ADD PRIMARY KEY (`ReadingID`);')
      con.execute('ALTER TABLE `schema` ADD PRIMARY KEY (`SchemaID`);')
      con.execute('ALTER TABLE `readings` ADD FOREIGN KEY (`SiteID`) REFERENCES stations(`SiteID`);')
      con.close()

   engine.dispose()
except SQLAlchemyError:
   sys.exit("Encountered general SQLAlchemyError. Review DB and code.")