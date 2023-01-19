# Sinhala Song Metaphors Search Engine

This project is to create a search engine that is capable of searching Sinhala songs that contain metaphors using Sinhala text.

## Prerequisites
Python 3.11

ElasticSearch v7.8.0

Kibana v7.8.0 (Optional)

Flask 2.1.0

## How to Set up

1.Start Elasticsearch

2.Create the index by running mapping.py

3.Start search engine app by running app.py

## Used Techniques

1. ICU_tokenizer - This tokenizer is best for the text from Unicode languages. ICU tokenizer is used for document tokenizing(indexing time).
       

2. Standard Tokenizer
     

3. The standard tokenizer is used during query tokenizing.
            

4. Stop word filtering
         

5. Resistant to simple spelling errors.
       

6. Character filters

## Advanced Features
1. Boosting queries - The system is boosting queries with Elasticsearch boost. The individual fields are set with higher weights after identifying the contexts.
               

2. Facet queries - The search engine supported faceted search related to singer, music, lyricist, year, and target.

