#coding: utf-8

import pandas
import nltk
from math import log

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
        file_csv = pandas.read_csv(doc_path)
        self.__corpus_length = len(file_csv.idNoticia)
        text = file_csv.titulo + " " + file_csv.conteudo
        self.__match_words = {}
        self.__k = 21
        self.__extract_words(text,file_csv.idNoticia)

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

if __name__ == "__main__":
    corpus = Corpus("noticias_estadao.csv")
    print corpus.search("binary", "Belo Horizonte")[:5]
    print corpus.search("tf","Belo Horizonte")[:5]
    print corpus.search("tf-idf","Belo Horizonte")[:5]
    print corpus.search("bm25","Belo Horizonte")[:5]
