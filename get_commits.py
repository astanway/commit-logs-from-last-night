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
# from twitter_auth import token, token_secret, consumer, consumer_secret
# from twitter import Twitter, OAuth #should this be OAuth2?


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

                    commit_dict['message'] = c['message']

                    commit_dict['avatar_url'] = jline['actor']['avatar_url'] #url to author avatar
                    commit_dict['author_username'] = jline['actor']['login'] #github user name
                    commit_dict['commit_time'] = dateutil.parser.parse(jline['created_at']) #a datatime object

                    #this is a hack so we don't have to authenticate with Github to get the user page, which should be this url
                    commit_dict['author_url'] = "https://github.com/" + jline['actor']['login'] 

                    # the url for the compare
                    commit_dict['commiturl'] = 'https://github.com/' + jline['repo']['name'] + "/commit/" + c['sha']
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
        created_at = dbauth.db.escape_string(message['commit_time'].strftime('%Y-%m-%d %H:%M:%S'))
        query = "INSERT INTO new_commits VALUES ('', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', '')" % (dbauth.db.escape_string(message['author_username']), dbauth.db.escape_string(message['message']), avatar, dbauth.db.escape_string(message['commiturl']), dbauth.db.escape_string(userurl), created_at)
        cursor.execute(query)
    except Exception as e:
        print e


def main():
    now = datetime.datetime.now()
    last_day = datetime.datetime.now() - datetime.timedelta(hours=1000)
    for d in datespan(last_day,now): #pass value instead of function to keep it from returning current hour
        try:
            url = get_file_url(d)
            r = urllib2.urlopen(url)
            compressedFile = StringIO.StringIO()
            compressedFile.write(r.read())
            compressedFile.seek(0)
            decompressedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')
            for commit in get_clist(decompressedFile):
                process(commit)
        except:
            "Error with url: " + url
            pass


if __name__ == "__main__":
    main()
