import sys
sys.path.append("../data/")
import data_processing as d_p
import lda_func as lda
import gensim
import numpy as np
import gensim.downloader as api
from sklearn.cluster import KMeans
from scipy.special import comb 
import string

list_directories = [["shopping", "orders", "purchases", "orders", "receipt", "recipes", "internet", "ebay", "shoes", "amazon"], ["finance", "bank", "trading", "credit", "cards", "banking", "stuff", "bill", "confirmation", "pay"], ["travel", "reservation", "hotel", "train", "ticket", "flights", "info", "confirmation", "air", "airlines"], ["social", "group", "facebook", "friend", "twitter", "myspace", "network", "sites", "follow"], ["career", "job", "application", "recruiter", "search", "resumes", "apps", "hunt"], ["other", "church", "stuff", "soccer", "dating", "match", "school", "education", "jokes", "college", "survey"]]
## Order : Shopping / Finance / Travel / Social / Career / Other

if __name__ == "__main__":
    
    # Parameters #
    nb_topics = 5
    nb_passes = 80
    nb_clusters = 5

    # Get csv #
    filename = "../data/mails_0_50.csv"
    df = d_p.get_pandas_from_csv(filename)
    
    # LDA on text #
    print("Running LDA on text...")
    text_topics, vector_text = lda.apply_lda_text(df['text'], nb_topics=nb_topics, nb_passes=nb_passes)
    print(text_topics)

    print("\n")

    # LDA on subject #
    print("Running LDA on subject...")
    subject_topics, vector_subject = lda.apply_lda_subject(df['subject'], nb_topics=nb_topics, nb_passes=nb_passes)
    print(subject_topics)

    print("\n")

    # Applying clustering #
    print("Running clustering...")
    vectors = np.zeros((len(df['text']), nb_topics*2))
    for i in range(len(df['text'])):
        for j in range(nb_topics):
            vectors[i][j] = vector_text[i][j]
        for j in range(nb_topics):
            vectors[i][nb_topics + j] = vector_subject[i][j]
    clustering = KMeans(n_clusters=nb_clusters).fit(vectors)
    labels = clustering.labels_

    tab_count = []
    matrix_mails = []
    for i in range(nb_clusters):
        count = 0
        list_mails = []
        for j in range(len(labels)):
            if i == labels[j]:
                count += 1
                list_mails.append(df['subject'][j])
        tab_count.append(count)
        matrix_mails.append(list_mails)
    print("Repartition des mails dans les clusters : ", tab_count)

    print('\n')
    
    # Displaying result of clustering #
    for i in range(nb_clusters):
        print("Cluster ", i)
        for elem in matrix_mails[i]:
            print(elem)
        print()


    ## EXPERIMENTAL (optional) ##

    yes_no = input("Do you want to try experimental stuff ? (y/n) : ")
    if yes_no == 'y':
        
        word_vectors = api.load("glove-wiki-gigaword-100")  # load pre-trained word-vectors from gensim-data

        # From categories to most likely directory name #
        for i in range(nb_clusters):
            list_sim = lda.similarity_dir(matrix_mails[i], list_directories, word_vectors)
            list_sim2 = lda.similarity_dir_2(matrix_mails[i], list_directories, word_vectors)
            print("Cluster ", i)
            print(list_sim)
            print(list_sim2)

