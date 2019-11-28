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
import func_matrix as f_m
import re


df = data.get_pandas_from_csv("../data/mails_method_3_1_translated_3.csv")
sorted_list_words = f_m.get_all_words(df, 10)
print(sorted_list_words)
print(len(sorted_list_words))
