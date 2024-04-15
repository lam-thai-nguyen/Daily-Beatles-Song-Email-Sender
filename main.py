from email.message import EmailMessage
import smtplib
import ssl
from sender import *
from get_song import get_song, choose_song


def daily_email_sender(sender=sender, password=password, receiver=receiver):
    url = choose_song()
    save_path = get_song(url)
    
    with open(save_path, 'r') as f:
        if len(f.readlines()) < 15:
            return 0
    
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = receiver
    msg["subject"] = "Daily Beatles Song"
    
    with open(save_path, 'r') as f:
        body = f.read()
        
    msg.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, msg=msg.as_string())
    

if __name__ == "__main__":
    while True:
        status = daily_email_sender()
        if status == 0:
            print("This song lyrics are not found!")
            continue
        break
    print("Success")
    