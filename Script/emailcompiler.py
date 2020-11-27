#dominate allows for cleaner html creation within python
import dominate
from dominate.tags import *
#ezgmail is a wrapper for the Google gmail API that facilitates our requests
import ezgmail
#datetime used to determine current day and yesterday
from datetime import datetime, timedelta
#tzlocal used to get local time to ensure that 'yesterday' is determined correctly
from tzlocal import get_localzone
#regex expressions for locating and modifying portions text
import re
#Used to modify directory pathnames
import os.path
#For opening the generated html file in default browser
import webbrowser

#choose search parameters for the email collection you would like to compile (examples below)
#suggested parameter 'newer_than:1d' to collect previous day's emails
#suggested parameter 'to:YOUR_EMAIL' keeps sent mail from being added'
#any parameters besides 'newer_than', 'to', and 'is' are added with OR operator and are non-exclusive
params = ['from:account@gmail.com','from:otheraccount@university.edu','subject:school','list:info@example.com','is:unread','newer_than:1d','to:#INSERT_EMAIL@gmail.com']

#choose the directory where you want the html file and any downloaded attachments to be saved
directory = 'INSERT_DIRECTORY'

#returns a formatted string representing the date 24 hours before the script was executed
def get_yesterday():
    local_time = get_localzone()
    now_utc = datetime.now(local_time)
    yesterday = now_utc - timedelta(1)
    yester_date = yesterday.strftime('%A, %B %-d')
    return yester_date

#returns a list of ezgmail GmailThread Objects
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
    link(rel='stylesheet',href= directory + '/style.css')
    #Save style.css in the same local directory that you assign to 'directory variable.
      
  with webpage:
    h = h1("Message Digest for %s"%yester_date)
    h["style"] = 'color:red;font-size:25px;'
  
    
#Writes the html for a single email preview  
def make_preview(message):
  global webpage
  main_text = message.body
  
  link_link = re.compile('https[^\s\]\)>]*') 
  link_name = re.compile('(\S*?//)(\S*?)(/\S*)')
  line_breaks = re.compile('\\r\\n') 
  
  link_list = link_link.findall(main_text)
  main_preview = main_text[:1000] 
  subbed_preview = line_breaks.sub('#BR#', main_preview)
  
  #Creates the main information fields and text for a single email
  sender = message.sender
  subject = message.subject
  time = message.timestamp.strftime('%H:%M:%S %a %y-%m-%d')
  webpage += p(sender + ' at ' + time, cls = 'sender', style='color:green;font-size:15px')
  webpage += p(subject, cls = 'subject', style='color:blue;font-size:15px')
  webpage += p('Message preview:' , cls = 'preview', style ='color:black;font-size:12px;')
  webpage += div(subbed_preview + '...', cls = 'maintext', style ='color:black;font-size:15px;')
  
  #creates links section if there are links to display
  if(not len(link_list)==0):
      links_section = div(p('Message links:#BR#'), cls = 'links', style='color:#ff9900;font-size:12px;')
      with links_section:
        for link in link_list:
            lname = re.sub(link_name, r'\2',link)
            newlink = span('— — — —  ', a(lname, href = link),'  — — — —')
      webpage+= links_section
      webpage+='#BR#'
  
  #creates attachments section if there are any attachments to display
  attachments = message.attachments
  if(not len(attachments) == 0):
    message.downloadAllAttachments(downloadFolder = subdirectory, overwrite = True)
    attachments_section = div(p('Attachments:#BR#'),cls = 'attachments', style='color:#ff9900;font-size:12px;')
    with attachments_section:
      for att in attachments:
        newatt = span('  ————  ', a(att, href = subdirectory + '/' + att),'  ————  ')
    webpage+= attachments_section
    webpage+='#BR#'
    
def main():
    #Gets the appropriate date for yesterday
    global yester_date
    yester_date = get_yesterday()
    
    #names the html file with the date, checks if the target directory exists
    #and creates one if it does not. Then checks if a subdirectory with the date
    #exists and creates one if it does not.
    filename = '%s.html' %yester_date
    if not os.path.isdir(directory):
        os.mkdir(directory)
    global subdirectory
    subdirectory = os.path.join(directory + '/%s'%yester_date)
    if not os.path.isdir(subdirectory):
        os.mkdir(subdirectory)
    file_path = os.path.join(subdirectory, filename)
    
    #Collects emails that fit user parameters and creates initial html text
    emails = get_emails()
    start_page()
    
    
    #adds preview section for every email returned by get_emails()
    for item in emails:
        make_preview(item.messages[0])
    
    #filters the completed html text to reinsert line breaks where placeholder #BR# was inserted
    rebreaks = re.compile('#BR#') 
    webpage_final = rebreaks.sub('<br>', webpage.render())
    
    
    #writes the file and saves it to its subdirectory
    file = open(file_path, 'w')
    file.write(webpage_final)
    file.close()
    
    #prompts user to choose whether or not to mark compiled emails as read
    mark_as_read = ''
    while(not (mark_as_read == 'y' or mark_as_read == 'n')):
        mark_as_read = input('Would you like to mark compiled emails as read? \'y\' to mark read or \'n\' to leave unread: ')
        if mark_as_read == 'y':
            ezgmail.markAsRead(emails)
            
    #opens the webpage in the user's default browser        
    webbrowser.open('file://' + os.path.join(subdirectory, filename))
       
    
if __name__ == "__main__":
    main()
    