from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib, ssl

class Email():

  SMTP_SERVER = 'smtp.gmail.com' 
  PORT =  587  # For starttls

  def __init__(self, sender:str, subject:str, body:str, body_type:str, 
               receiver:list, attachments=None|list):
    self.sender = sender
    self.receiver = receiver
    self.subject = subject
    self.body = body
    self.body_type = body_type
    self.attachments = attachments
    self.messages = self.message()
    
  
  def create_msg(self):
    msg = MIMEMultipart('alternative')
    msg["From"] = self.sender
    msg["To"] = ', '.join(self.receiver)
    msg["Subject"] = self.subject
    self.msg = msg


  def add_body(self):

    if self.body_type.casefold() == 'PLAIN'.casefold():
      body_part = MIMEText(self.body, "plain")
      self.msg.attach(body_part)
    elif self.body_type.casefold() == 'HTML'.casefold():
      body_part = MIMEText(self.body, "html")
      self.msg.attach(body_part)
    else:
      pass    


  def add_attachments(self):

    if self.attachments is not None:
      for filename in self.attachments:
        with open(filename, "rb") as file:
          # Add file as application/octet-stream
          # Email client can usually download this automatically as attachment
          part = MIMEBase("application", "octet-stream")
          part.set_payload(file.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header("Content-Disposition",
                        "attachment; filename= {0}".format(filename)
                        )
        # Add attachment to message and convert message to string
        self.msg.attach(part)

    else:
      pass


  def message(self):
    self.create_msg()
    self.add_body()
    self.add_attachments()
    return self.msg

  @classmethod
  def send(cls, user:str, password:str,msg):
    # Create a secure SSL context
    """ This will load the system’s trusted CA certificates, enable host name checking 
    # and certificate validation, and try to choose reasonably secure protocol and 
    # cipher settings."""
    context = ssl.create_default_context()

    with smtplib.SMTP(host=cls.SMTP_SERVER, port=cls.PORT) as server:
      server.starttls(context=context)
      server.login(user=user, password=password)
      server.sendmail(from_addr=msg.sender, to_addrs=msg.receiver, msg=msg.messages.as_string())
      print('The email has been sent successfully!')
