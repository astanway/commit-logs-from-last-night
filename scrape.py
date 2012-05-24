import httplib2
import pprint
import sys
from BeautifulSoup import BeautifulSoup
import requests
import simplejson

from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

def find_avatar(username):
  r = requests.get('https://github.com/' + username)
  soup = BeautifulSoup(r.text)
  for img in soup.find_all("img"):
    try:
      if img.get('src').index('gravatar') > 0:
        return img.get('src')
    except:
      continue

def printTableData(data, startIndex):
  for row in data['rows']:
    rowVal = []
    for cell in row['f']:
        rowVal.append(cell['v'])
    avatar = find_avatar(row['f'][3]['v'])
    print avatar
    print 'Row %d: %s' % (startIndex, rowVal)
    startIndex +=1


def main(argv):
  f = file('key.p12', 'rb')
  key = f.read()
  f.close()

  credentials = SignedJwtAssertionCredentials(
      '789819888058@developer.gserviceaccount.com',
      key,
      scope='https://www.googleapis.com/auth/bigquery')
  http = httplib2.Http()
  http = credentials.authorize(http)

  service = build("bigquery", "v2", http=http)
  
  projectId = "789819888058"
  datasetId = "github"
  
  def runSyncQuery (service, projectId, datasetId, timeout=0):
    jobCollection = service.jobs()
    queryData = {'query':
    """SELECT created_at, url, payload_commit_msg, actor FROM [githubarchive:github.timeline] 
    WHERE 
    (LOWER(payload_commit_msg) CONTAINS "fuck") OR  
    (LOWER(payload_commit_msg) CONTAINS "bitch") OR
    (LOWER(payload_commit_msg) CONTAINS "shit") OR
    (LOWER(payload_commit_msg) CONTAINS " tits") OR
    (LOWER(payload_commit_msg) CONTAINS "asshole") OR
    (LOWER(payload_commit_msg) CONTAINS "dick") OR
    (LOWER(payload_commit_msg) CONTAINS "cocksucker") OR
    (LOWER(payload_commit_msg) CONTAINS "cunt") OR
    (LOWER(payload_commit_msg) CONTAINS " hell ") OR
    (LOWER(payload_commit_msg) CONTAINS "douche") OR
    (LOWER(payload_commit_msg) CONTAINS "testicle") OR
    (LOWER(payload_commit_msg) CONTAINS "twat") OR
    (LOWER(payload_commit_msg) CONTAINS "bastard") OR
    (LOWER(payload_commit_msg) CONTAINS "faggot") OR
    (LOWER(payload_commit_msg) CONTAINS "nigger") OR
    (LOWER(payload_commit_msg) CONTAINS "sperm") OR
    (LOWER(payload_commit_msg) CONTAINS "shit") OR
    (LOWER(payload_commit_msg) CONTAINS "dildo") OR
    (LOWER(payload_commit_msg) CONTAINS "wanker") OR
    (LOWER(payload_commit_msg) CONTAINS "prick") OR
    (LOWER(payload_commit_msg) CONTAINS "penis") OR
    (LOWER(payload_commit_msg) CONTAINS "vagina") OR
    (LOWER(payload_commit_msg) CONTAINS "whore")
    ORDER BY created_at DESC LIMIT 500;""",
                 'timeoutMs':timeout}

    queryReply = jobCollection.query(projectId=projectId,
                                     body=queryData).execute()

    jobReference=queryReply['jobReference']

    # Timeout exceeded: keep polling until the job is complete.
    while(not queryReply['jobComplete']):
      print 'Job not yet complete...'
      queryReply = jobCollection.getQueryResults(
                          projectId=jobReference['projectId'],
                          jobId=jobReference['jobId'],
                          timeoutMs=timeout).execute()

    # If the result has rows, print the rows in the reply.
    if('rows' in queryReply):
      print 'has a rows attribute'
      printTableData(queryReply, 0)
      currentRow = len(queryReply['rows'])

      # Loop through each page of data
      while('rows' in queryReply and currentRow < queryReply['totalRows']):
        queryReply = jobCollection.getQueryResults(
                          projectId=jobReference['projectId'],
                          jobId=jobReference['jobId'],
                          startIndex=currentRow).execute()
        if('rows' in queryReply):
          printTableData(queryReply, currentRow)
          currentRow += len(queryReply['rows'])

  runSyncQuery (service, projectId, datasetId)
    
if __name__ == '__main__':
  main(sys.argv)