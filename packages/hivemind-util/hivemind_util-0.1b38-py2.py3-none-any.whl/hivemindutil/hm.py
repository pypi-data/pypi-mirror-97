import pkg_resources
import requests
import os
import re
import pandas as pd
import urllib.request as urlrequest
from urllib.parse import urlparse, urlencode
from .formatters import FileHandle, HivemindApiUrl


def help(searchterm=''):
    '''
    Displays the help file text.
    searchterm: search for hivemindutil method names containing the given string
    
    returns: print to stdout the help text or help text for methods with names 
        containing the searchterm.
    '''
    helpFile = pkg_resources.resource_string(__name__, 'help.txt')
    hf = helpFile.decode('utf8')

    m = re.split(r'(- \w*\([^\)]*\))', hf)
    if searchterm:
        for idx in range(1,len(m),2):
            if searchterm in m[idx].lower().split('(')[0]:
                print(''.join(m[idx:idx+2]))
    else:
        print(hf)


def info(searchterm=''):
    '''
    Wrapper function for the help function.
    searchterm: search for hivemindutil method names containing the given string
    
    returns: print to stdout the help text or help text for methods with names 
        containing the searchterm.
    '''
    help(searchterm) 


def makeAuthHeader(apiKey):
    return {'Authorization': 'ApiKey {0}'.format(apiKey)}


def removeMetadata(x):
    x.pop('_metadata', None)
    return x


def cleanBaseUrl(url):
    url = url.rstrip('/')
    if url[:4].lower() != 'http':
        url = 'https://' + url
    return url


def checkHttpResponse(r):
    if r.status_code >= 300:
        print('API request error')
        print('Url: ' + r.url)
        print('Status: ' + str(r.status_code))
        print('Reason: ' + r.reason) 
        print('Text: ' + r.text)
        print('Request body:')
        print(r.request.body)
    return r


def getResults(taskId, baseUrl, apiKey, incIncompleteInstances=False, incIterations=True): 
    if incIncompleteInstances:
        incIncompleteInstances = 'true'
    else:
        incIncompleteInstances = 'false'

    if incIterations:
        incIterations = 'true'
    else:
        incIterations = 'false'
        
    authHeader = makeAuthHeader(apiKey)
    baseUrl = cleanBaseUrl(baseUrl)
    with requests.Session() as s:
        s.headers.update(authHeader)
        
        paginatedUrl = '{0}/api/tasks/{1}/results?perPage=1000&incIncompleteInstances={2}&incIterations={3}'.format(
            baseUrl, taskId, incIncompleteInstances, incIterations)
        results = []

        while paginatedUrl is not None:            
            response = checkHttpResponse(s.get(paginatedUrl))         
            results += response.json()
            n = response.links["next"] if "next" in response.links else None
            if n is not None:
                paginatedUrl = baseUrl + n["url"]
            else:
                paginatedUrl = None
    return results    


def getInstanceResult(taskId, baseUrl, apiKey, instanceId):
    target = '{0}/api/tasks/{1}/instances/{2}/results'.format(baseUrl, taskId, instanceId)
    r = requests.get(target, headers=makeAuthHeader(apiKey))
    r.raise_for_status()
    return r.json()


def getTableExtractionResults(taskId, baseUrl, apiKey, instanceId, outputDir=None, outputFormat='csv'):
    def getFormatted(fFormat, data, outDir, outFile):
        if fFormat == 'csv':
            ret = os.path.join(outDir, outFile)
            data.to_csv(ret,
                        header=False,
                        index=False,
                        encoding='utf-8-sig')
        elif fFormat == 'dataframe':
            ret = data.copy()
        else:
            raise Exception('Unknown return format requested:')

        return ret

    if outputDir is None:
        outputDir = ''

    counter = {}
    outputName = '{filename}_{tabletype}_page{tablePage:03}_{tableNum:02}.csv'
    instanceResult = getInstanceResult(taskId, baseUrl, apiKey, instanceId)

    tables = instanceResult[0].get('data').get('Tables', [])
    dataSet = []
    for table in tables:
        tablepg = table.get('relativePageNumber')
        file = table.get('file')
        td = table.get('tableData')
        tt = table.get('metadata').get('tableType')
        tablenum = counter.get((file, tablepg), 0) + 1
        counter[(file, tablepg)] = tablenum
        outputFile = outputName.format(filename=file, tabletype=tt, tablePage=tablepg, tableNum=tablenum)
        df = pd.DataFrame(td)
        dataSet.append(getFormatted(outputFormat, df, outputDir, outputFile))
    return dataSet


