import httplib2
import pprint
import sys
import urllib2
import simplejson
import MySQLdb
import dbauth
import random
import requests
from time import sleep
from bs4 import BeautifulSoup
from twitter_auth import token, token_secret, consumer, consumer_secret
from twitter import Twitter, OAuth
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

cursor = dbauth.db.cursor()
t = Twitter(
    auth=OAuth(token, token_secret, consumer, consumer_secret))

def insult(name):
  person = '@' + name
  i = ['Watch your mouth, ' + person, 
       person + ' , I love it when you talk dirty', 
       'Very disappointed with your language, ' + person, 
       'Yo,' + person + ' , quit cursing in your code!',
       person + ', you should be ashamed for using this kind of language.',
       person + ', you kiss your mother with that mouth?',
       person.upper() + ' CURSES IN HIS !@*^ING CODE',
       person + ', act professional and quit using bad words. Fucker.',
       'Impressive vocabulary, ' + person,
       person + ', fucking cursing in your code and shit.',
       'Hope your manager doesn\'t see this, ' + person + '!'
       ]

  return random.choice(i)

def find_avatar(username):
  r = urllib2.urlopen('https://github.com/' + username)
  body = r.read()
  soup = BeautifulSoup(body)
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
    #Some random fucking german dude whose shit always shows up.
    if row['f'][3]['v'] == 'yayachiken' or row['f'][3]['v'] == 'harshitagg':
        continue
    avatar = find_avatar(row['f'][3]['v'])
    userurl = "https://github.com/" + row['f'][3]['v']
    query = "INSERT INTO new_commits VALUES ('', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', '')" % (row['f'][3]['v'], dbauth.db.escape_string(row['f'][2]['v']), avatar, row['f'][1]['v'], userurl, row['f'][0]['v'])
    try:
      cursor.execute(query)
      if startIndex % 35 == 0:
        """Sleep a random amount of time to avoid spam tag and tweet"""
        tweet = insult(row['f'][3]['v']) + " " + row['f'][1]['v']
        url = "http://api.twitter.com/1/users/show.xml?screen_name=" + row['f'][3]['v']
        r = requests.get(url)
        print r.status_code
        if r.status_code == 200:
            print "Tweeting"
            t.statuses.update(status=tweet)
            sleep(random.randrange(20, 60, 1))
    except MySQLdb.Error, e:
      print str(e)
      pass
    startIndex +=1


def main(argv):
  f = file('/home/abasababa/key.p12', 'rb')
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
    (LOWER(payload_commit_msg) CONTAINS "dildo") OR
    (LOWER(payload_commit_msg) CONTAINS "wanker") OR
    (LOWER(payload_commit_msg) CONTAINS "prick") OR
    (LOWER(payload_commit_msg) CONTAINS "penis") OR
    (LOWER(payload_commit_msg) CONTAINS "vagina") OR
    (LOWER(payload_commit_msg) CONTAINS "whore")
    ORDER BY created_at DESC LIMIT 700;""",
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
