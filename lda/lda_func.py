import sys
sys.path.append("../data/")

import data_processing as d_p
import gensim
import numpy as np
import math

def get_vector(tab, nb_topic):
    dic = {}
    for elem in tab:
        dic[elem[0]] = elem[1]

    new_tab = []

    for i in range(nb_topic):
        if i in dic:
            new_tab.append(dic[i])
        else:
            new_tab.append(0)

    return new_tab

def apply_lda_text(elems, nb_topics = 4, nb_passes = 40):
    nb_mails = len(elems)
    list_topics = []
    list_vectors = []

    # Met tous les mails dans une liste de mots par mail : processed_docs #
    processed_docs = []
    for i in range(0, nb_mails):
        processed_tab = d_p.get_full_process(elems[i])
        list_words = d_p.get_only_list_words(processed_tab)
        processed_docs.append(list_words)

    # Lancement de l'algo LDA #
    dictionary = gensim.corpora.Dictionary(processed_docs)
    bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

    lda_model =  gensim.models.LdaMulticore(bow_corpus, num_topics = nb_topics, id2word = dictionary, passes = nb_passes, workers = 2)

    # Affiche tous les topics #
    for i in range(0, nb_topics):
        topic = []
        for elem in lda_model.get_topic_terms(i):
            topic.append(dictionary[elem[0]])
        list_topics.append(topic)

    # Pour chaque mail créé un vecteur avec les % de similarité à chaque topic #
    # Affiche pour chaque mail les % de similarité à chaque topic #
    for i in range(0, nb_mails):
        list_vectors.append(get_vector(lda_model[bow_corpus[i]], nb_topics))

    return list_topics, list_vectors

def apply_lda_subject(elems, nb_topics = 4, nb_passes = 40):
    nb_mails = len(elems)
    list_topics = []
    list_vectors = []

    # Met tous les mails dans une liste de mots par mail : processed_docs #
    processed_docs = []
    for i in range(0, nb_mails):
        processed_tab = d_p.get_full_process_subject(elems[i])
        list_words = d_p.get_only_list_words_subject(processed_tab)
        processed_docs.append(list_words)

    # Lancement de l'algo LDA #
    dictionary = gensim.corpora.Dictionary(processed_docs)
    bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

    lda_model =  gensim.models.LdaMulticore(bow_corpus, num_topics = nb_topics, id2word = dictionary, passes = nb_passes, workers = 2)

    # Affiche tous les topics #
    for i in range(0, nb_topics):
        topic = []
        for elem in lda_model.get_topic_terms(i):
            topic.append(dictionary[elem[0]])
        list_topics.append(topic)

    # Pour chaque mail créé un vecteur avec les % de similarité à chaque topic #
    # Affiche pour chaque mail les % de similarité à chaque topic #
    for i in range(0, nb_mails):
        list_vectors.append(get_vector(lda_model[bow_corpus[i]], nb_topics))

    return list_topics, list_vectors

def list_sub_to_list_words(list_sub):
    list_words = []
    for elem in list_sub:
        if type(elem) != float:
            words = elem.split(' ')
            for word in words:
                list_words.append(word.lower())

    return list_words

def similarity_dir(list_sub, list_dir, word_vectors):
    list_sim = []
    words = list_sub_to_list_words(list_sub)
    for dir_ in list_directories:
        score = 0
        count = 0
        for elem in dir_:
            for word in words:
                try:
                    similarity = word_vectors.similarity(elem, word)
                    score = score + similarity
                    count += 1
                except:
                    pass
        list_sim.append(round(score/count, 3))

    return list_sim

def similarity_dir_2(list_sub, list_dir, word_vectors):
    list_sim = []
    words = list_sub_to_list_words(list_sub)
    for dir_ in list_directories:
        score = 0
        count = 0
        for elem in dir_:
            for word in words:
                try:
                    similarity = word_vectors.similarity(elem, word)
                    if similarity > 0.50:
                        score = score + similarity
                    count += 1
                except:
                    pass
        list_sim.append(round(100*score/count, 3))

    return list_sim




def Jensen_Shannon(P,Q):
        M = 0.5*(P+Q)
        return 1-(math.sqrt(0.5*Kullback_Leibler(P,M)+0.5*Kullback_Leibler(Q,M)))


def Kullback_Leibler(P,Q):
    sum=0
    for i in range(len(P)):

        sum+=P[i]*math.log(P[i]/Q[i],10)
    return sum
