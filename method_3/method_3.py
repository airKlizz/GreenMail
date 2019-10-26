import sys
sys.path.append("../data/")
sys.path.append("../function/")
import function
import data
import pandas
import spacy
nlp = spacy.load('en_core_web_md') 
import method_3_function as f

SUBJECT_INFLUENCE = 5
MIN_DIST = 0.4
MIN_ALIKE_WORDS = 1.0

df = data.get_pandas_from_csv("../data/mails_method_3_1_translated.csv")

l = "trading stock volatility"
tokens_keyword = nlp(l)
#for t in tokens_keyword:
    #print(t.text, t.has_vector, t.vector_norm, t.is_oov)

## TEST : 
# Get words from 300D and apply distance to see if there is
# any correlation between distance and meaning
## METHOD :
# Get list of every word from a mail
# Make list of 'test word' to identify a type of mail
# Check if distance with one of our 'test word' has a distance < MIN_DIST
# if case add at a value, get either the ponderation with number of words in the mail
# and the number of alike words
# Check if ponderation > MIN_POND or if alike words > MIN_ALIKE_WORDS
# if case, we classify the mail with the type we tested

for i in range(0,len(df)):
    text = SUBJECT_INFLUENCE*(df['2'][i] + ' ') + df['4'][i]

    list_words = f.get_list_words(text)
    nb_words = len(list_words)

    dict_words, list_single_words = f.get_dict_and_single_list_words(list_words)
    nb_different_words = len(list_single_words)

    text_words = f.get_list_words_as_text(list_single_words)

    tokens_text = nlp(text_words)
    #for t in tokens_text:
        #print(t.text, t.has_vector, t.vector_norm, t.is_oov)

    score = 0
    for tok1 in tokens_keyword:
        if tok1.has_vector:
            for tok2 in tokens_text:
                if tok2.has_vector:
                    if tok1.similarity(tok2) > MIN_DIST:
                        score += (tok1.similarity(tok2) - MIN_DIST)*dict_words[tok2.text]
                        #print(tok1.text, tok2.text, tok1.similarity(tok2), dict_words[tok2.text])

    if (score/nb_words)*100 > MIN_ALIKE_WORDS:
        print(score, (score/nb_words)*100, df['2'][i])