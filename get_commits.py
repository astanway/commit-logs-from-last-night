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
# import twython #will probably need to install
import sys
import dateutil
import collections
import dateutil.parser

# from original scrape.py
import MySQLdb
import dbauth
from twitter_auth import token, token_secret, consumer, consumer_secret
from twitter import Twitter, OAuth #should this be OAuth2?


from word_list import word_list #list of curse words to look for


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
    '''
    A function to take the input file, search for commits with words in the word list, and create 
    a dictionary of the information for those commits.
    'avatar_url' -> the url for the author's avatar
    'author_username' -> the author username
    'commit_time' -> the time of the commit 
    'author_url' -> the url for the author's Github page
    'message' -> the line in the commit message with the curse word
    'link' -> the link for the compare and the commit message
    '''
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

def process(message):
    '''
    A function to commit the selected message to the database. The message is a dictionary of the randomly selected commit.
    This loads the commit into the database
    '''
    try:
        cursor = dbauth.db.cursor()
        userurl = message['author_url']
        avatar = message['avatar_url']
        created_at = dbauth.db.escape_string(message['created_at'].strftime('%Y-%m-%d %H:%M:%S'))
        query = "INSERT INTO new_commits VALUES ('', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', '')" % (message['author_username'], dbauth.db.escape_string(message['message']), avatar, dbauth.db.escape_string(message['message']), dbauth.db.escape_string(userurl), created_at)
        cursor.execute(query)
        tweet_commit(message['message'],message['link'])
    except Exception as e:
        print e
        continue


def tweet_commit(message, link): # a sketch of the tweet function that should be tested with real keys
    t = Twitter(
        auth=OAuth(token, token_secret, consumer, consumer_secret))
    try:
        t.statuses.update(status= message + ' ' + link) 
    except:
        pass


def main():
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

if __name__ == "__main__":
    main()