import sqlite3
import openpyxl

wb = openpyxl.load_workbook('FR.xlsx')
conn = sqlite3.connect('Test.db')
c = conn.cursor()

for sheet in wb.get_sheet_names():
    # TODO: input the row headers into the database to populate the facts table
    wSheet = wb.get_sheet_by_name(sheet)
    print wSheet['A10'].value
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
