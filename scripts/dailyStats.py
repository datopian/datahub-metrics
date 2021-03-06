import psqlStats
import googleAnalytics
import metastoreDataAPI
import googleSpreadsheetUtils
import testFilesPushToDataHub
from dataRequests import getNumberOfDataRequestsForGivenDate
from datetime import datetime, timedelta


def getDailyStats(dailyStatsFieldsNameList):
    dailyStats = {}
    for field in dailyStatsFieldsNameList:
        dailyStats[field] = ''

    dailyStats['Date'] = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    dailyStats['Total Users'] = psqlStats.getCountOfTotalUsers()
    dailyStats['Total datasets'] = psqlStats.getCountOfAllDatasets()
    dailyStats['Private datasets'] = psqlStats.getCountOfPrivateDatasets()
    dailyStats['Private datasets(extracting our datasets)'] = dailyStats['Private datasets'] - psqlStats.getCountOfPrivateDatasetsExtractingOur()
    dailyStats['Published datasets (DB)'] = psqlStats.getCountOfPublishedDatasets()
    dailyStats['Published datasets (metastore)'] = metastoreDataAPI.getCountOfPublishedDatasets()
    dailyStats['Data stored (Published)'] = metastoreDataAPI.getSizeOfPublishedDatasets()
    dailyStats['Unlisted datasets'] = dailyStats['Total datasets'] - dailyStats['Private datasets'] - dailyStats['Published datasets (DB)']
    dailyStats['Unlisted datasets (extracting our datasets)'] = dailyStats['Unlisted datasets'] - psqlStats.getCountOfUnlistedDatasets()
    dailyStats['Number of pushes'] = psqlStats.getCountOfAllPushRequests(dailyStats['Date'])
    dailyStats['Number of pushes (excluding us)'] = psqlStats.getCountOfPushRequestsExcludingUs(dailyStats['Date'])
    dailyStats['Total number of data requests'] = str(getNumberOfDataRequestsForGivenDate(dailyStats['Date']))
    try:
        timesOfProcessing = testFilesPushToDataHub.getTimesOfProcessing()
        dailyStats['Speed of a 5kb of packaged dataset push (in seconds)'] = timesOfProcessing['5kb-test']
        dailyStats['Speed of a 1Mb of packaged dataset push (in seconds)'] = timesOfProcessing['1mb-test']
    except:
        print('\nThere was an error in test dataset pushing!')
        dailyStats['Speed of a 5kb of packaged dataset push (in seconds)'] = 'ERROR!'
        dailyStats['Speed of a 1Mb of packaged dataset push (in seconds)'] = 'ERROR!'

    dailyGoogleAnalyticsStats = googleAnalytics.getStats('daily', dailyStats['Date'])
    for field in dailyGoogleAnalyticsStats:
        dailyStats[field] = dailyGoogleAnalyticsStats[field]

    # We get 'Total downloads' field with formula:
    dailyStats['Total downloads'] = str(
        int(dailyStats['cli-macos']) + int(dailyStats['cli-linux'])
        + int(dailyStats['cli-windows']) + int(dailyStats['data-desktop'])
    )
    return dailyStats


def main(stageSpreadsheetName):
    print('running daily stats')
    dailyStatsFieldsNameList = [
        'Date', 'Total Users', 'Total new users', 'Published datasets (metastore)',
        'Published datasets (DB)', 'Unlisted datasets', 'Unlisted datasets (extracting our datasets)', 'Private datasets',
        'Private datasets(extracting our datasets)', 'Total datasets', 'Number of pushes', 'Number of pushes (excluding us)',
        'Speed of a 1Mb of packaged dataset push (in seconds)', 'Speed of a 5kb of packaged dataset push (in seconds)',
        'Clicks on download link (csv + json + zip)', 'cli-macos', 'cli-linux', 'cli-windows',
        'data-desktop', 'Total downloads', 'Download page (unique pageviews)', 'sign-in-pricing-page',
        'sign-up-pricing-page', 'contact-us-pricing-page', 'Pricing page (unique pageviews)',
        'Site Traffic', 'Data stored (Published)', 'Data growth', 'Total number of data requests', 'Comment'
    ]

    dailyStatsWorksheet = googleSpreadsheetUtils.setUpStatsWorksheet(
        spreadsheetName=stageSpreadsheetName,
        worksheetName="Daily Stats",
        fieldNamesList=dailyStatsFieldsNameList
    )
    dailyStats = getDailyStats(dailyStatsFieldsNameList)
    googleSpreadsheetUtils.updateWorksheetAfterLastRow(dailyStatsWorksheet, dailyStats)
    googleSpreadsheetUtils.downloadWorksheetAsCsvFile(dailyStatsWorksheet, 'daily_stats.csv')
