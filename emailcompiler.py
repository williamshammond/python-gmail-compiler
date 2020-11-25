#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 19:51:02 2020

@author: william
"""

import dominate
from dominate.tags import *
import ezgmail
from datetime import datetime, timedelta
from tzlocal import get_localzone
import re
import os.path

params = ['from:googlecommunityteam-noreply@google.com','from:no-reply@accounts.google.com','from:wsh2117@columbia.edu','newer_than:2d','to:tstscrptemail@gmail.com']
directory = '/Users/william/Desktop/EmailProject'
yesterdate = ""

def get_yesterday():
    local_time = get_localzone()
    now_utc = datetime.now(local_time)
    yesterday = now_utc - timedelta(1)
    yester_date = yesterday.strftime('%A, %B %-d')
    return yester_date

def get_emails():
  query = ''
  for item in params:
    if item[:2] == 'to' or item[:2] == 'ne':
      query+= item + ' '
    else: query += 'OR ' + item + ' '
  yesterday_mail = ezgmail.search(query,maxResults=25)
  return yesterday_mail

def start_page():
  global yester_date
  global webpage
  webpage = dominate.document(title='Daily Email report')
  with webpage.head:
    style('{color:red;font-size:25px;}')

  with webpage:
    h = h1('Message Digest for %s'%yester_date)
    h['style'] = 'color:red;font-size:25px;'
    
    
def make_preview(message):
  global webpage

  link = re.compile('https\S*>') 
  maintext = message.body

  linklist = link.findall(maintext)
  mainpreview = maintext[:1000]
  breaks = re.compile('\\r\\n') 
  subbedpreview = breaks.sub('#BR#', mainpreview)

  sender = message.sender
  subject = message.subject
  time = message.timestamp.strftime('%H:%M:%S %a %y-%m-%d')
  webpage += p(sender + ' at ' + time, style='color:green;font-size:15px')
  webpage += p(subject, style='color:blue;font-size:15px')
  webpage += p('Message preview:' + subbedpreview + '...', style ='color:black;font-size:12px;')
  links_section = div('Message links:#BR#',style='color:#ff9900;font-size:12px;')
  with links_section:
    for link in linklist:
      newlink = span('  ————  ', a(link[:-1], href = link[:-1]),'  ————  ')
  webpage+= links_section
  webpage+='#BR#'
  attachments = message.attachments
  if(not len(attachments) == 0):
    message.downloadAllAttachments(downloadFolder = directory, overwrite = True)
    attachments_section = div('Attachments:#BR#',style='color:#ff9900;font-size:12px;')
    with attachments_section:
      for att in attachments:
        newatt = span('  ————  ', a(att, href = directory + '/' + att),'  ————  ')
    webpage+= attachments_section
    webpage+='#BR#'
    
def main():
    global yester_date
    yester_date = get_yesterday()
    emails = get_emails()
    start_page()
    for item in emails:
        make_preview(item.messages[0])
    rebreaks = re.compile('#BR#') 
    webpage_final = rebreaks.sub('<br>', webpage.render())
    filename = 'test5.html'
    file_path = os.path.join(directory, filename)
    if not os.path.isdir(directory):
        os.mkdir(directory)
    file = open(file_path, 'w')
    file.write(webpage_final)
    file.close()
    mark_as_read = input('Would you like to mark compiled emails as read? \'y\' to mark read')
    if mark_as_read == 'y':
        ezgmail.markAsRead(emails)
    
    
    
if __name__ == "__main__":
    main()