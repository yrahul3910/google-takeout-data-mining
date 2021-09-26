import os
from bs4 import BeautifulSoup
import re
import mailbox
from userdata_mining.utils import warn
from html.parser import HTMLParser
from io import StringIO


# from https://stackoverflow.com/a/925630/2713263
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def postprocess(text: str) -> str:
    """
    Postprocesses a message text by removing Unicode characters and
    HTML links.

    :param {str} text - The message text
    """
    text = text.encode('ascii', 'ignore').decode()
    text = re.sub('http\S+', '', text, flags=re.MULTILINE)
    s = MLStripper()
    try:
        s.feed(text)
        return " ".join(re.findall("[a-zA-Z]+", s.get_data()))
    except:
        return ""


def get_html_text(html):
    """
    Parses HTML content of a message.

    :param {str} html - The HTML content.
    :return {str} The text content
    """
    try:
        return BeautifulSoup(html, 'lxml').body.get_text(strip=True)
    except AttributeError:  # message contents empty
        return None


# from https://gist.github.com/benwattsjones/060ad83efd2b3afc8b229d41f9b246c4
class GmailMboxMessage():
    def __init__(self, email_data):
        if not isinstance(email_data, mailbox.mboxMessage):
            raise TypeError('Variable must be type mailbox.mboxMessage')
        self.email_data = email_data

    def parse_email(self):
        email_labels = self.email_data['X-Gmail-Labels']
        email_date = self.email_data['Date']
        email_from = self.email_data['From']
        email_to = self.email_data['To']
        email_subject = self.email_data['Subject']
        email_text = self.read_email_payload()

        if isinstance(email_text, list):
            email_text = ' '.join([postprocess(x)
                                   for x in email_text if isinstance(x, str)])
        elif isinstance(email_text, str):
            email_text = postprocess(email_text)
        return email_text

    def read_email_payload(self):
        email_payload = self.email_data.get_payload()
        if self.email_data.is_multipart():
            email_messages = list(self._get_email_messages(email_payload))
        else:
            email_messages = [email_payload]
        return [self._read_email_text(msg) for msg in email_messages]

    def _get_email_messages(self, email_payload):
        for msg in email_payload:
            if isinstance(msg, (list, tuple)):
                for submsg in self._get_email_messages(msg):
                    yield submsg
            elif msg.is_multipart():
                for submsg in self._get_email_messages(msg.get_payload()):
                    yield submsg
            else:
                yield msg

    def _read_email_text(self, msg):
        content_type = 'NA' if isinstance(msg, str) else msg.get_content_type()
        encoding = 'NA' if isinstance(msg, str) else msg.get(
            'Content-Transfer-Encoding', 'NA')
        if 'text/plain' in content_type and 'base64' not in encoding:
            msg_text = msg.get_payload()
        elif 'text/html' in content_type and 'base64' not in encoding:
            msg_text = get_html_text(msg.get_payload())
        elif content_type == 'NA':
            msg_text = get_html_text(msg)
        else:
            msg_text = None
        return msg_text


def parse_mail_data(user, data_path='.'):
    """
    Parses a user's email data in mbox format. If cache exists, returns None.

    :param {str} user - The user directory.
    :param {str} data_path - Path to the data/ directory, without the trailing /.
    :return {list} A list of messages
    """
    # First, check for cache
    if os.path.exists(f'{data_path}/saved/embeddings/mail.pickle'):
        return None

    path = f'{data_path}/data/{user}/Takeout/Mail/All mail Including Spam and Trash.mbox'

    # Check if path exists
    if not os.path.exists(path):
        warn('Mail path does not exist.')
        return []

    box = mailbox.mbox(path)
    messages = []
    for message in box:
        message_obj = GmailMboxMessage(message)
        parsed_mail = message_obj.parse_email()
        if parsed_mail != [] and not re.match('\s+', parsed_mail):
            messages.append(parsed_mail)

    return messages
