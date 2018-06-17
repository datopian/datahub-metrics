from oauth2client.service_account import ServiceAccountCredentials
import gspread
import sys
import csv


def setUpStatsWorksheet(spreadsheetName, worksheetName, fieldNamesList):
    statsSpreadsheetObject = openSpreadsheet(spreadsheetName)
    statsWorksheetObject = statsSpreadsheetObject.worksheet(worksheetName)
    if not checkFieldAndColumnNamesMatch(
        worksheet=statsWorksheetObject,
        fieldNamesList=fieldNamesList
    ):
        sys.exit()
    return statsWorksheetObject


def openSpreadsheet(spreadsheetName):
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    jsonKeyFileNamePath = 'Gspread.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        jsonKeyFileNamePath, scope
    )
    gc = gspread.authorize(credentials)
    spreadsheetObject = gc.open(spreadsheetName)
    return spreadsheetObject


def updateWorksheetAfterLastRow(worksheet, statsData):
    lastRowIndex = obtainIndexOfLastRow(worksheet)
    columnIndexesOfFieldCells = obtainColumnIndexesOfFieldCells(worksheet, list(statsData.keys()))
    if 'Total new users' in statsData:
        statsData['Total new users'] = statsData['Total Users'] - int(worksheet.cell(lastRowIndex, columnIndexesOfFieldCells['Total Users']).value)
    if 'Data growth' in statsData:
        statsData['Data growth'] = statsData['Data stored (Published)'] - int(worksheet.cell(lastRowIndex, columnIndexesOfFieldCells['Data stored (Published)']).value)
    for field in statsData:
        worksheet.update_cell(lastRowIndex+1, columnIndexesOfFieldCells[field], statsData[field])


def obtainIndexOfLastRow(worksheet):
    indexOfLastRow = len([y for y in worksheet.col_values(1) if y != ""])
    return indexOfLastRow


def obtainColumnIndexesOfFieldCells(worksheet, fieldList):
    columnIndexesOfFieldCells = {}
    columnNamesList = obtainColumnNamesFromSheet(worksheet)
    for field in fieldList:
        columnIndexesOfFieldCells[field] = columnNamesList.index(field) + 1
    return columnIndexesOfFieldCells


def obtainColumnNamesFromSheet(worksheet):
    columnNamesList = [x for x in worksheet.row_values(1) if x != ""]
    return columnNamesList


def checkFieldAndColumnNamesMatch(worksheet, fieldNamesList):
    columnNamesList = obtainColumnNamesFromSheet(worksheet)
    if set(fieldNamesList) == set(columnNamesList):
        print('Column names in spreadsheet match field names. Working ...')
        return True
    else:
        fieldNamesNotInSpreadsheet = [x for x in fieldNamesList if x not in columnNamesList]
        columnNamesNotInFieldNames = [x for x in columnNamesList if x not in fieldNamesList]
        print('Column names do not match those in script. Please recheck script')
        print(fieldNamesNotInSpreadsheet, columnNamesNotInFieldNames)
        return False


def downloadWorksheetAsCsvFile(worksheetObject, csvFileName):
    with open(csvFileName, 'w') as f:
        writer = csv.writer(f)
        worksheetRows = worksheetObject.get_all_values()
        writer.writerows([worksheetRows[0]] + worksheetRows[3:])
