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
categories = []
categories.append("shopping orders purchases receipts compras recipes ebay shoes amazon")
categories.append("finance bank trading credit cards financial bankling stuff statements bill confirmations pay")
categories.append("travel hotel reservations train tickets flights airlines reservations info confirmations train")
categories.append("social groups facebook friends twitter myspace social networking network sites")
categories.append("career jobs job recruiters search career resumes hunting")
categories.append("education school course college learn")
categories.append("other church stuff soccer dating jokes surveys")

categories_dict = {}

for l in categories:
    print("\n\n", l, "\n\n")
    categories_dict[l] = {}
    #l = "trading stock volatility"
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

        score = 0
        for tok1 in tokens_keyword:
            if tok1.has_vector:
                for tok2 in tokens_text:
                    if tok2.has_vector:
                        if tok1.similarity(tok2) > MIN_DIST:
                            try:
                                score += (tok1.similarity(tok2) - MIN_DIST)*dict_words[tok2.text]
                            except:
                                print("ERROR with ", tok2.text)
                            #print(tok1.text, tok2.text, tok1.similarity(tok2), dict_words[tok2.text])

        if (score/nb_words)*100 > MIN_ALIKE_WORDS:
            print(score, (score/nb_words)*100, df['2'][i])
            categories_dict[l][i] = (score/nb_words)*100


print(categories_dict)
##categories_dict[categories[0]].pop(33, None)

### AFFINAGE POUR AVOIR UN MAIL SEULEMENT DANS UNE CATEGORIE ###

sorting_dict = {}

for df_id in range(0,len(df)):
    for elem in categories_dict:
        if df_id in categories_dict[elem]:
            if df_id in sorting_dict:
                if sorting_dict[df_id][1] < categories_dict[elem][df_id]:
                    sorting_dict[df_id] = [elem, categories_dict[elem][df_id]]
            else:
                sorting_dict[df_id] = [elem, categories_dict[elem][df_id]]
    if df_id not in sorting_dict:
        sorting_dict[df_id] = ["others", 0]

print(sorting_dict)

### AFFICHAGE RESULAT ###

for elem in sorting_dict:
    print(sorting_dict[elem][0].split()[0], df['2'][elem])
