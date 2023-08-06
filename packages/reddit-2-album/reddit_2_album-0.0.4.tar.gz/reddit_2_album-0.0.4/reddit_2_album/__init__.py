#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'reddit_2_album'

from telegram_util import AlbumResult as Result
import yaml
import os
import praw
import cached_url
from bs4 import BeautifulSoup

def getCredential():
    for root, _, files in os.walk("."):
        for file in files:
            if 'credential' in file.lower():
                try:
                    with open(os.path.join(root, file)) as f:  
                        credential = yaml.load(f, Loader=yaml.FullLoader)
                        credential['reddit_client_id']
                        return credential
                except:
                    ...

credential = getCredential()

reddit = praw.Reddit(
    client_id=credential['reddit_client_id'],
    client_secret=credential['reddit_client_secret'],
    password=credential['reddit_password'],
    user_agent="testscript",
    username=credential['reddit_username'],
)

def getGallery(url):
    content = cached_url.get(url, force_cache=True)
    soup = BeautifulSoup(content, 'html.parser')
    for item in soup.find_all('a'):
        if item.parent.name != 'figure':
            continue
        yield item['href'] 

def getImgs(submission):
    if submission.url == submission.permalink:
        return []
    if 'gallery' not in submission.url.split('/'):
        return [submission.url]
    return list(getGallery(submission.url))

def get(path):
    try:
        reddit_id = path.split('/')[6] # may need to revisit
    except:
        reddit_id = path
    submission = reddit.submission(reddit_id)
    result = Result()
    result.imgs = getImgs(submission)
    result.cap = submission.title
    if submission.selftext:
        result.cap += '\n\n%s' % submission.selftext
    result.url = path
    return result