#coding: utf-8

import pandas
import nltk

__author__ = "Ionesio Junior"

# Color consts
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'

match_words = {}


def add_dictionary( info_tuple ):
    '''
        This method fill lists of news index with match words

        Args:
            info_tuple(String, Int) : this tuple contain a specific word and index of news
    '''
    word, index = info_tuple
    try:
        match_words[ word.lower() ].append(index)
    except KeyError:
        match_words[ word.lower() ] = [ index ]


def extract_words( text , id_col ):
    ''' 
        This method extract match words from all text tables and store in a dictionary correlating with news index
        
        Args:
                text() : table with text to extract words
                id_col : table with news index
    '''
    [ map( add_dictionary, [ ( word, id_col[i] ) for word in nltk.word_tokenize( text[i] ) ] ) for i in xrange( len(text) ) ]


def search( words ):
    '''
        This method search a set of words using AND/OR operators to guide how to search

        Args:
                words(String) : string with words to be searched (Ex: word1 AND word2 AND ... | word1 OR word2 OR ... )
        Return:
                index_list[Int] : list of news index that matches with words
    '''
    if ( "AND" in words ):
        list_of_words = map( lambda x: x.strip(), words.split("AND") )
        return reduce( lambda x,y : list( set(x) & set(y) ), [ match_words[word.lower()] for word in list_of_words ]      )
    elif ("OR" in words ):
        list_of_words = map(lambda x: x.strip(), words.split("OR"))
        return reduce( lambda x,y : list( set(x + y) ), [ match_words[word.lower()] for word in list_of_words ] )
    else:
        return match_words[words]

def debug_test(text, expected_value):
	result =  len(search(text)) == expected_value
	if result == True:
		print "Testing \"" + text + "\"... " + OKGREEN + "Sucess!!" + ENDC
	else:
		print "Testing \"" + text + "\"... " + FAIL + "Fail!!" + ENDC
    

def test_search():
    #OR
    debug_test("debate OR presidencial",1770)
    debug_test("presidenciáveis OR corruptos", 164)
    debug_test("Belo OR Horizonte", 331)

    #AND
    debug_test("Belo AND Horizonte", 242)
    debug_test("presidenciáveis AND corruptos", 0)
    debug_test("debate AND presidencial",201)
    debug_test("Campina AND Grande",12)


if __name__ == "__main__":
    file_csv = pandas.read_csv("noticias_estadao.csv")
    text = file_csv.titulo + " " + file_csv.conteudo
    extract_words(text,file_csv.idNoticia)
    test_search()
