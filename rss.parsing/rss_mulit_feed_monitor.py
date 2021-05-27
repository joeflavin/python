#!/usr/bin/python3
import sys
from os import path
import feedparser
import smtplib
from email.message import EmailMessage
import datetime
import json

# Set save file filename
filename = '.rss_multi_feed_data.json'
# List of RSS feed URLs
urls = ['https://www.example.com/category/feed/',
        'https://www.example.com/category/another/feed/',
        'https://www.example.com/category/yet/another/feed/']
# List of target strings
targets = ['list', 'of', 'target strings']
# Set gmail credentials
gmail_user = 'yourname@gmail.com'
gmail_password = 'app_speficic_gmail_password'


def send_email(body, subject):
    """ Sends an email using gmail credentials

        body is the message, a string; sub is the subject line, a string
    """

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
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
        with open(filename, 'r') as f:
            last_feed = json.load(f)
    else:
        last_feed = ''

    # Now check the feed for new data
    now = datetime.datetime.now()
    print(now, "Checking Feed")

    try:
        feeds = [feedparser.parse(url)['entries'] for url in urls]
        items = []
        for feed in feeds:
            feed_items = [ [entry['title'], entry['links'][0]['href']] for entry in feed ]
            items.extend(feed_items)

    except Exception as e:
        sys.exit(e)

    if items == last_feed:
        print("No updates")
    else:
        hit = ""
        for item in items:
            for target in targets:
                if target in item[0]:
                    hit += " ".join(x for x in item)
                    hit += "\n"

        if hit != "":
            send_email(hit, 'Multi RSS Parser Hit')
        else:
            print("No hits this time.")

        # Now save the data for next time
        with open(filename, 'w') as f:
            json.dump(items, f)


if __name__ == "__main__":
    main()
