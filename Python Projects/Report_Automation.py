
"""
Weekly Productivity Report Automator
------------------------------------
Description: 
This script automates the generation and delivery of weekly productivity reports via email. It dynamically calculates the reporting period (Monday to Thursday), retrieves the three most recent performance charts from a local directory, and embeds them into a professionally formatted HTML email—including a company logo and custom signature—using SMTP with SSL encryption.
"""

import pandas as pd
from email.message import EmailMessage
from email.utils import make_msgid
from datetime import datetime, timedelta
import smtplib
import os
import glob

# --- Credentials and accesses ---
PATH = r"C:\Users\Carlos Reyes\Desktop\MA-007"
LOGO_PATH = r"C:\Users\Carlos Reyes\Desktop\MA-007\logo.png" 
APP_PSW = 'XXX'
EMAIL_USERNAME = 'XXX'
RECIPIENT = ['XXX', 'xxx', 'xxx']

# --- Automatic date configuration ---
today = datetime.now()
monday = today - timedelta(days=4)
thursday = today - timedelta(days=1)
start_date = monday.strftime('%m/%d') 
end_date = thursday.strftime('%m/%d') 

def send_report():
    # 1. Getting the most recent images of the destinated file
    files = glob.glob(os.path.join(PATH, "*.png"))
    report_files = sorted(files, key=os.path.getmtime, reverse=True)[:3]
    report_files.reverse() 

    if len(report_files) < 3:
        print(f"Error: The 3 report captures were not found in {PATH}.")
        return

    # 2. Creating message structure
    msg = EmailMessage()
    msg['Subject'] = f'End of week report {start_date} - {end_date} | MA-007 Tallman Eye Associates'
    msg['From'] = EMAIL_USERNAME
    msg['To'] = ", ".join(RECIPIENT)
    msg['Cc'] = 'XXX'

    report_cid = [make_msgid()[1:-1] for _ in range(3)]
    logo_cid = make_msgid()[1:-1]

    # 3. HTML structure 
    html_body = f"""
    <html>
        <body style="font-family: Arial, Helvetica, sans-serif; font-size: 12pt; color: #333; line-height: 1.5;">
            <p>Good afternoon team,</p>
            <p>I hope this email finds you well there.</p>
            <p>I'm sharing this week's productivity report, covering from <strong>{start_date} to {end_date}</strong>.</p>
            
            <p><strong>Weekly Numbers:</strong><br>
            <img src="cid:{report_cid[0]}" width="650" style="display: block; margin-top: 10px; border: 1px solid #eee;"></p>
            
            <p><strong>Productivity per day:</strong><br>
            <img src="cid:{report_cid[1]}" width="650" style="display: block; margin-top: 10px; border: 1px solid #eee;"></p>
            
            <p><strong>Individual KPIs and calls taken by agent:</strong><br>
            <img src="cid:{report_cid[2]}" width="650" style="display: block; margin-top: 10px; border: 1px solid #eee;"></p>
            
            <p>If you have any questions, I'll be glad to address it with insights.</p>
            <p>Bests,</p>
            
            <div style="font-size: 12pt; line-height: 1.2;">
                <img src="cid:{logo_cid}" width="200" style="margin-top: 5px;">
            </div>
            
        </body>
    </html>
    """

    msg.set_content(f"I'm sharing this week's productivity report, covering from {start_date} to {end_date}.")
    msg.add_alternative(html_body, subtype='html')

    # 4. Attach report images
    for i, path in enumerate(report_files):
        with open(path, 'rb') as img:
            msg.get_payload()[1].add_related(img.read(), maintype='image', subtype='png', cid=f"<{report_cid[i]}>")

    # 5. Attach Logo
    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, 'rb') as img:
            msg.get_payload()[1].add_related(img.read(), maintype='image', subtype='png', cid=f"<{logo_cid}>")

    # 6. Sending
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_USERNAME, APP_PSW)
            server.send_message(msg)
        print("Email sent successfully with Sans Serif Medium font.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_report()
