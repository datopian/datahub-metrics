# DataHub Metrics

This repo automates daily, weekly and biweekly stats collection for datahub.io. Stats are collected from postgre sql database, metastore api sevice, google analytics and gitter. The script also uploads test csv files via [data-cli](https://github.com/datahq/data-cli) to measure data processing time on website on a daily basis

Once collected the stats are inserted into a google spreadsheet. The stats collection is automated via Travis. There are three scripts that run automatically at specified times.
* dailyStats.py runs every Tuesday, Wednesday, Thursday, Friday and Saturday at 00:05 UTC and collects daily stats for the previous day
* weeklyStats.py runs every Monday at 00:05 UTC and collects stats for the previous week
* biWeeklyStats.py runs every other Thursday at 00:05 UTC and collects stats for previous 14 days which is a duration of our sprint


## Requirements
Scripts are written for python 3.6+. Modules that are required:

- pexpect
- python-dotenv
- psycopg2
- httplib2
- google-api-python-client
- oauth2client
- gspread

To install requirements run `pip install -r requirements.txt`


## License
Public Domain Dedication and License (PDDL)