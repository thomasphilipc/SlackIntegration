import smtplib
import time
import imaplib
import email
from bs4 import BeautifulSoup
import re

# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------

ORG_EMAIL   = "@gmail.com"
FROM_EMAIL  = "roamworkstech" + ORG_EMAIL
FROM_PWD    = "Tom@RW1206"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993

def read_email_from_gmail():
    #try:
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL,FROM_PWD)
        # print(mail.list()) # prints the folders
    mail.select('inbox')

    result, data = mail.uid('search', None, "ALL") # search and return uids instead
    latest_email_uid = data[0].split()[-1]

    #print((data[0][1]))
    uid_list = data[0].decode("utf-8", "ignore").split()
    print (uid_list)

    for i in range (len(list(data[0].split()))):
        email_uid = uid_list[i]
        result, data = mail.uid('fetch', email_uid, '(RFC822)')
        raw_email = data[0][1]

        email_message=email.message_from_bytes(raw_email)

        sender = email_message['from']
        receipient  = email_message['to']
        cc = email_message['cc']
        bcc = email_message['bcc']
        #similar to subject get only the date , strip all metadata
        a = email_message['Received']
        a = a.strip(',.-')
        a = a.replace('  ','')

        received_on = a[a.find(",")-3:a.find("-")]
        received_on.strip()
        print(len(received_on))

        subject = email_message['subject']
        #because subject may contain additional metadata , strip them , and shorten the subject
        if len(subject) > 300 :
            subject = subject[:299]
        subject = subject.replace('=','')
        subject = subject.replace('?','')

        for part in email_message.walk():
            body_str=''

            if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html" :
                    #try various encodings
                    encodings =[part.get_content_charset(),'ISO-8859-1','UTF-8','Windows-1252']
                    for encoding in encodings :
                        try:

                           body_bytes = part.get_payload(decode=True)
                           body_str = body_bytes.decode(encoding)
                           soup = BeautifulSoup(body_str,"html.parser")
                           body = soup.get_text()
                           body = re.sub(r'<.*?>', '', body)
                        except Exception:
                            pass


            if part.get_content_maintype() == 'multipart':
                pass

            if part.get('Content-Disposition') is None:
                pass


        print("FROM:"+sender)
        print("SUBJECT:"+subject)
        print("TO:"+receipient)
        if cc != None:
            print("CC:"+ cc)
        print("DATE:"+received_on)
        print("Body_HTML:"+body_str)
        print("Body_Simple:"+str(body))


read_email_from_gmail()