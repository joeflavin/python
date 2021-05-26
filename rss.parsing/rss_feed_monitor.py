#!/usr/bin/python3
import sys
from os import path
import feedparser
import smtplib
from email.message import EmailMessage
from time import sleep
import datetime
import json


filename = '.rss_feed_data.json'
url = 'https://www.example.com/category/feed/'
targets = ['list', 'of', 'target strings']


def send_email(arg, sub):

    gmail_user = 'yourname@gmail.com'
    gmail_password = 'app_speficic_gmail_password'

    msg = EmailMessage()
    msg.set_content(arg)
    msg['Subject'] = sub
    msg['From'] = 'Does This Work?'
    msg['To'] = 'yourname@gmail.com'

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(gmail_user, gmail_password)
        server.send_message(msg)
        server.quit()
        print('Email sent!')
    except Exception as e:
        print(e)
        print('Something went wrong...')


def main():
    # First load the previous data if it exists
    if path.isfile(filename):
        with open(filename, 'rb') as f:
            last_feed = json.load(f)
    else:
        last_feed = ''

    # Now check the feed for new data
    now = datetime.datetime.now()
    print(now, "Checking Feed")

    try:
        feed = feedparser.parse(url)
        entries = feed['entries']
        items = [ (entry['title'], entry['links'][0]['href']) for entry in entries ]
    except Exception as e:
        sys.exit(e)


    if items == last_feed:
        print("No updates")
    else:
        hit = ""
        for item in items:
            for target in targets:
                if target in item[0]:
                    hit += " ".join( x for x in item)
                    hit += "\n"

        if hit != "":
            send_email(hit, 'RSS Parser Hit')
        else:
            print("No hits this time.")

        # Now save the data for next time
        with open(filename, 'wb') as f:
            json.dump(items, f)


if __name__ == "__main__":
    main()
