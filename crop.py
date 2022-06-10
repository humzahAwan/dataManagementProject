
import csv

with open('bristol-air-quality-data/bristol-air-quality-data.csv', 'r') as datafile, open('bristol-air-quality-data/crop.csv', 'w', newline='')  as outputfile:
    dataread = csv.reader(datafile, delimiter=';')
    datawrite = csv.writer(outputfile, delimiter=';', lineterminator='\n')
    header = next(dataread)
    datawrite.writerow(header)
    year1 = 2010
    for row in dataread:
        year2 = row[0][0:4]
        if year2.isdigit() and int(year2) >= year1:
            datawrite.writerow(row)


        






    


