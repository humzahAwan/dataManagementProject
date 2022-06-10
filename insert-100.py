import csv
import itertools
import datetime

count = 1
with open('bristol-air-quality-data\clean.csv') as csvfile:
    for row in itertools.islice(csv.DictReader(csvfile, delimiter=';'),100):
    
        del row['Location']
        del row['geo_point_2d']

        date_t = datetime.datetime.fromisoformat(row['Date Time'][:-6])
        date_t.strftime('%Y-%m-%d %H:%M:%S')
        row['Date Time'] = date_t

        date_s = datetime.datetime.fromisoformat(row['DateStart'][:-6])
        date_s.strftime('%Y-%m-%d %H:%M:%S')
        row['DateStart'] = date_s

        if row['DateEnd']:
            date_e = datetime.datetime.fromisoformat(row['DateEnd'][:-6])
            date_e.strftime('%Y-%m-%d %H:%M:%S')
            row['DateEnd'] = date_e
    
        record = [row['Date Time'], row['NOx'], row['NO2'], row['NO'], row['PM10'], row['NVPM10'],
                row['VPM10'], row['NVPM2.5'], row['PM2.5'], row['CO'], row['O3'], row['SO2'], 
                row['Temperature'], row['RH'], row['Air Pressure'], row['DateStart'],
                row['DateEnd'], row['Current'], row['Instrument Type'], row['SiteID']]

        record_in = ["'" + str(x) + "'" for x in record]

        record_in = ",".join(record_in)

        record_in = record_in.replace("''", "NULL")
        record_in = record_in.replace("'True'", " True")
        record_in = record_in.replace("'False'", " False")

        sql_1 = "INSERT INTO `readings` VALUES\n"
        sql_2 = '(' + str(count) + ', ' + record_in + '),' + '\n'
        count += 1

        sql = sql_1 + sql_2[:-2] + ';'
        file = open("insert-100.sql", "a")
        file.write(sql + '\n')
csvfile.close()