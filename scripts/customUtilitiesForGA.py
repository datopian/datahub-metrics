cliActionMetrics = [{'expression': 'ga:uniqueEvents'}]

##########################################################################
# FIELDS
##########################################################################

statsFields = {
    'daily': {
        'Clicks on download link (csv + json + zip)', 'cli-macos', 'cli-linux',
        'cli-windows', 'data-desktop', 'Download page (unique pageviews)',
        'sign-in-pricing-page', 'sign-up-pricing-page', 'contact-us-pricing-page',
        'Pricing page (unique pageviews)', 'Site Traffic', 'Total number of data requests'
    },
    'weekly': {
        'Site traffic weekly (measured every monday for the last week)',
        'Total number of data requests per week'
    },
    'biweekly': {
        'Downloads CLI (GA)', 'cli-windows', 'cli-linux', 'cli-macos',
        'Number of first runs of `data`', 'help', 'noArgs', 'validate', 'push',
        'get', 'cat', 'info', 'init', 'login', 'Site traffic (daily average)',
        'Number of pushes (daily average)', 'Number of data requests (daily average)',
        'Number of unique visits'
    }
}

##########################################################################
# METRICS
##########################################################################

statsMetrics = {
    'daily': {
        'Clicks on download link (csv + json + zip)': [{'expression': 'ga:uniqueEvents'}],
        'cli-macos': [{'expression': 'ga:totalEvents'}],
        'cli-linux': [{'expression': 'ga:totalEvents'}],
        'cli-windows': [{'expression': 'ga:totalEvents'}],
        'data-desktop': [{'expression': 'ga:totalEvents'}],
        'Download page (unique pageviews)': [{'expression': 'ga:uniquePageviews'}],
        'sign-in-pricing-page': [{'expression': 'ga:uniqueEvents'}],
        'sign-up-pricing-page': [{'expression': 'ga:uniqueEvents'}],
        'contact-us-pricing-page': [{'expression': 'ga:uniqueEvents'}],
        'Pricing page (unique pageviews)': [{'expression': 'ga:uniquePageviews'}],
        'Site Traffic': [{'expression': 'ga:users'}],
        'Total number of data requests': [{'expression': 'ga:totalEvents'}],
        'Cli Action': cliActionMetrics
    },
    'weekly': {
        'Site traffic weekly (measured every monday for the last week)': [{'expression': 'ga:users'}],
        'Total number of data requests per week': [{'expression': 'ga:totalEvents'}]
    },
    'biweekly': {
        'Downloads CLI (GA)': cliActionMetrics,
        'cli-windows': [{'expression': 'ga:totalEvents'}],
        'cli-linux': [{'expression': 'ga:totalEvents'}],
        'cli-macos': [{'expression': 'ga:totalEvents'}],
        'Number of first runs of `data`': cliActionMetrics,
        'help': cliActionMetrics,
        'noArgs': cliActionMetrics,
        'validate': cliActionMetrics,
        'push': cliActionMetrics,
        'get': cliActionMetrics,
        'cat': cliActionMetrics,
        'info': cliActionMetrics,
        'init': cliActionMetrics,
        'login': cliActionMetrics,
        'Site traffic (daily average)': [{'expression': 'ga:users'}],
        'Number of pushes (daily average)': cliActionMetrics,
        'Number of data requests (daily average)': [{'expression': 'ga:totalEvents'}],
        'Number of unique visits': [{'expression': 'ga:newUsers'}]
    }
}

##########################################################################
# FILTERS
##########################################################################

