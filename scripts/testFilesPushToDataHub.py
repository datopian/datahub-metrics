from urllib.request import Request, urlopen
from urllib.error import HTTPError
import re
import time
import pexpect


def requestPageUntilProcessed(url):
    t0 = time.time()
    datasetProcessed = False
    time.sleep(30)
    while not datasetProcessed:
        try:
            html = urlopen(Request(url)).read().decode("utf-8")
            processingTime = round(time.time() - t0, 2)
            print('dataset has been succesfully processed. Time elapsed: ', processingTime)
            return processingTime
        except HTTPError:
            print("dataset is getting processed. Time elapsed: ", round(time.time() - t0, 2))
            time.sleep(2)
        if float(time.time() - t0) > 200:
            print('there was an error, dataset is taking too long to process, exiting ...')
            return '200'


def getTimesOfProcessing():
    processingTimes = {}
    folderWithTestDataForPushing = 'test_push'
    for name in ['5kb-test', '1mb-test']:
        print('data push ' + folderWithTestDataForPushing + '/' + name + '.csv' + ' --published')
        child = pexpect.spawn('data push ' + folderWithTestDataForPushing + '/' + name + '.csv' + ' --published')
        child.expect('Please, confirm name for this dataset:')
        child.sendline(name)
        child.expect("Please, confirm title for this dataset:")
        child.sendline(name)
        byteOutput = child.read()
        outputString = byteOutput.decode("utf-8")
        regex = re.compile('https://datahub.io/Branko-Dj/' + name + '/v/[0-9]+')
        publishingLink = regex.findall(outputString)[0]
        print(publishingLink)
        processingTimes[name] = requestPageUntilProcessed(publishingLink)
        print("Time of processing for ", name, ' t = ', processingTimes[name], 's')
    return processingTimes
