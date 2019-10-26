import sys
sys.path.append("../data/")
sys.path.append("../function/")
import function
import data
import pandas
import re

def get_list_words(text):
    text = re.sub(r'\S*[0123456789]\S*', '', text)
    text = re.sub('[:"\'().,-?_!;]', '', text)
    text = text.lower()
    list_words = text.split(' ')
    list_words.sort()
    return list_words

def get_list_words_as_text(list_words):
    text = list_words[0]
    for word in list_words[1:]:
        text = text + " " + word
    return text

def get_dict_and_single_list_words(list_words):
    dict_words = dict()
    list_single_words = []
    precedent_value = ''
    for word in list_words:
        if word != '':
            if precedent_value != word:
                dict_words[word] = 1
                list_single_words.append(word)
                precedent_value = word
            else:
                dict_words[word] += 1

    return dict_words, list_single_words