dailyStatsFilters = {
    'Clicks on download link (csv + json + zip)': [
        {'filters': [{'dimensionName': 'ga:eventCategory', 'expressions': 'outbound'}]},
        {'filters': [{'dimensionName': 'ga:eventAction', 'expressions': 'click'}]},
        {'filters': [{'dimensionName': 'ga:eventLabel', 'expressions': '/r/'}]}
    ],
    'cli-macos': [
        {'filters': [{'dimensionName': 'ga:pagePath', 'expressions': '/download'}]},
        {'filters': [{'dimensionName': 'ga:eventCategory', 'expressions': 'outbound'}]},
        {'filters': [{'dimensionName': 'ga:eventAction', 'expressions': 'click'}]},
        {'filters': [{'dimensionName': 'ga:eventLabel', 'expressions': 'bin-macos'}]}
    ],
    'cli-linux': [
        {'filters': [{'dimensionName': 'ga:pagePath', 'expressions': '/download'}]},
        {'filters': [{'dimensionName': 'ga:eventCategory', 'expressions': 'outbound'}]},
        {'filters': [{'dimensionName': 'ga:eventAction', 'expressions': 'click'}]},
        {'filters': [{'dimensionName': 'ga:eventLabel', 'expressions': 'bin-linux'}]}
    ],
    'cli-windows': [
        {'filters': [{'dimensionName': 'ga:pagePath', 'expressions': '/download'}]},
        {'filters': [{'dimensionName': 'ga:eventCategory', 'expressions': 'outbound'}]},
        {'filters': [{'dimensionName': 'ga:eventAction', 'expressions': 'click'}]},
        {'filters': [{'dimensionName': 'ga:eventLabel', 'expressions': 'bin-windows'}]}
    ],
    'data-desktop': [
        {'filters': [{'dimensionName': 'ga:pagePath', 'expressions': '/download'}]},
        {'filters': [{'dimensionName': 'ga:eventCategory', 'expressions': 'outbound'}]},
        {'filters': [{'dimensionName': 'ga:eventAction', 'expressions': 'click'}]},
        {'filters': [{'dimensionName': 'ga:eventLabel', 'expressions': 'data-desktop-app'}]}
    ],
    'Download page (unique pageviews)': [
        {'filters': [{'dimensionName': 'ga:PagePath', 'expressions': '/download'}]}
    ],
    'sign-in-pricing-page': [
        {'filters': [{'dimensionName': 'ga:eventCategory', 'expressions': 'pricingPage'}]},
        {'filters': [{'dimensionName': 'ga:eventAction', 'expressions': 'click'}]},
        {'filters': [{'dimensionName': 'ga:eventLabel', 'expressions': 'Sign in'}]}
    ],
    'sign-up-pricing-page': [
        {'filters': [{'dimensionName': 'ga:eventCategory', 'expressions': 'pricingPage'}]},
        {'filters': [{'dimensionName': 'ga:eventAction', 'expressions': 'click'}]},
        {'filters': [{'dimensionName': 'ga:eventLabel', 'expressions': 'Sign up'}]}
    ],
    'contact-us-pricing-page': [
        {'filters': [{'dimensionName': 'ga:eventCategory', 'expressions': 'pricingPage'}]},
        {'filters': [{'dimensionName': 'ga:eventAction', 'expressions': 'click'}]},
        {'filters': [{'dimensionName': 'ga:eventLabel', 'expressions': 'Contact us'}]}
    ],
    'Pricing page (unique pageviews)': [
        {'filters': [{'dimensionName': 'ga:PagePath', 'expressions': '/pricing'}]}
    ],
    'Site Traffic': [
        {'filters': [{'dimensionName': 'ga:channelGrouping', 'expressions': ''}]}
    ],
    'Total number of data requests': [
        {'filters': [{'dimensionName': 'ga:eventCategory', 'expressions': 'requests'}]},
        {'filters': [{'dimensionName': 'ga:eventAction', 'expressions': 'data-request'}]}
     ]
     # 'Cli Action': [
     #    {'filters': [{'dimensionName': 'ga:eventCategory', 'expressions': 'cli'}]},
     #    {'filters': [{'dimensionName': 'ga:eventAction', 'expressions': 'click'}]},
     # ]
}