def getInstances(taskId, baseUrl, apiKey, expandSummary=True): 
    authHeader = makeAuthHeader(apiKey)
    baseUrl = cleanBaseUrl(baseUrl)
    with requests.Session() as s:
        s.headers.update(authHeader)
        expandSummaryOption = '&expand=summary' if expandSummary else ''
        paginatedUrl = '{0}/api/tasks/{1}/instances?perPage=1000{2}'.format(baseUrl, taskId, expandSummaryOption)
        instances = []

        while paginatedUrl is not None:
            response = checkHttpResponse(s.get(paginatedUrl))
            instances += response.json()
            n = response.links["next"] if "next" in response.links else None
            if n is not None:
                paginatedUrl = baseUrl + n["url"]
            else:
                paginatedUrl = None
    return instances


def getInstance(taskId, baseUrl, apiKey, instanceId, expandSummary=True): 
    authHeader = makeAuthHeader(apiKey)
    baseUrl = cleanBaseUrl(baseUrl)
    with requests.Session() as s:
        s.headers.update(authHeader)
        expandSummaryOption = '?expand=summary' if expandSummary else ''
        paginatedUrl = '{0}/api/tasks/{1}/instances/{2}{3}'.format(baseUrl, taskId, instanceId, expandSummaryOption)
        response = checkHttpResponse(s.get(paginatedUrl))
            
    return response.json()     


def getInstanceIds(taskId, baseUrl, apiKey):
    instances = getInstances(taskId, baseUrl, apiKey)
    instanceIds = []
    for i in instances:
        instanceIds.append(i.get('id'))
    return instanceIds


def transferEntry(source, target, entryFields=("data", "annotations"), sourceIdField="id", targetIdField="instanceId"):
    # source and target are each an array of dictionaries.
    # For each entry in source, extract "entry" and insert it into  
    # the dictionary in target in which sourceId matches targetId.
    # By default transfers "data" from list of instance dictionaries to list of results dictionaries.
    # If entry doesn't exist in source, insert null into target
    
    # Create set of sourceId : entry pairs
    
    for entryField in entryFields:
        sourceIdEntryPairs = {}
        for s in source:
            if entryField not in s:
                continue
            entry = s.get(entryField)
            sourceId = s.get(sourceIdField)
            sourceIdEntryPairs[sourceId] = entry
        for t in target:
            targetId = t.get(targetIdField)
            t[entryField] = sourceIdEntryPairs.get(targetId)


def getInstancesAndResults(taskId, baseUrl, apiKey, expandSummary=True,
                           incIncompleteInstances=False, incIterations=True):
    # Make API calls for both instances and results, and transfer data from the former to the latter.
    instances = getInstances(taskId, baseUrl, apiKey, expandSummary)
    results = getResults(taskId, baseUrl, apiKey, incIncompleteInstances, incIterations)
    transferEntry(instances, results)
    return results


