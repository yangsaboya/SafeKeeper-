# -*- coding: utf-8 -*-

import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

import calendarHelper as cal

app = Flask(__name__)
ask = Ask(app, '/')

eventId = None

@ask.launch
def launched():
    msg = render_template('welcome')
    return question(msg)

@ask.intent('LeaveIntent')
def onLeave():
    msg = render_template('ask_leave')
    eventId = cal.insertNewItem()
    logging.info('\t [NEW ITEM] eventId = {}'.format(eventId))
    return statement(msg)

@ask.intent('BackIntent')
def onBack():
    msg = render_template('ask_back')
    if not eventId is None:
        cal.deleteItem(eventId)
        logging.info('\t [DELETE ITEM] DELETE DONE!')
        eventId = None
    return statement(msg)

@ask.intent('EmergencyIntent')
def onEmergency():
    msg = render_template('ask_emergency')
    return statement(msg)

if __name__ == '__main__':
    app.run(debug = True)
