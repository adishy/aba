import smtplib

from email.mime.text import MIMEText

from threading import Thread

class emailer:
    def __init__(self, 
                 from_email_address_provided, 
                 from_email_password_provided, 
                 smtp_provider = 'smtp.gmail.com:587'):
        
        try:
            self.send_mail_off = True

            if self.send_mail_off:
                return

            self.from_email_address = from_email_address_provided
        
            self.from_email_password = from_email_password_provided

            self.send_mail = smtplib.SMTP(smtp_provider)

            self.send_mail.ehlo()

            self.send_mail.starttls()

            self.send_mail.login(self.from_email_address, self.from_email_password)

        except Exception as smtp_login_error:
            print('Could not login with email credentials')

            print(smtp_login_error)

            raise ValueError

    def getemailtext(self, **kwargs):
        message_provided = MIMEText(kwargs['contenttext'])
        
        message_provided['From'] = kwargs['from_email_address']

        
        message_provided['To'] = kwargs['to_email_address']

        message_provided['Subject'] = kwargs['subjecttext']
      
        return message_provided

    def sendemails(self, **kwargs):
        if self.send_mail_off:
            return

        print('Start sending emails provided')

        def send_emails_provided(self, to_email_addresses, subject, content):
            print('Sending email')
            
            print(to_email_addresses)

            print(subject)

            print(content)

            for some_email_address in to_email_addresses:
                try:
                    print('Sending email to address: ', some_email_address)

                    print(self.getemailtext(from_email_address = self.from_email_address, 
                                            to_email_address = some_email_address, 
                                            subjecttext = subject, 
                                            contenttext = content))

                    self.send_mail.send_message(self.getemailtext(from_email_address = self.from_email_address, 
                                                                  to_email_address = some_email_address, 
                                                                  subjecttext = subject, 
                                                                  contenttext = content))

                    print('Sent email address to: ', some_email_address)

                except Exception as smtp_send_error:
                    print('Could not send email')

                    print(smtp_send_error)

        send_mails = Thread(target = send_emails_provided, 
                            args = (self, 
                                    kwargs['to_email_addresses'], 
                                    kwargs['subject'], 
                                    kwargs['content']))
        send_mails.start()

    def __del__(self):
        if self.send_mail_off:
            return

        self.send_mail.quit()