#import mailer_localhost
import email_helper

recipient = 'bartsmeding@gmail.com'
subject = 'Test message'
message = '''

This is a fictional test message.


Regards,

Bart

'''

sender = 'ktbyers@twb-tech.com'
email_helper.send_mail(recipient, subject, message, sender)
