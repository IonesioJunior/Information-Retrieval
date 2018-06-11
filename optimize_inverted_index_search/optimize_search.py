#coding: utf-8

import pandas
import nltk
import numpy as np
import ast
from math import log
import re
from unicodedata import normalize

__author__ = "Ionesio Junior"

class Documents(object):
    def __init__(self, index, first_word, tf_first_word):
        self.__index = index
        self.__first_word = first_word
        self.__dict_of_words = { first_word : tf_first_word }

    def get_index(self):
        return self.__index

    def append_new_term(self, word, word_frequency):
        self.__dict_of_words[word] = word_frequency

    def get_term_frequency(self, word=None):
        if word == None:
            self.__dict_of_words[this.__first_word]
        else:
            try:
                return self.__dict_of_words[word]
            except KeyError:
                return 0

    def get_words_dict(self):
        return self.__dict_of_words

    def update(self, other_doc):
        self.__dict_of_words.update(other_doc.get_words_dict())

    def __eq__(self,other):
        return self.__index == other.get_index()

    def __hash__(self):
        return hash(self.__index)


class Corpus(object):
    
    def __init__(self, doc_path):
        file_csv = pandas.read_csv(doc_path, encoding="utf-8")
        file_csv = file_csv.replace(np.nan, '',regex = True)
        self.__corpus_length = len(file_csv.idNoticia)
        text = file_csv.titulo + " " + " " +  file_csv.subTitulo + " " + file_csv.conteudo
        text.apply(lambda x: "" if isinstance(x, float) else self.__text_clear(x).lower())
        self.__match_words = {}
        self.__k = 1.5
        self.__extract_words(text,file_csv.idNoticia)

    def __text_clear(self,text):
        pattern = re.compile('[^a-zA-Z0-9 ]')
        text = normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
        return pattern.sub(' ', text)
        
    def __add_dictionary(self,info_tuple):
        word, index, text = info_tuple
        try:
            self.__match_words[ word.lower() ].add( Documents(index, word.lower(), text.count(word)) )
        except KeyError:
            self.__match_words[ word.lower() ] = set( [ Documents(index, word.lower(), text.count(word))] )

    def __extract_words(self,text , id_col):
        [ map( self.__add_dictionary, [ ( word, id_col[i],text[i] ) for word in nltk.word_tokenize( text[i] ) ] ) for i in xrange( len(text) ) ]

    def __idf(self, word):
        return log( self.__corpus_length + 1 / len(self.__match_words[word]) )

    def __bm25(self, term_frequency):
        return ((self.__k + 1)* term_frequency) / (self.__k + term_frequency)

    def __AND_between_documents(self,x,y):
        new_list = []
        for first_doc in x:
            for second_doc in y:
                if(second_doc == first_doc):
                    first_doc.update(second_doc)
                    new_list.append(first_doc)
        return set(new_list) 

    def search(self,type_of_search, words):
        if ( " " in words ):
            list_of_words = list( set( map( lambda x: ( x.strip().lower(), words.count(x) ), words.split(" ") ) ) )
            results = reduce( lambda x,y : self.__AND_between_documents(x,y) , [ self.__match_words[word[0].lower()] for word in list_of_words ] )
        else:
            results = list( self.__match_words[words] )
        if type_of_search.lower() == "binary":
            return map(lambda x: x.get_index(), results)
        elif type_of_search.lower() == "tf":
            tf_results = [ ( result.get_index(), sum( map(lambda x: x[1] * result.get_words_dict()[x[0]], list_of_words )) ) for result in results ]
            return sorted(tf_results, key=lambda x: x[1],reverse=True)
        elif type_of_search.lower() == "tf-idf":
            tf_idf_results = [ ( result.get_index(), sum( map(lambda x: x[1] * result.get_words_dict()[x[0]] * self.__idf(x[0]), list_of_words )) ) for result in results ]
            return sorted(tf_idf_results, key=lambda x: x[1],reverse=True)
        elif type_of_search.lower() == "bm25":
            bm25_results = [ ( result.get_index(), sum( map(lambda x: x[1] * self.__bm25(result.get_words_dict()[x[0]]) * self.__idf(x[0]), list_of_words )) ) for result in results ]
            return sorted(bm25_results, key=lambda x: x[1],reverse=True)

        
