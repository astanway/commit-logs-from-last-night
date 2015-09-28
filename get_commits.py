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
import twython

from word_list import word_list #list of curse words to look for
from keys import keys

def get_file_url(): #calculate the file name from the current data minus one hour
    d = datetime.datetime.now() - datetime.timedelta(hours=1)
    d_string = d.strftime('%Y-%m-%d')
    #trimming leading hour off of hour because apparently this isn't something we do in Python
    hour = d.strftime('%H') if d.strftime('%H')[0] != '0' else d.strftime('%H')[1:]
    return 'http://data.githubarchive.org/%s-%s.json.gz' % (d_string,hour)

def get_file(): #kick off the file getting and unzipping
    url = get_file_url()
    r = urllib2.urlopen(url)
    compressedFile = StringIO.StringIO()
    compressedFile.write(r.read())
    compressedFile.seek(0)
    return gzip.GzipFile(fileobj=compressedFile, mode='rb')

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

decompressedFile = get_file() #get the file for the previous hour

clist = [] #list of commits with curse words and compare link ready to be tweeted

#loop to search for commit messages with curse words and append to clist
for line in decompressedFile:
    jline = json.loads(line)
    if jline['public'] and 'payload' in jline.keys() and 'commits' in jline['payload'].keys():
        for c in jline['payload']['commits']:
            if any(word in c['message'] for word in word_list):

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
                        clist.append(l + ' ' + link % (before,sha))

#randomly select commit and tweet
tweet_commit(clist[random.randint(0,len(clist)-1)])