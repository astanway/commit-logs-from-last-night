'''
A script to get the commit logs from Github archive and parse for curse words to tweet.
The script is intended to run every hour in a cron job, downloading the processing the previous
hours archive for a commit log with a curse word and tweeting one of them at random.
'''

import urllib2
import StringIO
import gzip
import datetime
import json
import random
import twython #will probably need to install
import sys
import dateutil
import collections
# import requests
import dateutil.parser

from word_list import word_list #list of curse words to look for
from keys import keys

#Based on http://stackoverflow.com/questions/153584/how-to-iterate-over-a-timespan-after-days-hours-weeks-and-months-in-python
def datespan(startDate, endDate, delta=datetime.timedelta(hours=1)):
    currentDate = startDate
    while currentDate < endDate:
        yield currentDate
        currentDate += delta

def get_file_url(d): #return file name based on passed in datetime object
    d_string = d.strftime('%Y-%m-%d')
    #trimming leading hour off of hour because apparently this isn't something we do in Python
    hour = d.strftime('%H') if d.strftime('%H')[0] != '0' else d.strftime('%H')[1:]
    return 'http://data.githubarchive.org/%s-%s.json.gz' % (d_string,hour)

#a function to take in the decompressed file and output a list of matching commits formatted to tweet
def get_clist(input_file): 
    #loop to search for commit messages with curse words and append to clist
    clist = []
    for line in input_file:
        jline = json.loads(line)
        if jline['public'] and 'payload' in jline.keys() and 'commits' in jline['payload'].keys():
            for c in jline['payload']['commits']:
                if any(word in c['message'] for word in word_list):
                    commit_dict = collections.defaultdict(str)

                    commit_dict['avatar_url'] = jline['actor']['avatar_url'] #url to author avatar
                    commit_dict['author_username'] = jline['actor']['login'] #github user name
                    commit_dict['commit_time'] = dateutil.parser.parse(jline['created_at']) #a datatime object

                    #this is a hack so we don't have to authenticate with Github to get the user page, which should be this url
                    commit_dict['author_url'] = "https://github.com/" + jline['actor']['login'] 
                    
                    # the url for the compare
                    link = 'https://github.com/' + jline['repo']['name'] + "/compare/%s...%s"
                    
                    #the shortened hash for previous commit to the cursed one
                    before = jline['payload']['before'][:10] 
                    
                    #search for the line in the commit message with the curse word
                    for l in c['message'].split('\n'):
                        #limit length of commit message (prefer short and saucy)
                        if len(l) <= 50 and any(w in l for w in word_list):

                            #the shortened hash for the current cursed commit
                            sha = c['sha'][:10] 
                            commit_dict['message'] = l
                            commit_dict['link'] = link % (before,sha)

                            clist.append(commit_dict)
    return clist

def tweet_commit(tweet): #a placeholder for the full tweet until tested
    print tweet

    # #####authenticate the Twitter account
    # CONSUMER_KEY = keys['consumer_key']
    # CONSUMER_SECRET = keys['consumer_secret']
    # ACCESS_TOKEN = keys['access_token']
    # ACCESS_TOKEN_SECRET = keys['access_token_secret']
    # twitter = twython.Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
    # #######
    
    # try:
    #     twitter.update_status(status=tweet)
    # except:
    #     pass

    # return

commit_list = []
now = datetime.datetime.now()
last_day = datetime.datetime.now() - datetime.timedelta(hours=24)
for d in datespan(last_day,now): #pass value instead of function to keep it from returning current hour
    try:
        url = get_file_url(d)
        r = urllib2.urlopen(url)
        compressedFile = StringIO.StringIO()
        compressedFile.write(r.read())
        compressedFile.seek(0)
        decompressedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')
        commit_list += get_clist(decompressedFile)
    except:
        "Error with url: " + url
        pass

#randomly select commit and tweet
tweet_commit(commit_list[random.randint(0,len(commit_list)-1)])