def listFilesUploaded(taskId, baseUrl, apiKey):
    # Make API call to get list of filenames uploaded to the task.
    authHeader = makeAuthHeader(apiKey)
    baseUrl = cleanBaseUrl(baseUrl)
    with requests.Session() as s:
        s.headers.update(authHeader)
        paginatedUrl = '{0}/api/tasks/{1}/files?perPage=1000'.format(baseUrl, taskId)
        result = []

        while paginatedUrl is not None:
            response = checkHttpResponse(s.get(paginatedUrl))
            result += response.json()
            n = response.links["next"] if "next" in response.links else None
            if n is not None:
                paginatedUrl = baseUrl + n["url"]
            else:
                paginatedUrl = None
        lstFilesAlreadyUploaded = map(lambda x: x.get('filename'), result)
    return list(lstFilesAlreadyUploaded)


def uploadFiles(taskId, baseUrl, apiKey, lstFilenames, localRepo, overwrite=False, raiseForStatus=True):
    if not overwrite:
        filesUploaded = listFilesUploaded(taskId, baseUrl, apiKey)
        lstFilenames = list(set(lstFilenames) - set(filesUploaded))
        
    authHeader = makeAuthHeader(apiKey)
    baseUrl = cleanBaseUrl(baseUrl)
    with requests.Session() as s:
        s.headers.update(authHeader)
        fileUrl = '{0}/api/tasks/{1}/files'.format(baseUrl, taskId)
        files = map(lambda x: os.path.join(localRepo, x), lstFilenames)

        for filename in files:
            with open(filename, 'rb') as f:
                response = s.post(fileUrl, files={'file': f})
            if raiseForStatus:
                response.raise_for_status()
            else:
                checkHttpResponse(response)


def downloadFile(filepath, localRepo, prefix='', overwrite=False):
    filename = urlparse(filepath).path.split('/')[-1]
    newFilename = '{0}_{1}'.format(prefix, filename) if prefix != '' else filename

    lstFilesDownloaded = os.listdir(localRepo)
    if overwrite or (newFilename not in lstFilesDownloaded):
        urlrequest.urlretrieve(filepath, os.path.join(localRepo, newFilename))
    return newFilename


def getIterations(taskId, baseUrl, apiKey, instanceId): 
    authHeader = makeAuthHeader(apiKey)
    baseUrl = cleanBaseUrl(baseUrl)
    with requests.Session() as s:
        s.headers.update(authHeader)        
        iterationResults = checkHttpResponse(s.get('{0}/api/tasks/{1}/instances/{2}/results'.format(baseUrl,
                                                                                                    taskId,
                                                                                                    instanceId))).json()
    return iterationResults       


def getIterationIds(taskId, baseUrl, apiKey, instanceId):
    iterationResults = getIterations(taskId, baseUrl, apiKey, instanceId)
    iterationIds = []
    for i in iterationResults:
        iterationIds.append(i.get('iterationId'))
    return iterationIds


def deleteIteration(taskId, baseUrl, apiKey, instanceId, iterationId):    
    authHeader = makeAuthHeader(apiKey)
    baseUrl = cleanBaseUrl(baseUrl)
    with requests.Session() as s:
        s.headers.update(authHeader)
        response = checkHttpResponse(s.delete('{0}/api/tasks/{1}/instances/{2}/iterations/{3}'.format(baseUrl,
                                                                                                      taskId,
                                                                                                      instanceId,
                                                                                                      iterationId)))
    return response


def deleteInstance(taskId, baseUrl, apiKey, instanceId):
    authHeader = makeAuthHeader(apiKey)
    baseUrl = cleanBaseUrl(baseUrl)
    iterationIds = getIterationIds(taskId, baseUrl, apiKey, instanceId)
    
    for iterationId in iterationIds:
        deleteIteration(taskId, baseUrl, apiKey, instanceId, iterationId)
    
    with requests.Session() as s:
        s.headers.update(authHeader)
        response = checkHttpResponse(s.delete('{0}/api/tasks/{1}/instances/{2}'.format(baseUrl, taskId, instanceId)))
    return response
   
    
