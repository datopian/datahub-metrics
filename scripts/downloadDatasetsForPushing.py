import googleSpreadsheetUtils


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
    spreadsheetName="Stats Test",
    worksheetName="Daily Stats",
    fieldNamesList=dailyStatsFieldsNameList
)
googleSpreadsheetUtils.downloadWorksheetAsCsvFile(dailyStatsWorksheet, 'daily_stats.csv')