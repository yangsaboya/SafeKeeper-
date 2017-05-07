# -*- coding: utf-8 -*-

from __future__ import print_function
import httplib2
import os, logging

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

logging.basicConfig(filename = 'logger.log', level = logging.INFO)

try:
    import argparse
    flags = argparse.ArgumentParser(parents = [tools.argparser]).parse_args()
except ImportError:
    flags = None

# Authorization Workflow

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

## Get path for saving credentials
def getCredentialPath():
    ''' Generate path for credential'''

    home_dir = os.path.abspath(os.curdir)
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.mkdir(credential_dir)
    credential_path = os.path.join(credential_dir, 'calendar-python.json')
    logging.info('credential_path = {}'.format(credential_path))
    return credential_path

## Get Authorization
def getCredentials():
    ''' Get credentials'''
    store = Storage(getCredentialPath())
    credentials = store.get()
    logging.info('Getting credential ...')
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            credentials = tools.run(flow, store)
    logging.info('Get credential done!')
    return credentials

## Insert a new Calendar Item
def insertNewItem():
    now = datetime.datetime.now()
    startTime = datetime.datetime(now.year, now.month, now.day, 
            min(now.hour + 10, 23), 0, 0, 0)
    endTime = datetime.datetime(now.year, now.month, now.day,
            startTime.hour, 0, 30, 0)

    logging.info('\t now, {}'.format(now))
    logging.info('\t start, {}'.format(startTime))
    logging.info('\t end, {}'.format(endTime))

    credentials = getCredentials()
    logging.info('[INSERT ITEM], GET CREDENTIALS DONE.')
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http = http)
    logging.info('[INSERT ITEM], GET SERVICE DONE')

    tarevent = {
        'summary': 'EXPETED BACK HOME TIME',
        'location': 'No.5 Yiheyuan Road, Peking University',
        'description': 'Expected time for back home',
        'start': {
            'dateTime': startTime.strftime('%Y-%m-%dT%H:%M:%S-07:00'),
            'timeZone': 'Asia/Shanghai',
        },
        'end': {
            'dateTime': startTime.strftime('%Y-%m-%dT%H:%M:%S-07:00'),
            'timeZone': 'Asia/Shanghai',
        },
    }
    event = service.events().insert(calendarId = 'primary', body = tarevent).execute()
    logging.info('[INSERT ITEM] INSERT EVENT DONE!')
    logging.info('[INSERT ITEM] EVENT ID = {}'.format(event['id']))
    return event['id']

def deleteItem(eventId):
    credentials = getCredentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http = http)

    try:
        event = service.events().get(calendarId = 'primary', eventId = eventId).execute()
    except:
        logging.error('[DELETE ITEM] ERROR IN FINDING EVENT')
    finally:
        if not event is None:
            service.events().delete(calendarId = 'primary', eventId = eventId).execute()
            logging.info('[DELETE ITEM] DELETE ITEM DONE!')

# if __name__ == '__main__':
  #   deleteItem(insertNewItem())
