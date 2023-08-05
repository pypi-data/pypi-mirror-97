import mimetypes
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email import encoders
from typing import Dict, List


def attach_file(file_to_send: str):
    ctype, encoding = mimetypes.guess_type(file_to_send)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)
    if maintype == "text":
        with open(file_to_send, "r") as fp:
            attachment = MIMEText(fp.read())
    elif maintype == "image":
        with open(file_to_send, "rb") as fp:
            attachment = MIMEImage(fp.read())
    elif maintype == "audio":
        with open(file_to_send, "rb") as fp:
            attachment = MIMEAudio(fp.read())
    else:
        with open(file_to_send, "rb") as fp:
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=file_to_send)

    return attachment


def create_email_message(subject: str, sender: str, recipients: str, text: str, html: str,
                         params: dict = Dict, file_to_send: str = "", files_to_send=None) -> MIMEMultipart:
    """
    Sends an email using both an html and text version.\n
    Based originally on example from: https://docs.python.org/3/library/email-examples.html
    :param subject: Subject of the email.
    :param sender: Email address to send from.
    :param recipients: Email address to send to. For multiple recipients, separate the addresses with coma space (, )
    :param text: Text version of the email.
    :param html: HTML version of the email.
    :param params: dictionary of items to replace in the message body, using square brackets.\n
                    \t Example: "[firstname]" would be replaced by "John"
    :param files_to_send: Single file to send as an attachment
    :param file_to_send: Multiple files to send as an attachment
    :return: Email message to send through SMTP.
    """
    if files_to_send is None:
        files_to_send = []
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipients

    html, text = merge_params(html, text, params)
    part1 = ''
    part2 = ''
    if text:
        part1 = MIMEText(text, 'plain')
    if html:
        part2 = MIMEText(html, 'html')

    if part1:
        msg.attach(part1)
    if part2:
        msg.attach(part2)

    if file_to_send:
        msg.attach(attach_file(file_to_send))

    for f in files_to_send:
        msg.attach(attach_file(f))

    return msg


def merge_params(html, text, params):
    for key in params.keys():
        text = text.replace('[{}]'.format(key), params[key])
        html = html.replace('[{}]'.format(key), params[key])

    return html, text
