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
import subprocess
import json
import dateutil.parser

cursor = dbauth.db.cursor()
t = Twitter(
    auth=OAuth(token, token_secret, consumer, consumer_secret))

output = json.loads(subprocess.Popen(["ruby", "get_commits.rb"], stdout=subprocess.PIPE).communicate()[0])

def insult(name):
  person = '@' + name
  i = ['Watch your mouth, ' + person, 
       person + ', I love it when you talk dirty', 
       'Very disappointed with your language, ' + person, 
       'Yo,' + person + ', quit cursing in your code!',
       person + ', you should be ashamed for using this kind of language.',
       person + ', you kiss your mother with that mouth?',
       person.upper() + ' CURSES IN HIS !@*^ING CODE',
       person + ', act professional and quit using bad words. Fucker.',
       'Impressive vocabulary, ' + person,
       person + ', fucking cursing in your code and shit.',
       'Hope your manager doesn\'t see this, ' + person + '!'
       ]

  return random.choice(i)

def find_avatar(userurl):
  r = urllib2.urlopen(userurl)
  body = r.read()
  soup = BeautifulSoup(body)
  for img in soup.find_all("img"):
    print img
    try:
      if img.get('src').index('avatar') > 0:
        return img.get('src')
    except:
      continue


def process(output):
  for row in output:
    try:
        userurl = "https://" + row['userurl']
        avatar = find_avatar(userurl)
        created_at = dateutil.parser.parse(row['created_at']).strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT INTO new_commits VALUES ('', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', '')" % (row['commiter'], dbauth.db.escape_string(row['message']), avatar, row['commiturl'], userurl, created_at)
        cursor.execute(query)
    except Exception as e:
        print e
        continue

process(output)
