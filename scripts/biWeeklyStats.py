from urllib.request import Request, urlopen
import json
import datetime
import gitterAPI
import googleAnalytics
import psqlStats
import metastoreDataAPI
import googleSpreadsheetUtils


def getBiWeeklyStats(biWeeklyStatsFieldsNameList):
    thursdayDate = '2018-05-17'  # datetime.now().strftime("%Y-%m-%d"),
    wednesdayCurrentWeekDate = '2018-05-16'
    thursdayTwoWeeksAgo = '2018-05-03'

    biWeeklyStats = {}
    for field in biWeeklyStatsFieldsNameList:
        biWeeklyStats[field] = ''
    biWeeklyStats['Date'] = thursdayDate
    biWeeklyStats['Total Users'] = psqlStats.getCountOfTotalUsers()
    biWeeklyStats['Downloads CLI (npm)'] = getNumberOfCliDownloadsNPM()
    biWeeklyStats['Number of (new = last 2w) users who publishes any dataset'] = psqlStats.getCountOfNewUsersWhoPublishedDatasetBetweenDates(thursdayTwoWeeksAgo, wednesdayCurrentWeekDate)
    biWeeklyStats['How many of these push more than one dataset?'] = psqlStats.getCountOfNewUsersWhoPublishedMoreThanOneDatasetBetweenDates(thursdayTwoWeeksAgo, wednesdayCurrentWeekDate)
    biWeeklyStats['Total published (public) datasets'] = metastoreDataAPI.getCountOfPublishedDatasets()
    biWeeklyStats['Total number of new datasets in last 2w'] = psqlStats.getCountOfNewDatasetsBetweenDates(thursdayTwoWeeksAgo, wednesdayCurrentWeekDate)
    biWeeklyStats['Number of members on datahubio chat on gitter'] = gitterAPI.getCountOfUsersInDatahubChatRoom()

    biWeeklyGoogleAnalyticsStats = googleAnalytics.getStats('biweekly', thursdayTwoWeeksAgo, wednesdayCurrentWeekDate)
    for field in biWeeklyGoogleAnalyticsStats:
        biWeeklyStats[field] = biWeeklyGoogleAnalyticsStats[field]
        if field in ['Number of pushes (daily average)', 'Number of data requests (daily average)', 'Site traffic (daily average)']:
            biWeeklyStats[field] = round(int(biWeeklyStats[field])/14, 2)
    return biWeeklyStats


def getNumberOfCliDownloadsNPM():
    npmApiUrl = 'https://api.npmjs.org/downloads/point/2018-05-03:2018-05-16/data-cli'
    response = urlopen(Request(npmApiUrl))
    numberOfCliDownloadsNPM = json.loads(response.read())['downloads']
    return numberOfCliDownloadsNPM


biWeeklyStatsFieldsNameList = [
    'Date', 'Total Users', 'Total new users', 'Downloads CLI (npm)',
    'Downloads CLI (GA)', 'cli-windows', 'cli-linux', 'cli-macos',
    'Number of (new = last 2w) users who publishes any dataset',
    'How many of these push more than one dataset?', 'Number of first runs of `data`',
    'help', 'noArgs', 'validate', 'push', 'get', 'cat', 'info', 'init',
    'login', 'Site traffic (daily average)', 'Total published (public) datasets',
    'Total number of new datasets in last 2w', 'Number of pushes (daily average)',
    'Number of members on datahubio chat on gitter', 'Number of data requests (daily average)',
    'Number of unique visits'
]
biWeeklyStatsWorksheet = googleSpreadsheetUtils.setUpStatsWorksheet(
    spreadsheetName="Stats Test",  # "DataHub v3 Stats & Metrics",
    worksheetName="Biweekly Stats",
    fieldNamesList=biWeeklyStatsFieldsNameList
)
biWeeklyStats = getBiWeeklyStats(biWeeklyStatsFieldsNameList)
googleSpreadsheetUtils.updateWorksheetAfterLastRow(biWeeklyStatsWorksheet, biWeeklyStats)