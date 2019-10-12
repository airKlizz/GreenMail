import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.cluster import AffinityPropagation

def progbar(curr, total, full_progbar):
    # Input :
    # curr : the current step
    # total : the number of steps
    # full_progbar: the number of interval
    #
    # Display a progress bar

    frac = curr/total
    filled_progbar = round(frac*full_progbar)
    print('\r', '#'*filled_progbar + '-'*(full_progbar-filled_progbar), '[{:>7.2%}]'.format(frac), end='')

def get_dict_from_words(words):
    # Input :
    # words : a list of words which we want obtain the embedding from the glove file.
    # Output :
    # words_embedding : a np array which contains on each row the embedding array of a word
    # words_dict : a dict that matches a word with its index in words_embedding
    #
    # Allow to have the embedding of words

    wordset = set()
    for word in words:
        wordset.add(word)

    embedding_dim = 300
    words_dict = dict()
    words_embedding = []
    index = 1
    words_dict['$EOF$'] = 0
    words_embedding.append(np.zeros(embedding_dim))

    embedding_file_path = 'glove.840B.300d.txt'
    embedding_file_length = 2200000
    with open(embedding_file_path, 'r',encoding="utf-8") as f:
        curr = 0
        for line in f:
            progbar(curr, embedding_file_length, 20)
            curr += 1
            l = line.strip().split()
            if len(l) != 301:
                continue
            line = line.strip().split()
            if line[0] not in wordset: continue
            embedding = np.array([float(s) for s in line[1:]])
            words_embedding.append(embedding)
            words_dict[line[0]] = index
            index +=1

    for word in wordset:
        if word not in words_dict:
            words_embedding.append(np.random.rand(300))
            words_dict[word] = index
            index +=1

    return words_embedding, words_dict

def apply_clustering(name_clustering, nb_cluster, data, dimension_reduction=False, reduction_dim=None):
    # Input :
    # name_clustering : the name of the clustering method used ('KMeans' or 'AffinityPropagation')
    # nb_cluster : the number of cluster wanted. None if the clustering method doesn't need number of cluster
    # data : the data to cluster. np array of dimension (nb_data, data_dimension)
    # dimension_reduction : Boolean to do a dimension reduction before clustering.
    # reduction_dim : if dimension_reduction is True, data_dimension after dimension_reduction
    # Output :
    # labels : a np array of dimension (nb_data, 1) that contains the label of each data.
    #
    # Clustering a set a N dimension points using different methods.

    if dimension_reduction:
        pcaN = PCA(n_components=reduction_dim)
        pcaN_result = pcaN.fit_transform(data)

    if name_clustering == 'KMeans':
        kmeans = KMeans(n_clusters=nb_cluster, random_state=0).fit(pcaN_result)
        return kmeans.labels_

    elif name_clustering == 'AffinityPropagation':
        af = AffinityPropagation().fit(pcaN_result)
        return af.labels_

    else :
        print('Wrong name_clustering. Please use \'KMeans\' or \'AffinityPropagation\'')

    return None

def get_cluster_word(labels, num_cluster, words_dict):
    # Input :
    # labels : the labels after clustering
    # num_cluster : the number of the cluster that you want
    # words_dict : a dict that matches a word with its index in words_embedding
    # Output :
    # words_from_cluster : a list of all words with the label num_cluster
    #
    # Obtain the words with the same label num_cluster

    idx_to_words = dict()
    for word, idx in words_dict.items():
        idx_to_words[idx] = word

    words_from_cluster = []

    for i, label in enumerate(labels):
        if label == num_cluster:
            words_from_cluster.append(idx_to_words[i])

    return words_from_cluster

def get_cluster_mail(labels, num_cluster, df_mail):
    return df_mail_from_cluster
