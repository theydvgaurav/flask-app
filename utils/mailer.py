import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailWrapper:
    def __init__(self, smtp_server, port, username, password, use_tls=True):
        self.smtp_server = smtp_server
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls

    def send_email(self, to_address, subject, body, from_address=None, cc=None, bcc=None, attachments=None):
        if from_address is None:
            from_address = self.username

        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = to_address
        msg['Subject'] = subject
        if cc:
            msg['Cc'] = ','.join(cc)

        msg.attach(MIMEText(body, 'plain'))

        if attachments:
            for attachment in attachments:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment['content'])
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f"attachment; filename= {attachment['filename']}",
                )
                msg.attach(part)

        try:
            server = smtplib.SMTP(self.smtp_server, self.port)
            if self.use_tls:
                server.starttls()
            server.login(self.username, self.password)
            to_addresses = [to_address] + (cc if cc else []) + (bcc if bcc else [])
            server.sendmail(from_address, to_addresses, msg.as_string())
            server.quit()
            return {'status': 'success', 'message': 'Email sent successfully'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
