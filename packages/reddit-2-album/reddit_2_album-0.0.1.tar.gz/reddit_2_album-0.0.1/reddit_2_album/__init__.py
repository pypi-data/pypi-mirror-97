#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'reddit_2_album'

from telegram_util import AlbumResult as Result
import yaml
import os
import praw

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

def get(path):
    try:
        reddit_id = path.split('/')[6] # may need to revisit
    except:
        reddit_id = path
    submission = reddit.submission(reddit_id)
    print(submission.url)
    result = Result()
    if submission.url != submission.permalink:
        result.imgs = [submission.url]
    result.cap_html = '[ %s ]' % submission.title
    if submission.selftext:
        result.cap_html += '\n\n%s' % submission.selftext
    result.cap_html += ' <a href="https://www.reddit.com%s">source</a>' % submission.permalink
    return result