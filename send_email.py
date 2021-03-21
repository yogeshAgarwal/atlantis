import re
import smtplib

class SendMailTest:
    def send_email_test(self, subject, message, recipient):
        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # start TLS for security
        s.starttls()
        # Authentication
        s.login("avantehatsphere@gmail.com", "xbdjhfjjxryqlesb")
        # ps - above one is not the actual password :p, its a temporarily created app password will remove it after 1 week.
        # message to be sent
        # sending the mail
        message = 'Subject: {}\n\n{}'.format(subject, message)
        s.sendmail("avantehatsphere@gmail.com", recipient, message, subject)
        # print(s.__dict__)
        s.quit()
        return True


if __name__ == '__main__':
    subject = input("Subject?")
    message = input("body?")
    recipient = input("Recipient?")
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    while(True):
        if not (re.search(regex, recipient)):
            recipient = input("Email id is not correct, please enter it again?")
        else:
            break
    obj = SendMailTest()
    response = obj.send_email_test(subject, message, recipient)
    if response is True:
        print("Mail Sent")