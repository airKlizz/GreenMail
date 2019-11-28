import imaplib
import string
import pandas as pd
import mailparser
import re
import nltk
from nltk import word_tokenize
from nltk import sent_tokenize
nltk.download('punkt')
from googletrans import Translator
from nltk.corpus import stopwords 
from gensim.summarization import keywords
from bs4 import BeautifulSoup
from cleantext import clean

def create_csv_mail(location_name, address, password, mails_from_copy = 0, mails_to_copy = -1):
    ### Connection au client mail ###
    domain = address.split('@')[1]
    mail = imaplib.IMAP4_SSL('imap.'+domain)
    mail.login(address, password)
    mail.list()
    mail.select("inbox")

    ### Recuperation de tous les mails au format csv ###
    result, data = mail.search(None, "ALL")
    ids = data[0]
    id_list = ids.split() # id list des mails

    j = 0
    for i in id_list:
        j+=1
    print("Vous avez ", j, " mails dans votre boite mail \n")

    final_tab = []
    value = False

    if(mails_to_copy != -1):
        if(mails_to_copy < j):
            j = mails_to_copy

    if(mails_from_copy != 0):
        if(mails_from_copy >= j):
            mails_from_copy = 0
    
    for i in range(mails_from_copy,j):
        print(i, "/", j)
        result, data = mail.fetch(id_list[i], "(RFC822)") # recupere donnees du mail en question
        raw_email = data[0][1] # donnees du mail

        email = mailparser.parse_from_bytes(raw_email)
        
        from_1 = email.from_[0][1] # Mail du serveur
        from_2 = email.from_[0][0] # Nom mail du serveur
        subject = email.subject
        subject = subject_processing(subject)
        subject = subject_processing2(subject)
        subject = subject_processing3(subject)
        subject = subject_processing4(subject)
        date = email.date # Date du mail
        if len(email.text_plain) == 1:
            text = email.text_plain[0]
            text, url = text_processing(text)
            text = text_processing_2(text)
            text = text_processing_3(text)
            text = text_processing_4(text)
        elif len(email.text_html) > 0:
            text = re.sub(r'<style(\S|\s)*</style>', '', email.text_html[0])
            text = BeautifulSoup(text, "html.parser")
            text = text.get_text(separator=' ')
            text, url = text_processing(text)
            text = text_processing_2(text)
            text = text_processing_3(text)
            text = text_processing_4(text)
        else: 
            text = []
            url = []

        tab = [from_1, from_2, subject, date, text, url]
        final_tab.append(tab)
        
    final_tab_df = pd.DataFrame(final_tab, columns=['from address', 'from name', 'subject', 'date', 'text', 'urls'])
    final_tab_df.to_csv(location_name)

def text_processing(text):
    text = re.sub(r'<.*>', '', text)
    text = clean(text,
        fix_unicode=True,               # fix various unicode errors
        to_ascii=True,                  # transliterate to closest ASCII representation
        lower=True,                     # lowercase text
        no_line_breaks=False,           # fully strip line breaks as opposed to only normalizing them
        no_urls=False,                  # replace all URLs with a special token
        no_emails=False,                # replace all email addresses with a special token
        no_phone_numbers=False,         # replace all phone numbers with a special token
        no_numbers=False,               # replace all numbers with a special token
        no_digits=False,                # replace all digits with a special token
        no_currency_symbols=False,      # replace all currency symbols with a special token
        no_punct=False,                 # fully remove punctuation
        replace_with_url="<URL>",
        replace_with_email="<EMAIL>",
        replace_with_phone_number="<PHONE>",
        replace_with_number="<NUMBER>",
        replace_with_digit="0",
        replace_with_currency_symbol="<CUR>",
    )

    url = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)

    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    text = re.sub(r'www\S*', '', text)
    return text, url

def text_processing_2(text):
    words = text.split()
    table = str.maketrans('', '', "\!\"#$%&()*+,/:;<=>?@[\]^_`{|}~")
    stripped = [w.translate(table) for w in words]
    words = stripped
    text_2 = ""
    for word in words:
        text_2 = text_2 + word + " "

    return text_2

def text_processing_3(text):
    text = re.sub(r'---*', '', text)
    text = re.sub(r'\.\.\.*', '', text)
    return text

def text_processing_4(text):
    tokens = sent_tokenize(text)
    tab = []
    for token in tokens:
        txt = token
        txt = re.sub(r'\.*', '', txt)
        if txt != '':
            translator = Translator()
            tab.append((translator.translate(txt, dest='en')).text)

    return tab

def subject_processing(text):
    text = re.sub(r'<.*>', '', text)
    text = clean(text,
        fix_unicode=True,               # fix various unicode errors
        to_ascii=True,                  # transliterate to closest ASCII representation
        lower=True,                     # lowercase text
        no_line_breaks=False,           # fully strip line breaks as opposed to only normalizing them
        no_urls=False,                  # replace all URLs with a special token
        no_emails=False,                # replace all email addresses with a special token
        no_phone_numbers=False,         # replace all phone numbers with a special token
        no_numbers=False,               # replace all numbers with a special token
        no_digits=False,                # replace all digits with a special token
        no_currency_symbols=False,      # replace all currency symbols with a special token
        no_punct=False,                 # fully remove punctuation
        replace_with_url="<URL>",
        replace_with_email="<EMAIL>",
        replace_with_phone_number="<PHONE>",
        replace_with_number="<NUMBER>",
        replace_with_digit="0",
        replace_with_currency_symbol="<CUR>",
    )

    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    text = re.sub(r'www\S*', '', text)
    return text

def subject_processing_2(text):
    words = text.split()
    table = str.maketrans('', '', "\!\"#$%&()*+,/:;<=>?@[\]^_`{|}~")
    stripped = [w.translate(table) for w in words]
    words = stripped
    text_2 = ""
    for word in words:
        text_2 = text_2 + word + " "

    return text_2

def subject_processing_3(text):
    text = re.sub(r'---*', '', text)
    text = re.sub(r'\.\.\.*', '', text)
    return text

def subject_processing_4(text):
    text = re.sub(r'\.*', '', text)
    if text != '':
        translator = Translator()
        text = (translator.translate(text, dest='en')).text

    return text

if __name__ == "__main__":
    addr = input("addr = ")
    mdp = input("password = ")
    filename = input("filename = ")
    nb_from = input("from mail numero = ")
    nb_to = input("to mail numero (-1 for maximum) = ")

    create_csv_mail(filename, addr, mdp, int(nb_from), int(nb_to))

