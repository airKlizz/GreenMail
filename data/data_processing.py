import pandas as pd
import re
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
lemmatizer = WordNetLemmatizer()

def nltk2wn_tag(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:          
        return None

def lemmatize_sentence(sentence):
    nltk_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))  
    wn_tagged = map(lambda x: (x[0], nltk2wn_tag(x[1])), nltk_tagged)

    res_words = []
    for word, tag in wn_tagged:
        if tag is None:            
            res_words.append(word)
        else:
            res_words.append(lemmatizer.lemmatize(word, tag))
    
    return " ".join(res_words)

def get_pandas_from_csv(filename):
    df = pd.read_csv(filename, index_col=0)
    return df

def get_sentences_from_text_df(text):
    tab = text.split(',')
    new_tab = []
    first = True
    for elem in tab:
        if first:
            new_tab.append((elem[1:-1]).lower())
            first = False
        else:
            new_tab.append((elem[2:-1]).lower())

    return new_tab

def lemmatize_tab(tab):
    new_tab = []
    for elem in tab:
        new_tab.append(lemmatize_sentence(elem))
    
    return new_tab

def delete_stopwords_sentence(sentence):
    words = sentence.split(' ')
    new_words = []
    for word in words:
        if word not in stopwords.words('english'):
            new_words.append(word)
                
    return " ".join(new_words)

def delete_stopwords_tab(tab):
    new_tab = []
    for elem in tab:
        new_tab.append(delete_stopwords_sentence(elem))
    
    return new_tab

def stemmed_sentence(sentence):
    words = sentence.split(' ')
    new_words = []
    for word in words:
        new_words.append(stemmer.stem(word))
    
    return " ".join(new_words)

def stemmed_tab(tab):
    new_tab = []
    for elem in tab:
        new_tab.append(stemmed_sentence(elem))
    
    return new_tab

def no_number_sentence(sentence):
    words = sentence.split(' ')
    new_words = []
    for word in words:
        elem = re.sub(r'[0-9]*', '', word)
        if elem != '':
            new_words.append(word)
    
    return " ".join(new_words)

def no_number_tab(tab):
    new_tab = []
    for elem in tab:
        new_tab.append(no_number_sentence(elem))
    
    return new_tab

def no_short_words_sentence(sentence, NB_TO_SUPPRESS = 3):
    words = sentence.split(' ')
    new_words = []
    for word in words:
        if len(word) > NB_TO_SUPPRESS:
            new_words.append(word)
    
    return " ".join(new_words)

def no_short_words(tab, NB_TO_SUPPRESS = 3):
    new_tab = []
    for elem in tab:
        new_tab.append(no_short_words_sentence(elem, NB_TO_SUPPRESS))
    
    return new_tab

def get_full_process(text):
    text = text[1:-1]
    tab = get_sentences_from_text_df(text)
    tab_no_short_words = no_short_words(tab, 3)
    tab_lemmatize = lemmatize_tab(tab_no_short_words)
    tab_no_stopwords = delete_stopwords_tab(tab_lemmatize)
    tab_stemmed = stemmed_tab(tab_no_stopwords)
    tab_no_number = no_number_tab(tab_stemmed)

    return tab_no_number

def get_only_list_words(tab):
    new_list = []
    for elem in tab:
        words = elem.split(' ')
        for word in words:
            new_list.append(word)
    
    return new_list

if __name__ == "__main__":
    filename = "my_csv_test.csv"

    """
    df = get_pandas_from_csv("my_csv_test.csv")
    text = df['text'][0][1:-1]
    tab = get_sentences_from_text_df(text)
    tab_lemmatize = lemmatize_tab(tab)
    tab_no_stopwords = delete_stopwords_tab(tab_lemmatize)
    tab_stemmed = stemmed_tab(tab_no_stopwords)

    print("\nTEXT : \n", text)
    print("\nTAB : \n", tab)
    print("\nTAB_LEMMATIZE : \n", tab_lemmatize)
    print("\nTAB_NO_STOPWORDS : \n", tab_no_stopwords)
    print("\nTAB_STEMMED : \n", tab_stemmed)
    """

    df = get_pandas_from_csv("my_csv_test.csv")
    processed_docs = []
    for i in range(0,70):
        processed_tab = get_full_process(df['text'][i])
        list_words = get_only_list_words(processed_tab)
        processed_docs.append(list_words)
        #print(list_words)

    dictionary = gensim.corpora.Dictionary(processed_docs)
    bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

    lda_model =  gensim.models.LdaMulticore(bow_corpus, num_topics = 7, id2word = dictionary, passes = 100, workers = 2)

    for i in range(0,7):
        string = ""
        for elem in lda_model.get_topic_terms(i):
            string = string + " " + dictionary[elem[0]]
        print("TOPIC ", i, " ", string)

    print("\n\n")

    for i in range(0,70):
        print(df['subject'][i], sorted(lda_model[bow_corpus[i]], key=lambda tup: -1*tup[1]))
