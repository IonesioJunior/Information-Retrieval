# Inverted Index

### **Overview**
- [How to retrieve a text document by query?](#how-to-retrieve-document-by-query?)
- [What is Inverted Index?](#what-is-inverted-index?)
- [Our Example](#our-example)


##How to retrieve document by query?
<p align="center"><img src = "../resources/query.png" width = "500"></p>
Generally, we need to do some search on the web search services (google / yahoo / etc). To make these queries, we commonly use specific words that represent what we are looking for. But web search services return to us some documents / urls. How they can associate a set of words with complex documents?


Our natural thought concludes: "They search around all of document and verify if queries matches with some slice of document.Obviously!".But if you think about this a little bit, have some problems with this reasoning. How they can make this query in seconds/milliseconds? Search big documents checking every word is computationally expensive.


Fortunately, someone spent some time thinking about this and reached a conclusion. Our Inverted Index algorithm!

## What is Inverted Index?
Inverted index is a classic algorithm used to create a relation between documents and word/phrases queries.



## Our Example
