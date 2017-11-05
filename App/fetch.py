import urllib2

def load(url):
    response = urllib2.urlopen(url)
    return response.read()