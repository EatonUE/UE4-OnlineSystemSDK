import smtplib,random
from email.mime.text import MIMEText
def send(email):
    check= random.randint(1111,9999)
    msg_from='no-reply@sestudio.ml'
    passwd='mFm5AaCcFfDBc4Rr'
    msg_to=email                            
    subject="EGame中国区账号验证"    
    content="<p>您的EGame游戏账号验证码为"+str(check)+"</p><p>EGame游戏账号安全中心</p>"
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = 'EGame-CN'
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.exmail.qq.com",465)
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
    except:
        pass
    finally:
        s.quit()
    return check
