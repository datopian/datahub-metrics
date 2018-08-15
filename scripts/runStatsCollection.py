import datetime
import sys
import dailyStats
import weeklyStats
import biWeeklyStats


def isBetweenTuesdayAndSaturday(currentDate):
    return currentDate.weekday() in range(1, 6)


def isMonday(currentDate):
    return currentDate.weekday() == 0


def isSprintThursday(currentDate):
    with open("archive/last_sprint_date.txt", 'r') as f:
        lastSprintDate = datetime.datetime.strptime(f.read(), "%Y-%m-%d").date()
    if (currentDate - lastSprintDate).days % 14 == 0:
        with open("archive/last_sprint_date.txt", 'w') as w:
            w.write(currentDate.strftime("%Y-%m-%d"))
        return True
    else:
        return False


stage = sys.argv[1] if len(sys.argv) == 2 else 'production'
stageSpreadsheetNameDictionary = {
    'test': 'Stats Test',
    'production': 'DataHub v3 Stats & Metrics'
}
spreadsheetName = stageSpreadsheetNameDictionary[stage]
print('stage = ', stage)
print(spreadsheetName)
currentDate = datetime.date.today()
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
if isBetweenTuesdayAndSaturday(currentDate):
    dailyStats.main(spreadsheetName)
    if isSprintThursday(currentDate):
        biWeeklyStats.main(spreadsheetName)
elif isMonday(currentDate):
    weeklyStats.main(spreadsheetName)