weeklyStatsFilters = {
    'Site traffic weekly (measured every monday for the last week)': dailyStatsFilters['Site Traffic'],
    'Total number of data requests per week': dailyStatsFilters['Total number of data requests']
}

biWeeklyStatsFilters = {
    'Total number of data requests per week': dailyStatsFilters['Total number of data requests'],
    'Downloads CLI (GA)': [
        {'filters': [{'dimensionName': 'ga:pagePath', 'expressions': '/download'}]},
        {'filters': [{'dimensionName': 'ga:eventCategory', 'expressions': 'outbound'}]},
        {'filters': [{'dimensionName': 'ga:eventLabel', 'expressions': 'https://github.com/datahq/data-cli/releases/download/'}]}
    ],
    'cli-windows': dailyStatsFilters['cli-windows'],
    'cli-linux': dailyStatsFilters['cli-linux'],
    'cli-macos': dailyStatsFilters['cli-macos'],
    'Number of first runs of `data`': [
        {'filters': [{'dimensionName': 'ga:eventCategory', 'expressions': 'cli'}]},
        {'filters': [{'dimensionName': 'ga:eventAction', 'expressions': 'first-run'}]},
    ],
    'help': [
        {'filters': [{'dimensionName': 'ga:eventCategory', 'expressions': 'cli'}]},
        {'filters': [{'dimensionName': 'ga:eventAction', 'expressions': 'help'}]},
    ],
    'noArgs': [
        {'filters': [{'dimensionName': 'ga:eventCategory', 'expressions': 'cli'}]},
        {'filters': [{'dimensionName': 'ga:eventAction', 'expressions': 'noArgs'}]},
    ],
    'validate': [
        {'filters': [{'dimensionName': 'ga:eventCategory', 'expressions': 'cli'}]},
        {'filters': [{'dimensionName': 'ga:eventAction', 'expressions': 'validate'}]},
    ],
    'push': [
        {'filters': [{'dimensionName': 'ga:eventCategory', 'expressions': 'cli'}]},
        {'filters': [{'dimensionName': 'ga:eventAction', 'expressions': 'push'}]},
    ],
    'get': [
        {'filters': [{'dimensionName': 'ga:eventCategory', 'expressions': 'cli'}]},
        {'filters': [{'dimensionName': 'ga:eventAction', 'expressions': 'get'}]},
    ],
    'cat': [
        {'filters': [{'dimensionName': 'ga:eventCategory', 'expressions': 'cli'}]},
        {'filters': [{'dimensionName': 'ga:eventAction', 'expressions': 'cat'}]},
    ],
    'info': [
        {'filters': [{'dimensionName': 'ga:eventCategory', 'expressions': 'cli'}]},
        {'filters': [{'dimensionName': 'ga:eventAction', 'expressions': 'info'}]},
    ],
    'init': [
        {'filters': [{'dimensionName': 'ga:eventCategory', 'expressions': 'cli'}]},
        {'filters': [{'dimensionName': 'ga:eventAction', 'expressions': 'init'}]},
    ],
    'login': [
        {'filters': [{'dimensionName': 'ga:eventCategory', 'expressions': 'cli'}]},
        {'filters': [{'dimensionName': 'ga:eventAction', 'expressions': 'login'}]},
    ],
    'Number of pushes (daily average)': [
        {'filters': [{'dimensionName': 'ga:eventCategory', 'expressions': 'cli'}]},
        {'filters': [{'dimensionName': 'ga:eventAction', 'expressions': '^push$'}]}
    ],
    'Site traffic (daily average)': dailyStatsFilters['Site Traffic'],
    'Number of data requests (daily average)': dailyStatsFilters['Total number of data requests'],
    'Number of unique visits': dailyStatsFilters['Site Traffic']
}

statsFilters = {
    'daily': dailyStatsFilters,
    'weekly': weeklyStatsFilters,
    'biweekly': biWeeklyStatsFilters
}
