"""Google Analytics Reporting API V4."""

import argparse
import httplib2
import customUtilitiesForGA
from apiclient.discovery import build
from oauth2client import client
from oauth2client import file
from oauth2client import tools


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
CLIENT_SECRETS_PATH = 'client_secrets.json'
VIEW_ID = '157208265'


class GoogleAnalyticsStatsClass:
    """
        Custom made GoogleAnalyticsStatsClass. Created for DataHub and it is
        a modified version of helloAnalytics.py script which can be found at
        https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/installed-py
    """

    def __init__(self, startDate, endDate, metrics, filters):
        self.startDate = startDate
        self.endDate = endDate
        self.dimensions = []
        self.metrics = metrics
        self.filters = filters

    def initializeAnalyticsReporting(self):
        """Initializes the analytics reporting service object.

        Returns an authorized analytics reporting service object.
        """
        # Parse command-line arguments.
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            parents=[tools.argparser])
        flags = parser.parse_args([])

        # Set up a Flow object to be used if we need to authenticate.
        flow = client.flow_from_clientsecrets(
            CLIENT_SECRETS_PATH, scope=SCOPES,
            message=tools.message_if_missing(CLIENT_SECRETS_PATH))

        # Prepare credentials, and authorize HTTP object with them.
        # If the credentials don't exist or are invalid run through the native
        # client flow. The Storage object will ensure that if successful the
        # good credentials will get written back to a file.
        storage = file.Storage('analyticsreporting.dat')
        credentials = storage.get()
        if credentials is None or credentials.invalid:
            credentials = tools.run_flow(flow, storage, flags)
        http = credentials.authorize(http=httplib2.Http())
        analyticsObject = build('analytics', 'v4', http=http, discoveryServiceUrl=DISCOVERY_URI)

        self.analyticsObject = analyticsObject

    def getAnalyticsReport(self):
        # Use the Analytics Service Object to query the Analytics Reporting API V4.
        return self.analyticsObject.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': VIEW_ID,
                        'dateRanges': [{'startDate': self.startDate, 'endDate': self.endDate}],
                        'dimensions': self.dimensions,
                        'metrics': self.metrics,
                        'dimensionFilterClauses': self.filters
                    }]
            }
        ).execute()

    def getAnalyticsResponse(self, reportObject):
        """Parses and prints the Analytics Reporting API V4 response"""

        for report in reportObject.get('reports', []):
            columnHeader = report.get('columnHeader', {})
            dimensionHeaders = columnHeader.get('dimensions', [])
            metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
            rows = report.get('data', {}).get('rows', [])

        for row in rows:
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])

            for header, dimension in zip(dimensionHeaders, dimensions):
                print(header + ': ' + dimension)

            for dateRangeValueObject in dateRangeValues:
                values = dateRangeValueObject.get('values')
                for metricHeader, value in zip(metricHeaders, values):
                    return value


# dateStringsYmd have a date format "%Y-%m-%d"
def getStats(typeOfStat, *dateStringsYmd):
    if typeOfStat not in ['daily', 'weekly', 'biweekly']:
        print('Type of stat not recognised. Please check your spelling. The recognised types are "daily", "weekly" and "biweekly"')
        return
    statsFields = customUtilitiesForGA.statsFields[typeOfStat]
    statsMetrics = customUtilitiesForGA.statsMetrics[typeOfStat]
    statsFilters = customUtilitiesForGA.statsFilters[typeOfStat]

    googleAnalyticsStats = {}
    for field in statsFields:
        gaStatsClass = GoogleAnalyticsStatsClass(
            startDate=dateStringsYmd[0],
            endDate=dateStringsYmd[-1],
            metrics=statsMetrics[field],
            filters=statsFilters[field]
        )
        gaStatsClass.initializeAnalyticsReporting()
        reportObject = gaStatsClass.getAnalyticsReport()
        googleAnalyticsStats[field] = gaStatsClass.getAnalyticsResponse(reportObject)
        if googleAnalyticsStats[field] is None:
            googleAnalyticsStats[field] = '0'

    return googleAnalyticsStats
