from sys import argv
from time import time
from bs4 import BeautifulSoup
from urlparse import urlparse, parse_qs
import Queue
import requests
import json

BASE_URL = 'http://www.erji.net'

TOPIC_URL = 'http://www.erji.net/forum.php?mod=viewthread&tid=1956898&extra=page%3D1&page=1'

def extractTid(url):
    query =  urlparse(url).query
    return parse_qs(query)['tid'][0]


def getSoup(url):
    r = requests.get(url)

    # Create a soup
    soup = BeautifulSoup(r.content, 'lxml')

    return soup

def crawlThreads(url):
    threads = []

    soup = getSoup(url)

    # print soup.prettify()

    for t in soup.findAll('tbody', {'id': lambda x: x and x.startswith('normalthread_')}):
        for link in t.findAll('a', { 'class': 's xst' }):
            threads.append({
                'url': extractTid(link.attrs['href']),
                'text': link.string
            })

    return threads

def crawlTopic(url):
    soup = getSoup(url)

    # print soup.prettify()
    topicTitle = soup.find('span', { 'id': 'thread_subject' }).string
    
    print topicTitle

    for post in soup.findAll('div', { 'class': 'pct' }):
        print '=' * 10
        print post

def crawl():
    print crawlThreads('http://www.erji.net/forum.php?mod=forumdisplay&fid=2&page=1')
    # crawlTopic('http://www.erji.net/forum.php?mod=viewthread&tid=1956898&extra=page%3D1&page=1')

if __name__ == "__main__":
    crawl()
