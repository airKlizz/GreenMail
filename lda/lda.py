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
    nb_topics = 10
    nb_passes = 8
    nb_clusters = 10

    # Get csvs #
    filename = ["../data/mails_0_50.csv", 
    "../data/mails_51_100.csv",
    "../data/mails_101_150.csv",
    "../data/mails_151_200.csv",
    "../data/mails_201_250.csv",
    "../data/mails_251_400.csv",
    "../data/mails_401_700.csv"]
    df = d_p.get_pandas_from_csvlist(filename)
    
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
    print("\n\nYOU ENTER THE EXPERIMENTAL AREA\n\n")
    string_test = "What do you want to do ?\n" + "0 : Quit\n" + "1 : Get similarity between clusters and possible directory names\n" + "2 : Try to run LDA but only to get themes for each cluster\n" + "3 : Redisplay mails in a cluster\n" + "Answer : "
    test = input(string_test)
    while(int(test) != 0):
        if int(test) == 1:
            
            word_vectors = api.load("glove-wiki-gigaword-100")  # load pre-trained word-vectors from gensim-data

            # From categories to most likely directory name #
            for i in range(nb_clusters):
                list_sim = lda.similarity_dir(matrix_mails[i], list_directories, word_vectors)
                list_sim2 = lda.similarity_dir_2(matrix_mails[i], list_directories, word_vectors)
                print("Cluster ", i)
                print(list_sim)
                print(list_sim2)
        
        elif int(test) == 2:
            cluster_to_test = input("Which cluster to get themes from LDA ?\n" + "From 0 to " + str(nb_clusters-1) + " : ")
            print("Running LDA on subjects cluster", cluster_to_test, "...")
            topics_0 , vectors_0 = lda.apply_lda_subject(matrix_mails[int(cluster_to_test)], nb_topics=1, nb_passes=3)
            topics_0_ev , vectors_0_ev = lda.apply_lda_subject(matrix_mails[int(cluster_to_test)], nb_topics=1, nb_passes=30)
            print(topics_0)
            print(topics_0_ev)

        elif int(test) == 3:
            cluster_to_test = input("Which cluster to get mails from ?\n" + "From 0 to " + str(nb_clusters-1) + " : ")
            for elem in matrix_mails[int(cluster_to_test)]:
                print(elem)
        
        print()
        test = input(string_test)