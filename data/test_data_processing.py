import data_processing as d_p

if __name__ == "__main__":
    filename = input("filename csv = ")

    df = d_p.get_pandas_from_csv(filename)

    # Data processing of text #

    text = df['text'][0]
    text = text[1:-1]
    tab = d_p.get_sentences_from_text_df(text)
    tab_no_short_words = d_p.no_short_words(tab, 3)
    tab_lemmatize = d_p.lemmatize_tab(tab_no_short_words)
    tab_no_stopwords = d_p.delete_stopwords_tab(tab_lemmatize)
    tab_stemmed = d_p.stemmed_tab(tab_no_stopwords)
    tab_no_number = d_p.no_number_tab(tab_stemmed)

    print("\nTEXT_FROM_CSV : \n", text)
    print("\nTAB : \n", tab)
    print("\nTAB_NO_SHORT_WORDS : \n", tab_no_short_words)
    print("\nTAB_LEMMATIZE : \n", tab_lemmatize)
    print("\nTAB_NO_STOPWORDS : \n", tab_no_stopwords)
    print("\nTAB_STEMMED : \n", tab_stemmed)
    print("\nTAB_NO_NUMBER : \n", tab_no_number)

    text = df['text'][0]
    tab_full_process = d_p.get_full_process(text)
    print("\nTAB_FULL_PROCESS (equivalent): \n", tab_full_process)

    # Data processing of urls #

    urls = df['urls'][1]
    tab_urls = d_p.get_urls(urls)
    print("\nTAB_URLS : \n", tab_urls)