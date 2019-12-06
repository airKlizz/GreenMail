import numpy as np
import pandas as pd
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import KMeans
import random as rd
from scipy import spatial
from sklearn.cluster import KMeans
import scipy.spatial.distance as ssd
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt




def sum_distance(distance_mat,i,Y):
    """Compute the sum of distance from the point i  to all the point of the cluster
        i : index of the point
        Y : list of the index of thes point in the cluster
                                                            """
    sum=0
    for j in Y:
        sum+=distance_mat[i][j]
    return sum


def kmeans(Distance_mat,K,n_iter):
    m = Distance_mat.shape[0] #number of mails
    #Step 1: Initialize the centroids randomly from the data points
    Centroids = []
    rd.seed(400)
    for i in range(K):
        rand = rd.randint(0,m-1)
        if rand not in Centroids:
            Centroids.append(rand)
    #Step 2.a:  For each training example compute the euclidian distance from the centroid and assign the cluster based on the minimal distance
                #We find the euclidian distance from each point to all the centroids and store in a m x K matrix.
                #So every row in Distance matrix will have distances of that particular data point from all the centroids.
                #Next, we shall find the minimum distance and store the index of the column in a vector C
    Distance=np.zeros((m,K))
    for i in range(m):
        for k in range(K):
            Distance[i][k] = Distance_mat[i][Centroids[k]]
    C=np.argmin(Distance,axis=1)+1

    #Step 2.b: We need to regroup the data points based on the cluster index C and store in the Output dictionary and also compute the mean of separated clusters and assign it as new centroids.
    #          Y is a temporary dictionary which stores the solution for one particular iteration
    Y={}
    for k in range(K):
        Y[k+1]=[]
    for i in range(m):
        Y[C[i]].append(i)
    #Pour calculer le nouveau barycentre, nous ne pouvons pas utiliser les coordonnées.
    #Nous allons, pour chaque cluster, prendre le point qui minimise la somme des distance à ce point
    Centroids=[]
    for key,value in Y.items():
        min =sum_distance(Distance_mat,value[0],value)
        point = value[0]
        for point in value:
            sum = sum_distance(Distance_mat,point,value)
            if sum<min:
                #min=point
                min=sum
        #Centroids.append(min)
        Centroids.append(point)
    #Now we need to repeat step 2 till convergence is achieved. In other words, we loop over n_iter and repeat the step 2.a and 2.b as shown
    for i in range(n_iter):
        #step 2.a
        Distance=np.zeros((m,K))
        for i in range(m):
            for k in range(K):
                Distance[i][k] = Distance_mat[i][Centroids[k]]
        C2=np.argmin(Distance,axis=1)+1
        #step 2.b
        Y={}
        for k in range(K):
            Y[k+1]=[]
        for i in range(m):
            Y[C2[i]].append(i)
        Centroids=[]
        for key,value in Y.items():
            min =sum_distance(Distance_mat,value[0],value)
            for point in value:
                sum = sum_distance(Distance_mat,point,value)
                if sum<min:
                    min=sum
            Centroids.append(point)
        Output=Y
    return Output,Centroids

def output_kmean_to_list(Output,number_of_mail):
    """Methods to convert the output of the kmeans algo to a list
    Input : a dict of the form {1:[0,2,...], 2:[43,22,5,....]?3:{21,32,25,..},...}
            With the index of cluster as key and list of (index) of the mails whiche belong to the cluster as value
    Output : A list of the form [0,2,2,3,1,2,3,4,5,....] of the cluster associate to each mail"""

    list_clustering=[1]*number_of_mail  #output of the function
    for index_cluster,list_mail in Output.items():
        for mail in list_mail:
            list_clustering[mail] = index_cluster

    return list_clustering


# display the heat map labelled
def heat_map(similarity_matrix, labels):
	fig, ax = plt.subplots()
	im = ax.imshow(similarity_matrix, cmap='YlOrRd', vmin=0, vmax=1)
	ax.set_xticks(np.arange(len(labels)))
	ax.set_yticks(np.arange(len(labels)))
	ax.set_xticklabels(labels)
	ax.set_yticklabels(labels)
	plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
	fig.tight_layout()
	plt.show()

# display the dendogram created from the similarity matrix
# hyperparameters : you can change the linkage method
def display_dendrogram(similarity_matrix, labels, method='weighted'):
	distVec = ssd.squareform(similarity_matrix)
	link = linkage(y=(1 - distVec), method=method)
	link[link < 0] = 0
	dendro  = dendrogram(link, labels=labels)
	plt.show()

# return an array of size len(similarity_matrix) where the value is the cluster of the mail
# this version of kmeans takes the similarity vector of each mail as a point and apply kmeans on it
# /!!\ priori not the most efficient
def basic_kmeans(similarity_matrix):
	copy_similarity_matrix = similarity_matrix.copy()
	np.fill_diagonal(copy_similarity_matrix, 1)
	return KMeans(n_clusters=4, init='k-means++').fit_predict(copy_similarity_matrix)