def setAnnotation(taskId, baseUrl, apiKey, instanceId, key, value):
    authHeader = makeAuthHeader(apiKey)
    with requests.Session() as s:
        s.headers.update(authHeader)
        baseUrl = cleanBaseUrl(baseUrl)               
        data = {
            'key': key,
            'value': value
        }        
        response = checkHttpResponse(s.post('{0}/api/tasks/{1}/instances/{2}/annotations'.format(baseUrl, taskId,
                                                                                                 instanceId),
                                            json=data))
    return response


def addAnnotation(taskId, baseUrl, apiKey, instanceId, key, value):
    return setAnnotation(taskId, baseUrl, apiKey, instanceId, key, value)


def createInstance(taskId, baseUrl, apiKey, name, instructions='', data={}, overrideSchema=None,
                   tags=[], priority=0, annotations={}):
    # overrideSchema must either have a value or be null; cannot be {}
    if overrideSchema == {}:
        overrideSchema = None
    authHeader = makeAuthHeader(apiKey)
    with requests.Session() as s:
        s.headers.update(authHeader)
        baseUrl = cleanBaseUrl(baseUrl)               
        instance = {
            'name': name,
            'instruction': instructions,
            'data': data,
            'overrideSchema': overrideSchema,
            'tags': tags,
            'priority': priority
        }        
        response = checkHttpResponse(s.post('{0}/api/tasks/{1}/instances'.format(baseUrl, taskId), json=instance))
        instanceId = response.json()['id']
        for x in annotations:
            setAnnotation(taskId, baseUrl, apiKey, instanceId, x, annotations[x])

    return response


def reiterateInstance(taskId, baseUrl, apiKey, instanceId):
    authHeader = makeAuthHeader(apiKey)
    with requests.Session() as s:
        s.headers.update(authHeader)
        baseUrl = cleanBaseUrl(baseUrl)               
        response = checkHttpResponse(s.post('{0}/api/tasks/{1}/instances/{2}/reiterate'.format(baseUrl,
                                                                                               taskId,
                                                                                               instanceId)))
    return response
        

def deleteAnnotation(taskId, baseUrl, apiKey, instanceId, key):
    authHeader = makeAuthHeader(apiKey)
    with requests.Session() as s:
        s.headers.update(authHeader)
        baseUrl = cleanBaseUrl(baseUrl)           
        response = checkHttpResponse(s.delete('{0}/api/tasks/{1}/instances/{2}/annotations/{3}'.format(baseUrl,
                                                                                                       taskId,
                                                                                                       instanceId,
                                                                                                       key)))
    return response


def wipe(taskId, baseUrl, apiKey):
    instanceIds = getInstanceIds(taskId, baseUrl, apiKey)
    for _id in instanceIds:
        deleteInstance(taskId, baseUrl, apiKey, _id)


def getDatasetRows(datasetId, baseUrl, apiKey, queries=[]):
    authHeader = makeAuthHeader(apiKey)
    baseUrl = HivemindApiUrl(baseUrl).getChainingApiUrl()
    urlQuery = {'pageSize': 500}
    if queries:
        urlQuery['filter'] = list(queries)
    with requests.Session() as s:
        s.headers.update(authHeader)

        paginatedUrl = '{0}/api/datasets/{1}/rows/query?{2}'.format(
            baseUrl, datasetId, urlencode(urlQuery, doseq=True))
        results = []

        while paginatedUrl is not None:
            response = checkHttpResponse(s.get(paginatedUrl))
            data = response.json()
            results.extend(data.get('page'))
            n = data.get('continuationToken')
            if n is not None:
                paginatedUrl = f'{baseUrl}/api/datasets/{datasetId}/rows/query/continue?{urlencode({"token": n})}'
            else:
                paginatedUrl = None
    return results


