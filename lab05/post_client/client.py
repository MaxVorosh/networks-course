import sys
import smtplib
import email.mime.multipart
import email.mime.text
from password import PASSWORD


if len(sys.argv) != 4:
    print("Wrong amount of arguments")
    sys.exit()

addr = sys.argv[1]
content = sys.argv[2]
type = sys.argv[3]
my_addr = 'ma.voroshilov2004@gmail.com'

if type not in ['html', 'text']:
    print('type should be html ot text')
    sys.exit()

msg = email.mime.multipart.MIMEMultipart('alternative')
msg['Subject'] = 'Example'
msg['From'] = my_addr
msg['To'] = addr

if type == 'html':
    f = open(content)
    msg_content = email.mime.text.MIMEText(f.read(), 'html')
    f.close()
else:
    msg_content = email.mime.text.MIMEText(content, 'plain')
msg.attach(msg_content)
smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.starttls()
smtpObj.login(my_addr, PASSWORD)
smtpObj.sendmail(my_addr, addr, msg.as_string())
smtpObj.quit()
