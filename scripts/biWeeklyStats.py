import json
import gitterAPI
import googleAnalytics
import psqlStats
import metastoreDataAPI
import googleSpreadsheetUtils
from urllib.request import Request, urlopen
from datetime import date, timedelta
from dataRequests import getNumberOfDataRequestsForPreviousSprint


def getBiWeeklyStats(biWeeklyStatsFieldsNameList):
    todayDate = date.today()
    wednesdayCurrentWeekDate = getCurrentWednesdayDate(todayDate)
    thursdayTwoWeeksAgoDate = (wednesdayCurrentWeekDate + timedelta(days=-13)).strftime("%Y-%m-%d")
    wednesdayCurrentWeekDate = wednesdayCurrentWeekDate.strftime("%Y-%m-%d")

    biWeeklyStats = {}
    for field in biWeeklyStatsFieldsNameList:
        biWeeklyStats[field] = ''
    biWeeklyStats['Date'] = todayDate.strftime("%Y-%m-%d")
    biWeeklyStats['Total Users'] = psqlStats.getCountOfTotalUsers()
    biWeeklyStats['Downloads CLI (npm)'] = getNumberOfCliDownloadsNPM(thursdayTwoWeeksAgoDate, wednesdayCurrentWeekDate)
    biWeeklyStats['Number of (new = last 2w) users who publishes any dataset'] = psqlStats.getCountOfNewUsersWhoPublishedDatasetBetweenDates(thursdayTwoWeeksAgoDate, wednesdayCurrentWeekDate)
    biWeeklyStats['How many of these push more than one dataset?'] = psqlStats.getCountOfNewUsersWhoPublishedMoreThanOneDatasetBetweenDates(thursdayTwoWeeksAgoDate, wednesdayCurrentWeekDate)
    biWeeklyStats['Total published (public) datasets'] = metastoreDataAPI.getCountOfPublishedDatasets()
    biWeeklyStats['Total number of new datasets in last 2w'] = psqlStats.getCountOfNewDatasetsBetweenDates(thursdayTwoWeeksAgoDate, wednesdayCurrentWeekDate)
    biWeeklyStats['Number of members on datahubio chat on gitter'] = gitterAPI.getCountOfUsersInDatahubChatRoom()
    biWeeklyStats['Number of data requests (daily average)'] = str(round(getNumberOfDataRequestsForPreviousSprint(todayDate)/14, 2))

    biWeeklyGoogleAnalyticsStats = googleAnalytics.getStats('biweekly', thursdayTwoWeeksAgoDate, wednesdayCurrentWeekDate)
    for field in biWeeklyGoogleAnalyticsStats:
        biWeeklyStats[field] = biWeeklyGoogleAnalyticsStats[field]
        if field in ['Number of pushes (daily average)', 'Site traffic (daily average)']:
            biWeeklyStats[field] = round(int(biWeeklyStats[field])/14, 2)
    biWeeklyStats['Total Unique Visitors'] = biWeeklyGoogleAnalyticsStats['Site traffic (daily average)']
    return biWeeklyStats


def getCurrentWednesdayDate(todayDate):
    currentWeekWednesdayDate = todayDate + timedelta(days=-todayDate.weekday()+2)
    return currentWeekWednesdayDate


def getNumberOfCliDownloadsNPM(startDate, endDate):
    npmApiUrl = 'https://api.npmjs.org/downloads/point/' + startDate + ':' + endDate + '/data-cli'
    response = urlopen(Request(npmApiUrl))
    numberOfCliDownloadsNPM = json.loads(response.read())['downloads']
    return numberOfCliDownloadsNPM


def main(stageSpreadsheetName):
    print('running biweekly stats')
    biWeeklyStatsFieldsNameList = [
        'Date', 'Total Unique Visitors', 'Total Users', 'Total new users', 'Downloads CLI (npm)',
        'Downloads CLI (GA)', 'cli-windows', 'cli-linux', 'cli-macos',
        'Number of (new = last 2w) users who publishes any dataset',
        'How many of these push more than one dataset?', "number of first runs of `data`",
        'help', 'noArgs', 'validate', 'push', 'get', 'cat', 'info', 'init',
        'login', 'Site traffic (daily average)', 'Total published (public) datasets',
        'Total number of new datasets in last 2w', 'Number of pushes (daily average)',
        'Number of members on datahubio chat on gitter', 'Number of data requests (daily average)',
        'Number of unique visits'
    ]
    biWeeklyStatsWorksheet = googleSpreadsheetUtils.setUpStatsWorksheet(
        spreadsheetName=stageSpreadsheetName,
        worksheetName="Biweekly Stats",
        fieldNamesList=biWeeklyStatsFieldsNameList
    )
    biWeeklyStats = getBiWeeklyStats(biWeeklyStatsFieldsNameList)
    googleSpreadsheetUtils.updateWorksheetAfterLastRow(biWeeklyStatsWorksheet, biWeeklyStats)
    googleSpreadsheetUtils.downloadWorksheetAsCsvFile(biWeeklyStatsWorksheet, 'biweekly_stats.csv')
