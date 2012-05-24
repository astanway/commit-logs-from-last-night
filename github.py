from bs4 import BeautifulSoup
import requests
import simplejson

def find_avatar(username):
  r = requests.get('https://github.com/' + username)
  soup = BeautifulSoup(r.text)
  for img in soup.find_all("img"):
    try:
      if img.get('src').index('gravatar') > 0:
        return img.get('src')
    except:
      continue

print find_avatar('astanway')