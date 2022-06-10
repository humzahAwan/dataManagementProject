import csv

# Details for SiteID and corresponding location were taken from the assignment outline.
idList = [188, 203, 206, 209, 213, 215, 228, 270, 271, 375, 395, 452, 447, 459, 463, 481, 500, 501]
locList = ['AURN Bristol Centre', 'Brislington Depot', 'Rupert Street', 'IKEA M32', 'Old Market', 'Parson Street School', 'Temple Meads Station', 'Wells Road', 'Trailer Portway P&R', 'Newfoundland Road Police Station', "Shiner's Garage", 'AURN St Pauls', 'Bath Road', 'Cheltenham Road \ Station Road', 'Fishponds Road', 'CREATE Centre Roof', 'Temple Way', 'Colston Avenue']

# Dictionary containing SiteIDs paired with corresponding locations.
id_loc = {idList[i]:locList[i] for i in range (0,len(idList))}
#print(id_loc)

# Input and output files open and reader/writer objects created.
with open('bristol-air-quality-data/crop.csv', 'r') as infile, open('bristol-air-quality-data/clean.csv', 'w', newline = '') as outfile:
    dataread = csv.reader(infile, delimiter=';')
    datawrite = csv.writer(outfile, delimiter = ';', lineterminator='\n')
    header = next(dataread)
    datawrite.writerow(header)

    x=1
    for row in dataread:
        x +=1
        # Rows that with no value for SiteID have their number printed to the console.
        if len(row[4]) == 0:
            print('Row ', x, 'is missing the SiteID')
        # Rows with correctly paired SiteID and Location are written in the output file: cleaned.csv.
        else:
            row_id_loc = (int(row[4]),row[17])

            if row_id_loc in id_loc.items():
                datawrite.writerow(row)
            # Rows with mismatched pairs are not written to the output file and their row number and mismatched values are printed to the console.
            else:
                print('Row ', x ,'has a mismatched fields.\n It\'s ID:', row[4] ,"does not match it's location: ", row[17])


