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

list_keywords = []

for i in range(0,len(df)):
    text = SUBJECT_INFLUENCE*(df['2'][i] + ' ') + df['4'][i]

    list_words = f.get_list_words(text)
    for word in list_words:
        if word not in list_keywords:
            list_keywords.append(word)

text_keywords = f.get_list_words_as_text(list_keywords)
tokens_keyword = nlp(text_keywords)

cumul_3D = []
cpt = 0
for i in range(0,len(df)):
    print(cpt, "/", len(df))
    cpt+=1
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
    cumul_2D = []
    for tok1 in tokens_keyword:
        cumul = 0
        if tok1.has_vector:
            for tok2 in tokens_text:
                if tok2.has_vector:
                    if tok1.similarity(tok2) > MIN_DIST:
                        try:
                            #score += (tok1.similarity(tok2) - MIN_DIST)*dict_words[tok2.text]
                            cumul += 1
                        except:
                            print("ERROR WITH ", tok2.text)
                        #print(tok1.text, tok2.text, tok1.similarity(tok2), dict_words[tok2.text])
        cumul_2D.append(cumul)
    
    cumul_3D.append(cumul_2D)
    #if (score/nb_words)*100 > MIN_ALIKE_WORDS:
        #print(score, (score/nb_words)*100, df['2'][i])

for i in range(len(tokens_keyword)):
    average = 0
    for j in range(len(df)):
        average += cumul_3D[j][i]
    average = average / len(df)

    variance = 0
    for j in range(len(df)):
        variance += (cumul_3D[j][i]-average)*(cumul_3D[j][i]-average)
    variance = variance / len(df)
    if variance > 1000:
        print(tokens_keyword[i].text, variance)