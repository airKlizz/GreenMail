import sys
sys.path.append("../data/")
sys.path.append("../function/")
import numpy as np
import function
import data
import pandas
#import spacy
#nlp = spacy.load('en_core_web_md') 
import method_3_function as f
import operator


### Return matrix of similarity for mail address, 1 if same email address and 0 if not ###
def get_addr_mat(df):
    mailbox_size = len(df)
    matrix = np.zeros([mailbox_size, mailbox_size])

    current_index = 0
    for i in df['from address']:
        for j in range(current_index, mailbox_size):
            if(i == df['from address'][j]):
                matrix[current_index][j] = 1
                matrix[j][current_index] = 1
            else:
                matrix[current_index][j] = 0
                matrix[j][current_index] = 0
        current_index+=1

    return matrix

### Return all words and their occurence in the whole mailbox ###
### nb_min is the minimal occurence of the word to return it ###
def get_all_words(df, nb_min = 1):
    full_text = ""
    for text in df['text']:
        full_text = full_text + " " + text
    
    list_words = f.get_list_words(full_text)
    dict_words, list_single_words = f.get_dict_and_single_list_words(list_words)

    ### On supprime les mots ayant un nb d'occurence inférieur à nb_min ###
    for word in list_single_words:
        if(dict_words[word] < nb_min):
            dict_words.pop(word, None)

    ### On supprime les stopwords ###
    dict_words_without_stopwords = f.delete_stopwords_from_dict(dict_words)

    sorted_dict = sorted(dict_words_without_stopwords.items(), key=operator.itemgetter(1), reverse=True)

    return sorted_dict



