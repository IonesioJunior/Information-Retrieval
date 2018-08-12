# Inverted Index Optimizations
Now that we know how to build the inverted index algorithm, we need to go a little deeper and think about how it would work in a real-world environment.First, let's ask some questions.
-   How inverted index works on systems with millions of documents?
    -   _will we return tons of documents that contains these specific words?_  
-   How to know what document is most relevant to some query?
    -   _Many documents can contain query words without any relation to interest_
-   The size of documents have some impact of our queries?
    -   _The probability of a document containing a particular word increases as the number of words in that document grows, do you agree?_
-   How to create a metric for big and small documents?
    - _Can we create an arithmetic expression that can express this relation?_
-   How to penalize repeated words?
    -   _Repeated words should have a low score,  because it tends to be a generic term in any document, do you agree?_
-   How to boost score of words with low frequency?
    -   _We need to boost the score of low frequency words, because they tend to express the intention of the query._
-   How to evaluate my ranking system?
    -   _How do I know if my system is accurate?_
