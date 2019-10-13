import imaplib
import pandas as pd
import mailparser
import re
import nltk
nltk.download('punkt')
from googletrans import Translator
import sys
sys.path.append("GreenMail")
sys.path.append('../')
from function.function import *

# Output :
# pd : pandas dataframe which contains emails of the inbox

def create_dataframe(addr, password, domain, folder_name='database/', name='unknown'):
    # Input :
    # addr : email address
    # password : password of the account
    # domain : imap url (ex: 'imap.gmail.com')
    # name : name of the pickle file created
    #
    # Create a dataframe containing all emails of the inbox

    mail = imaplib.IMAP4_SSL(domain)
    mail.login(addr, password)
    mail.list()
    mail.select("inbox")

    df = pd.DataFrame(data=None, index=None, columns=['from name', 'from address', 'subject', 'date', 'text', 'html'], dtype=None, copy=False)

    result, data = mail.search(None, "ALL")
    ids = data[0]
    id_list = ids.split() # id list des mails

    final_tab = []
    value = False

    for i, id in enumerate(id_list):

        progbar(i, len(id_list), 20)

        result, data = mail.fetch(id, "(RFC822)") # recupere donnees du mail en question
        raw_email = data[0][1] # donnees du mail

        email = mailparser.parse_from_bytes(raw_email)

        from_1 = email.from_[0][1] # Mail du serveur
        from_2 = email.from_[0][0] # Nom mail du serveur
        subject = email.subject
        date = email.date
        try:
            text = email.text_plain[0] # Texte du mail
        except:
            test = ''
        try:
            html = email.text_html[0]
        except:
            html = ''

        df.loc[i] = [from_1, from_2, subject, date, text, html]


    df.to_pickle(folder_name+name+'.plk')

class DataMail:

    def __init__(self, list_pickle_name, folder_name='database/'):

        frames = []
        for name in list_pickle_name:
            frames.append(pd.read_pickle(folder_name+name+'.plk'))

        self.df = pd.concat(frames)
        self.text = self.df['text'].apply(self.text)
        #self.subject_text = self.df['subject'].apply(self.text)
        self.translate = self.text.apply(self.translate)
        #self.subject_translate = self.subject_text.apply(self.translate)

    def text(self, text):
        text = re.sub(r'https?\S*', '', text)
        text = re.sub(r'www\S*', '', text)
        text = re.sub(r'\S*#\S*', '', text)
        text = re.sub(r'-*', '', text)
        text = re.sub(r'_*', '', text)
        text = re.sub(r'<.*>', '', text)
        text = nltk.word_tokenize(text)
        text = ' '.join(text[:512])
        text = re.sub(r"[^\w@()':?;., ]",'', text)
        return text

    def translate(self, text):
        try:
            translator = Translator()
            translation = translator.translate(text)
            return translation.text
        except:
            return text

    def get_text(self):
        df = self.df.copy()
        df['text'] = self.text
        df['subject'] = self.subject_text
        del df['html']
        return df

    def get_translate(self):
        df = self.df.copy()
        df['text'] = self.translate
        df['subject'] = self.subject_translate
        del df['html']
        return df
