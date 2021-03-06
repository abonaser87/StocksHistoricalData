import csv
import os

bigfile = open('Equites_Historical_Adjusted_Prices_Report.csv')
cfile = csv.reader(bigfile)
fieldnames = ['Sector', 'Name', 'Date', 'Open', 'High', 'Low', 'Close', 'Vol']
temp = []
for row in cfile:
    # Skip the header line
    if not cfile.line_num == 1:
        # create a new file by ticker number
        outfile = csv.writer(open('AdjDaily/{}.csv'.format(row[0]), 'a', newline=''))
        # if it is empty insert the header
        if os.stat('AdjDaily/{}.csv'.format(row[0])).st_size == 0:
            outfile.writerow(fieldnames)
        # temp variable to store the previous row
        temp.append(row[0])
        if cfile.line_num == 2:
            outfile.writerow(row[1:])
        # if this is second line
        if not cfile.line_num == 2:
            # check if the ticker is the same
            if temp[1] == temp[0]:
                # write to the new file without the ticker number
                outfile.writerow(row[1:])
                # remove the last item from the array for checking purpose
                temp.pop()
            else:
                # if this is a new ticker empty the temp array and itereiate
                temp = []
                temp.append(row[0])
