#dominate allows for cleaner html creation within python
import dominate
from dominate.tags import *
#ezgmail is a wrapper for the Google gmail API that facilitates our requests
import ezgmail
#datetime used to determine current day and yesterday
from datetime import datetime, timedelta
#tzlocal used to get local time to ensure that 'yesterday' is determined correctly
from tzlocal import get_localzone
import re
import os.path

#choose search parameters for the email collection you would like to compile (examples below)
#suggested parameter 'newer_than:1d' to collect previous day's emails
#suggested parameter 'to:YOUR_EMAIL' keeps sent mail from being added'
#any parameters besides 'newer_than', 'to', and 'is' are added with OR operator and are non-exclusive
params = ['from:account@gmail.com','from:otheraccount@university.edu','subject:school','list:info@example.com','is:unread','newer_than:1d','to:tstscrptemail@gmail.com']

#choose the directory where you want the html file and any downloaded attachments to be saved
directory = '/Users/william/Desktop/EmailProject'


def get_yesterday():
    local_time = get_localzone()
    now_utc = datetime.now(local_time)
    yesterday = now_utc - timedelta(1)
    yester_date = yesterday.strftime('%A, %B %-d')
    return yester_date

def get_emails():
  query = ''
  for item in params:
    if item[:2] == 'to' or item[:2] == 'ne' or item[:2] == 'is':
      query+= item + ' '
    else: query += 'OR ' + item + ' '
  yesterday_mail = ezgmail.search(query,maxResults=25)
  return yesterday_mail

def start_page():
  global webpage
  webpage = dominate.document(title='Daily Email report')
  
 #Optionally add link to external css for styling. Template style.css included in styling folder for download.
  with webpage.head:
    link(rel='stylesheet', href='style.css')
    #Save style.css in the same local directory that you assign to 'directory variable.
      
  with webpage:
    h = h1("Message Digest for %s"%yester_date)
    h["style"] = 'color:red;font-size:25px;'
  
    
#Writes the html for a single email preview  
def make_preview(message):
  global webpage
  main_text = message.body
  
  link = re.compile('https\S*>') 
  link_name = re.compile('(\S*?//)(\S*?)(/\S*)')
  line_breaks = re.compile('\\r\\n') 
  
  link_list = link.findall(main_text)
  main_preview = main_text[:1000] 
  subbed_preview = line_breaks.sub('#BR#', main_preview)
  
  #Creates the main information fields and text for a single email
  sender = message.sender
  subject = message.subject
  time = message.timestamp.strftime('%H:%M:%S %a %y-%m-%d')
  webpage += p(sender + ' at ' + time, cls = 'sender', style='color:green;font-size:15px')
  webpage += p(subject, cls = 'subject', style='color:blue;font-size:15px')
  webpage += p('Message preview:' , cls = 'preview', style ='color:black;font-size:12px;')
  webpage += div(subbed_preview + '...',cls = 'maintext', style ='color:black;font-size:15px;')
  
  #creates links section if there are links to display
  if(not len(link_list)==0):
      links_section = div(p('Message links:#BR#'), cls = 'links', style='color:#ff9900;font-size:12px;')
      with links_section:
        for link in link_list:
            lname = re.sub(link_name, r'\2',link)
            newlink = span('— — — —  ', a(lname, href = link[:-1]),'  — — — —')
      webpage+= links_section
      webpage+='#BR#'
  attachments = message.attachments
  
  #creates attachments section if there are any attachments to display
  if(not len(attachments) == 0):
    message.downloadAllAttachments(downloadFolder = directory, overwrite = True)
    attachments_section = div(p('Attachments:#BR#'),cls = 'attachments', style='color:#ff9900;font-size:12px;')
    with attachments_section:
      for att in attachments:
        newatt = span('  ————  ', a(att, href = directory + '/' + att),'  ————  ')
    webpage+= attachments_section
    webpage+='#BR#'
    
def main():
    global yester_date
    
    #Gets the appropriate day, collects emails that fit user parameters, and creates initial html text
    yester_date = get_yesterday()
    emails = get_emails()
    start_page()
    
    #adds preview section for every email returned by get_emails()
    for item in emails:
        make_preview(item.messages[0])
    
    #filters the completed html text to reinsert line breaks where placeholder #BR# was inserted
    rebreaks = re.compile('#BR#') 
    webpage_final = rebreaks.sub('<br>', webpage.render())
    
    
    #names and writes the html file and saves it to the specified directory. 
    #If specified directory does not exist then it is created
    filename = '%s.html' %yester_date
    file_path = os.path.join(directory, filename)
    if not os.path.isdir(directory):
        os.mkdir(directory)
    file = open(file_path, 'w')
    file.write(webpage_final)
    file.close()
    
    #prompts user to choose whether or not to mark compiled emails as read
    mark_as_read = ''
    while(not (mark_as_read == 'y' or mark_as_read == 'n')):
        mark_as_read = input('Would you like to mark compiled emails as read? \'y\' to mark read or \'n\' to leave unread: ')
        if mark_as_read == 'y':
            ezgmail.markAsRead(emails)
           
    
if __name__ == "__main__":
    main()