def apk(actual, predicted, k=10):
    """
    Computes the average precision at k.
    This function computes the average prescision at k between two lists of
    items.
    Parameters
    ----------
    actual : list
             A list of elements that are to be predicted (order doesn't matter)
    predicted : list
                A list of predicted elements (order does matter)
    k : int, optional
        The maximum number of predicted elements
    Returns
    -------
    score : double
            The average precision at k over the input lists
    """
    if len(predicted)>k:
        predicted = predicted[:k]

    score = 0.0
    num_hits = 0.0

    for i,p in enumerate(predicted):
        if p in actual and p not in predicted[:i]:
            num_hits += 1.0
            score += num_hits / (i+1.0)

    if not actual:
        return 0.0

    return score / min(len(actual), k)


def mapk(actual, predicted, k=10):
    """
    Computes the mean average precision at k.
    This function computes the mean average prescision at k between two lists
    of lists of items.
    Parameters
    ----------
    actual : list
             A list of lists of elements that are to be predicted 
             (order doesn't matter in the lists)
    predicted : list
                A list of lists of predicted elements
                (order matters in the lists)
    k : int, optional
        The maximum number of predicted elements
    Returns
    -------
    score : double
            The mean average precision at k over the input lists
    """
    return np.mean([apk(a,p,k) for a,p in zip(actual, predicted)])


def main():
    corpus = Corpus("estadao_noticias_eleicao.csv")
    ground_truth = pandas.read_csv("gabarito.csv", encoding="utf-8")

    #Ground Truth results
    google_results = map(lambda x: ast.literal_eval(x), ground_truth.google)
    binary_search_results = map(lambda x: ast.literal_eval(x), ground_truth.busca_binaria)
    tf_results = map(lambda x: ast.literal_eval(x),ground_truth.tf)
    idf_results = map(lambda x: ast.literal_eval(x),ground_truth.tfidf)
    bm25_results = map(lambda x: ast.literal_eval(x),ground_truth.bm25)



    # My algorithms results

    #Binary Results
    binary_results = [ corpus.search("binary", word) for word in ground_truth.str_busca ]
    print ("Result for simple binary search:  %.4f" % mapk(binary_search_results,binary_results, k=5))

    #Term frequency Results
    custom_tf_results = [ map( lambda x: x[0], corpus.search("tf", word) ) for word in ground_truth.str_busca ]
    print ("Result for term frequency search: %.4f" % mapk(tf_results,custom_tf_results,k=5))


    #Term frequency / Inverted document frequency results
    custom_tf_idf_results = [ map( lambda x: x[0], corpus.search("tf-idf", word) ) for word in ground_truth.str_busca ]
    print ("Result for tf / idf search: %.4f" % mapk(idf_results,custom_tf_idf_results,k=5))

    #Term frequency / Inverted document frequency results
    custom_bm25_results = [ map( lambda x: x[0], corpus.search("bm25", word) ) for word in ground_truth.str_busca ]
    print ("Result for bm25 search: %.4f" % mapk(idf_results,custom_bm25_results,k=5))

    print " "
    print "Testing with Google results ..."
    print ("Result for simple binary search:  %.4f" % mapk(google_results,binary_results, k=5))
    print ("Result for term frequency search: %.4f" % mapk(google_results,custom_tf_results,k=5))
    print ("Result for tf / idf search: %.4f" % mapk(google_results,custom_tf_idf_results,k=5))
    print ("Result for bm25 search: %.4f" % mapk(google_results,custom_bm25_results,k=5))

    
if __name__ == "__main__":
    main()