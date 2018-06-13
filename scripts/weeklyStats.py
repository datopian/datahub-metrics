# Running this script gives stats for previous week but bear in mind that it
# should be run on monday as number of members on datahub/chat channel can't be obtained for specific dates, only current one

import gitterAPI
import googleSpreadsheetUtils
import datetime
import googleAnalytics


def getWeeklyStats():
    currentWeekMondayDate = getCurrentWeekMondayDate()
    sundayPreviousWeekDate = (currentWeekMondayDate + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
    mondayPreviousWeekDate = (currentWeekMondayDate + datetime.timedelta(weeks=-1)).strftime("%Y-%m-%d")

    weeklyStats = {}
    weeklyStats['Date'] = currentWeekMondayDate.strftime("%Y-%m-%d")
    try:
        weeklyStats['Number of members on datahubio chat on gitter (every monday)'] = gitterAPI.getCountOfUsersInDatahubChatRoom()
    except:
        weeklyStats['Number of members on datahubio chat on gitter (every monday)'] = 'ERROR - check authentication'
    weeklyStatsFromGoogleAnalytics = googleAnalytics.getStats('weekly', mondayPreviousWeekDate, sundayPreviousWeekDate)
    weeklyStats = {**weeklyStats, **weeklyStatsFromGoogleAnalytics}
    return weeklyStats


def getCurrentWeekMondayDate():
    today = datetime.date.today()
    currentWeekMondayDate = today + datetime.timedelta(days=-today.weekday())
    return currentWeekMondayDate


def main(stageSpreadsheetName):
    print('running weekly stats')
    weeklyStatsFieldNamesList = [
            'Date', 'Number of members on datahubio chat on gitter (every monday)',
            'Site traffic weekly (measured every monday for the last week)',
            'Total number of data requests per week'
    ]
    weeklyStatsWorksheet = googleSpreadsheetUtils.setUpStatsWorksheet(
        spreadsheetName=stageSpreadsheetName,
        worksheetName="Weekly Stats",
        fieldNamesList=weeklyStatsFieldNamesList
    )
    weeklyStats = getWeeklyStats()
    googleSpreadsheetUtils.updateWorksheetAfterLastRow(weeklyStatsWorksheet, weeklyStats)
