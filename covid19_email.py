import pandas as pd
import numpy as np
import smtplib
import ssl
import matplotlib.pyplot as plt
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders

# add curvefit and fbprophet

# uses JHU Covid19 Github Data
df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')

# plots cases for specific county

def plotCases(county):
    co = df[df['Admin2'] == county].iloc[:, 12:]
    co = co.transpose()
    co.columns = ['Cases']
    co = pd.DataFrame(co)
    co.columns = ['Cases']
    co = co.loc[co['Cases'] > 0]
    y = np.array(co['Cases'])
    x = np.arange(y.size)
    thisweek = y[-1]
    lastweek = y[-8]
    bodymessage = ""
    bodymessage += county + ' County\n'
    bodymessage += '\n\tTotal Number of Cases Today: ' + str(y[len(y)-1])
    bodymessage += '\n\tTotal Number of Cases Yesterday: ' + str(y[len(y)-2])
    bodymessage += '\n\tWeekly Increase:' + \
        str(round(100 * (thisweek/lastweek - 1), 1)) + '%'
    plt.figure(figsize=(10, 5))
    plt.plot(x, y, 'ko', label="JHU Data")
    plt.title(county + ' County Cumulative COVID-19 Cases. ', fontsize="large")
    plt.xlabel('Days', fontsize="large")
    plt.ylabel('Total Cases', fontsize="large")
    plt.legend(fontsize="large")
    plt.savefig('Desktop/' + county + '.png')
    plt.show()
    return bodymessage


plotCases('Collin')


# sending email https://www.geeksforgeeks.org/send-mail-attachment-gmail-account-using-python/
def sendEmail(county):
    fromaddr = "sender email address"
    toaddr = "receiver email address"
    msg = MIMEMultipart()

    msg['From'] = fromaddr

    msg['To'] = toaddr

    msg['Subject'] = county + " County Corona Virus Daily Update"

    body = plotCases(county)

    msg.attach(MIMEText(body, 'plain'))

    filename = county + ".png"
    attachment = open("Desktop/" + filename, "rb")

    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(fromaddr, "password of sender username")

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()

sendEmail('Collin')
