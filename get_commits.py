import urllib2
import StringIO
import gzip
import datetime
import json

from word_list import word_list

d = datetime.datetime.now() - datetime.timedelta(hours=1)
url = 'http://data.githubarchive.org/%s.json.gz' % d.strftime('%Y-%m-%d-%H')

r = urllib2.urlopen(url)
compressedFile = StringIO.StringIO()
compressedFile.write(r.read())
compressedFile.seek(0)
decompressedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')

clist = [] #list of commits
for line in decompressedFile:
    jline = json.loads(line)
    if jline['public'] and 'payload' in jline.keys() and 'commits' in jline['payload'].keys():
        for c in jline['payload']['commits']:
            if any(word in c['message'] for word in word_list):
                test_list.append(jline)
                before = jline['payload']['before'][:10]
                link = 'https://github.com/' + jline['repo']['name'] + "/compare/%s...%s"
                for l in c['message'].split('\n'):
                    if any(w in l for w in word_list):
                        sha = c['sha'][:10]
                        clist.append(l + ' ' + link % (before,sha))

#randomly select commit and tweet