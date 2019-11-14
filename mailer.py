import argparse
import smtplib
import pandas as pd

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from settings import *

#revenue dataframe generated from any excel sheet
def mail_table():
    dataframe = pd.read_excel('revenue_sheet.xls')
    expected_revenue = dataframe.groupby(['Mandi'])['Pickup_Cost', 'Sum_of_Commission'].sum()
    expected_revenue = expected_revenue.assign(Revenue = expected_revenue['Sum_of_Commission'] - expected_revenue['Pickup_Cost'])
    sum_expected_revenue = expected_revenue.append(expected_revenue.sum().rename('Total')).round(2).reset_index()
    return sum_expected_revenue

def send_mail(to_email, message):
    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    server.sendmail(EMAIL_HOST_USER, to_email, message.as_string(),)
    server.quit()

#reveiver's email-id arguement created
def add_arguments():
    parser = argparse.ArgumentParser(description='Processing mailer related arguements', usage='%(prog)s[options]')
    parser.add_argument('-e', '--to_email', default=None, nargs='+', help='Enter email-id with comma separated to send summary (e.g. \'a, b, c\')')
    args = parser.parse_args()
    return args

#complete mail body
def mail_body(message):
    args = add_arguments()
    if [args.to_email]:
        to_email = args.to_email
    else:
        to_email = EMAIL_HOST_USER
    
    message['subject'] = 'Automated Mailer Template'
    message['From'] = EMAIL_HOST_USER
    to_email = ' '.join(to_email)
    message['To'] = to_email
    revenue_table = mail_table()
    body = 'Dear User, <br/>This mailer is a template for any random automated mailing system.<br/><br/>The table given below is a part of the template for providing with any table format while sending a mail.<br/><br/>'
    row_list = []
    for obj in revenue_table.itertuples(index = False):
        mandi_row= '''<tr>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                    </tr>'''%(obj.Mandi, obj.Pickup_Cost, obj.Sum_of_Commission, obj.Revenue)

        row_list.append(mandi_row)
    body+= '''
            <html>
                <head>
                    <style>
                        table {
                            font-family: Times New Roman, sans-serif;
                            border-collapse: collapse;
                            width: 100;
                        }
                        td, th {
                            border: 1px solid #dddddd;
                            text-align: left;
                            padding: 8px;
                        }
                        tr:nth-child(even) {
                            background-color: #dddddd;
                        }
                    </style>
                </head>
                <body>
                    <table>
                        <tr>
                            <th>Mandi</th>
                            <th>Sum of Pickup Cost</th>
                            <th>Sum of Commission</th>
                            <th>Expected Revenue</th>
                        </tr>
                        <td>%s</td>
                    </table>
                </body>
            </html>
        <br/><br/>Thank you.            
    '''%(''.join(row_list))
    
    body = MIMEText(body, 'html')
    message.attach(body)
    return message, to_email

try:
    message = MIMEMultipart()
    mail, to_email = mail_body(message)
    send_mail(to_email, message)
    print("Email successfully sent to ", to_email)
except:
    print("SMTPAuthenticationError")
    print("Email not sent")