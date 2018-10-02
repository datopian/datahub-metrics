import googleSpreadsheetUtils
from datetime import datetime, timedelta


def getAllDatesFromWorksheet():
    timestamps = [x for x in dataRequestsWorksheet.col_values(1)[1:] if x]
    dates = list(map(lambda ts: datetime.strptime(ts, "%m/%d/%Y %H:%M:%S").date(), timestamps))
    return dates


def getNumberOfDataRequestsForPreviousSprint(currentThursdayDate):
    previousSprintDates = [currentThursdayDate - timedelta(i) for i in range(1, 15)]
    numberOfDataRequestsForPreviousSprint = 0
    for date in previousSprintDates:
        numberOfDataRequestsForPreviousSprint += getNumberOfDataRequestsForGivenDate(date)
    return numberOfDataRequestsForPreviousSprint


def getNumberOfDataRequestsForPreviousWeek(currentMondayDate):
    previousWeekDates = [currentMondayDate - timedelta(i) for i in range(1, 8)]
    numberOfDataRequestsForPreviousWeek = 0
    for date in previousWeekDates:
        numberOfDataRequestsForPreviousWeek += getNumberOfDataRequestsForGivenDate(date)
    return numberOfDataRequestsForPreviousWeek


def getNumberOfDataRequestsForGivenDate(date):
    return dates.count(date)


dataRequestsWorksheet = googleSpreadsheetUtils.setUpStatsWorksheet(
    spreadsheetName="Data Request Form (Responses from 2018-07-03)",
    worksheetName="Form Responses 1",
    fieldNamesList=["Timestamp", "Name", "Email", "Dataset category", "I want ...", "In order to ...", "Type of your organization"]
)

dates = getAllDatesFromWorksheet()
