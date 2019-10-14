import imaplib
import pandas as pd
import mailparser
import re
import nltk
from nltk import word_tokenize
nltk.download('punkt')
from googletrans import Translator
translator = Translator(service_urls=[
      'translate.google.com',
    ])
from rake_nltk import Rake
from nltk.corpus import stopwords 
from gensim.summarization import keywords

def create_csv_gmail(location_name, address, password, mails_to_copy = -1):
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
    
    for i in range(0,j):
        print(i, "/", j)
        result, data = mail.fetch(id_list[i], "(RFC822)") # recupere donnees du mail en question
        raw_email = data[0][1] # donnees du mail

        email = mailparser.parse_from_bytes(raw_email)
        
        from_1 = email.from_[0][1] # Mail du serveur
        from_2 = email.from_[0][0] # Nom mail du serveur
        subject = email.subject
        date = email.date # Date du mail
        if len(email.text_plain) == 1:
            text = email.text_plain[0] # Texte du mail
        else:
            text = ""

        tab = [from_1, from_2, subject, date, text]
        final_tab.append(tab)
        
    final_tab_df = pd.DataFrame(final_tab)
    final_tab_df.to_csv(location_name)

def get_pandas_from_csv(filename):
    df = pd.read_csv(filename)
    return df

def get_pandas_from_list_csv(filenames):
    df = pd.read_csv(filenames[0])
    for i in filenames[1:]:
        df2 = pd.read_csv(i)
        df = df.append(df2, ignore_index=True)
    return df

def get_txt_from_pandas(df):
    for i in range(0, len(df['4'])):
        df.set_value(i, '4', get_txt_from_string(df['4'][i]))
        df.set_value(i, '2', get_txt_from_string(df['2'][i]))
    return df

def get_translated_from_pandas(df):
    translator = Translator()
    print("Vous avez ", len(df['4']), " mails à traduire \n")
    for i in range(0, len(df['4'])):
        print(i, "/", len(df['4']))
        df.set_value(i, '4', get_translated_from_string(df['4'][i], translator))
        df.set_value(i, '2', get_translated_from_string(df['2'][i], translator))
    return df

def get_translated_from_pandas_and_create_csv(df, location_name):
    translator = Translator()
    print("Vous avez ", len(df['4']), " mails à traduire \n")
    for i in range(0, len(df['4'])):
        print(i, "/", len(df['4']))
        df.set_value(i, '4', get_translated_from_string(df['4'][i], translator))
        df.set_value(i, '2', get_translated_from_string(df['2'][i], translator))
    df.to_csv(location_name)
    return df

def get_keywords_from_pandas(df, nb_keywords_subject, nb_keywords_text):
    for i in range(0, len(df['4'])):
        df.set_value(i, '4', get_keywords_from_string(df['4'][i], nb_keywords_text))
        df.set_value(i, '2', get_keywords_from_string(df['2'][i], nb_keywords_subject))
    return df

def get_txt_from_string(text):
    text = str(text)
    text = re.sub(r'https?\S*', '', text)
    text = re.sub(r'www\S*', '', text)
    text = re.sub(r'\S*#\S*', '', text)
    text = re.sub(r'-*', '', text)
    text = re.sub(r'_*', '', text)
    text = re.sub(r'<.*>', '', text)
    text = nltk.word_tokenize(text)
    text = ' '.join(text)
    text = re.sub(r"[^\w@()':?;., ]",'', text)
    return text

def get_translated_from_string(text, translator):
    try:
        translation = translator.translate(text)
    except:
        print("TRANSLATION ERROR")
        return ""
    return translation.text

def get_keywords_from_string(text, nb_keywords):
    try:
        keyw = keywords(text, words = nb_keywords, scores = True, lemmatize = True)
    except:
        try:
            keyw = keywords(text, words = 5, scores = True, lemmatize = True)
        except:
            try:
                keyw = keywords(text, words = 1, scores = True, lemmatize = True)
            except:
                print("KEYWORD ERROR")
                keyw = ""
    return keyw
