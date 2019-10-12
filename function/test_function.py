import function

for i in range(200001):
    function.progbar(i, 200000, 10)

print()

words_embedding, words_dict = function.get_dict_from_words(['dad', 'mum', 'son', 'daugther', 'calizzano'])

print()

labels = function.apply_clustering('KMeans', 2, words_embedding, dimension_reduction=True, reduction_dim=4)

print()

words_from_cluster = function.get_cluster_word(labels, 0, words_dict)

print(words_from_cluster)
