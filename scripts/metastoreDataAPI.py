from urllib.parse import urljoin
from urllib.request import Request, urlopen
import json
import envVariables


def getMetastoreDataJSON():
    valid_token = envVariables.JWT_TOKEN
    api_base_url = 'https://' + envVariables.DOMAIN_API
    url_metastore_search = urljoin(api_base_url, 'metastore/search')
    headers = {'Auth-Token': valid_token}
    response = urlopen(Request(url_metastore_search, headers=headers))
    textResponseJSON = json.loads(response.read())
    return textResponseJSON


def getCountOfPublishedDatasets():
    return textResponseJSON['summary']['total']


def getSizeOfPublishedDatasets():
    return textResponseJSON['summary']['totalBytes']


textResponseJSON = getMetastoreDataJSON()
