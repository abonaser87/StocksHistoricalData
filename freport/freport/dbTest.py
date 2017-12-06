import sqlite3
import openpyxl

wb = openpyxl.load_workbook('FR.xlsx')
conn = sqlite3.connect('Test.db')
c = conn.cursor()

for sheet in wb.get_sheet_names():
    # TODO: input the row headers into the database to populate the facts table
    wSheet = wb.get_sheet_by_name(sheet)
    if sheet.startswith("!"):
        continue
    cols = wSheet.columns
    x = str(wSheet.title)
    try:
        c.execute("INSERT INTO company (name) VALUES(?)",(x,))
    except:
        c.execute("SELECT id FROM company WHERE name=?",(x,))
        companyId = c.fetchone()[0]
        pass

    for col in cols:
        i = 1
        loop=True
        for cell in col:
            if cell.value == "BALANCE SHEET":
                xy = openpyxl.utils.coordinate_from_string(cell.coordinate)
                row = xy[1]
                col = openpyxl.utils.column_index_from_string(xy[0])
                while loop == True:
                    try:
                        c.execute("INSERT INTO statementRow (statementId,rowOrder,rowTitle) SELECT 1,"+str(i)+",\""+wSheet.cell(row = row+i,column=col).value+"\" WHERE NOT EXISTS(SELECT 1 FROM statementRow where statementId=1 AND rowOrder="+str(i)+" AND rowTitle=\""+wSheet.cell(row = row+i,column=col).value+"\")")
                    except:
                        pass
                    i=i+1
                    if wSheet.cell(row = row+i,column=col).value == None:
                        loop = False

            if cell.value == "STATEMENT OF INCOME":
                xy = openpyxl.utils.coordinate_from_string(cell.coordinate)
                row = xy[1]
                col = openpyxl.utils.column_index_from_string(xy[0])
                while loop == True:
                    try:
                        c.execute("INSERT INTO statementRow (statementId,rowOrder,rowTitle) SELECT 2,"+str(i)+",\""+wSheet.cell(row = row+i,column=col).value+"\" WHERE NOT EXISTS(SELECT 1 FROM statementRow where statementId=2 AND rowOrder="+str(i)+" AND rowTitle=\""+wSheet.cell(row = row+i,column=col).value+"\")")
                    except:
                        pass
                    i = i + 1
                    if wSheet.cell(row = row+i,column=col).value == None:
                        loop = False

            if cell.value == "CASH FLOW":
                xy = openpyxl.utils.coordinate_from_string(cell.coordinate)
                row = xy[1]
                col = openpyxl.utils.column_index_from_string(xy[0])
                while loop == True:
                    try:
                        c.execute("INSERT INTO statementRow (statementId,rowOrder,rowTitle) SELECT 3,"+str(i)+",\""+wSheet.cell(row = row+i,column=col).value+"\" WHERE NOT EXISTS(SELECT 1 FROM statementRow where statementId=3 AND rowOrder="+str(i)+" AND rowTitle=\""+wSheet.cell(row = row+i,column=col).value+"\")")
                    except:
                        pass
                    i = i + 1
                    if wSheet.cell(row=row + i, column=col).value == None or wSheet.cell(row=row+i-1, column=col).value == "Cash at End of Period":
                        loop = False
conn.commit()
c.close()
conn.close()
# def create_table():
#     c.execute("""CREATE TABLE IF NOT EXISTS company (
#     id      integer PRIMARY KEY,
#     name    varchar(255)
# )""")
#     c.execute("""CREATE TABLE IF NOT EXISTS statement (
#     id      integer PRIMARY KEY,
#     name    varchar(255)
# )""")
#     c.execute("""CREATE TABLE IF NOT EXISTS statementRow (
#     id      integer  PRIMARY KEY,
#     statementId integer ,
#     rowOrder  integer ,
#     rowTitle  varchar(255) ,
#     rowDescription varchar(255) NULL,
#     rowProperties varchar(255) NULL,
#     FOREIGN KEY (statementId) REFERENCES statement (id)
# )""")
#
#     c.execute("""CREATE TABLE IF NOT EXISTS statementFact (
#     companyId      integer ,
#     statementRowId integer ,
#     date         date ,
#     amount         numeric ,
#     PRIMARY KEY (date, statementRowId),
#     FOREIGN KEY (companyId) REFERENCES company (id),
#     FOREIGN KEY (statementRowId) REFERENCES statementRow (id)
# )""")
#
#
# create_table()
# Dynamically add data from excel sheet
