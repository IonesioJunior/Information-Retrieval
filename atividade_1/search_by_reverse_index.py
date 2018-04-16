import pandas
import nltk

__author__ = "Ionesio Junior"


def extract_words( text ):
    ''' 
        This method extract match words from all text tables and store in a dictionary correlating with news index
        
        Args:
                text() : table with text to extract words
        Return:
                dict_words( Dict{ String:[Int] } ) : dictionary with words as a keys and a list of news index
    '''
    dict_words = {}
    for i in range(len(text)):
        tokens = nltk.word_tokenize(text[i])
        for j in range(len(token)):
            if( tokens[i] in dict_words.keys() ):
                dict_words[tokens[i]].append( i )
            else:
                dict_words[tokens[i]] = []
    return dict_words

if __name__ == "__main__":
    file_csv = pandas.read_csv("noticias_estadao.csv")
    text = file_csv.titulo + file_csv.conteudo
    match_words = extract_words(text)