def deleteDatasetRows(datasetId, baseUrl, apiKey, datasetRowIds=[], allRows=False, raiseForStatus=True):
    if not datasetRowIds and not allRows:
        print('No rows specified to delete.')
    authHeader = makeAuthHeader(apiKey)
    baseUrl = HivemindApiUrl(baseUrl).getChainingApiUrl()
    if allRows:
        allRows = getDatasetRows(datasetId, baseUrl, apiKey)
        datasetRowIds = [r.get('datasetRowId') for r in allRows]
    with requests.Session() as s:
        s.headers.update(authHeader)
        for datasetRowId in datasetRowIds:
            r = s.delete(f'{baseUrl}/api/datasets/{datasetId}/rows/{datasetRowId}')
            if raiseForStatus:
                r.raise_for_status()
            else:
                checkHttpResponse(r)


def getDatasetRow(datasetId, baseUrl, apiKey, datasetRowId):
    authHeader = makeAuthHeader(apiKey)
    baseUrl = HivemindApiUrl(baseUrl).getChainingApiUrl()

    response = checkHttpResponse(requests.get(f'{baseUrl}/api/datasets/{datasetId}/rows/{datasetRowId}',
                                              headers=authHeader)
                                 )
    return response.json()


def addDatasetRows(datasetId, baseUrl, apiKey, rowsData=[]):
    authHeader = makeAuthHeader(apiKey)
    baseUrl = HivemindApiUrl(baseUrl).getChainingApiUrl()
    response = None
    if rowsData:
        payload = list([{'data': rd} for rd in rowsData])
        response = checkHttpResponse(requests.post(f'{baseUrl}/api/datasets/{datasetId}/rows/bulk',
                                                   json=payload,
                                                   headers=authHeader))
    return response.json()


def addDatasetRow(datasetId, baseUrl, apiKey, rowData={}):
    authHeader = makeAuthHeader(apiKey)
    baseUrl = HivemindApiUrl(baseUrl).getChainingApiUrl()
    response = None
    if rowData:
        payload = {'data': rowData}
        response = checkHttpResponse(requests.post(f'{baseUrl}/api/datasets/{datasetId}/rows',
                                                  json=payload,
                                                  headers=authHeader)
                                     )
    return response.json()


def listFileStore(baseUrl, apiKey, remotePath='', recursive=False):
    endpoint = '/api/files/list'
    baseUrl = HivemindApiUrl(baseUrl).getFilesApiUrl()

    if recursive:
        endpoint = endpoint + '/recursive'

    if remotePath:
        searchQuery = f"?{urlencode({'directory': '!dir({})'.format(remotePath.replace('(', '((').replace(')','))'))})}"
    else:
        searchQuery = ''
    resp = checkHttpResponse(requests.get(f'{baseUrl}{endpoint}{searchQuery}',
                                          headers=makeAuthHeader(apiKey)))
    resp.raise_for_status()
    filesList = resp.json()
    return filesList


def uploadToFileStore(baseUrl, apiKey, fileName, localRepo, remotePath, overwrite=False, raiseForStatus=True):
    baseUrl = HivemindApiUrl(baseUrl).getFilesApiUrl()
    fullRemotePath = f'{remotePath}/{fileName}' if remotePath else fileName
    handle = FileHandle(fullRemotePath)
    if not overwrite:
        files = listFileStore(baseUrl, apiKey, remotePath)
        if str(handle) in files:
            return str(handle)
    response = checkHttpResponse(requests.put(f'{baseUrl}/api/files?{urlencode({"fileHandle": str(handle)})}',
                                              headers=makeAuthHeader(apiKey),
                                              files={'file': open(os.path.join(localRepo, fileName), 'rb')}
                                              )
                                 )
    if raiseForStatus:
        response.raise_for_status()

    try:
        response = response.json()
    except Exception as e:
        response = None

    return response


def deleteFromFileStore(baseUrl, apiKey, fileHandle, raiseForStatus=True):
    baseUrl = HivemindApiUrl(baseUrl).getFilesApiUrl()
    fh = FileHandle.parse(fileHandle)
    resp = checkHttpResponse(requests.delete(f'{baseUrl}/api/files?{urlencode({"fileHandle": str(fh)})}',
                                             headers=makeAuthHeader(apiKey)))
    if raiseForStatus:
        resp.raise_for_status()
