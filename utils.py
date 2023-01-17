import json

from elasticsearch import Elasticsearch, helpers

es_client = Elasticsearch(HOST="http://localhost", PORT=9200, http_auth=('elastic', 'cFGPaJgzB7iK9GRW_xgZ'))
INDEX = 'songs'



# define mappings and configs

configs = {
    "settings": {
        "index": {
            "number_of_shards": 1,
            "number_of_replicas": 1
        },
        "analysis": {
            "analyzer": {
                "sinhala-ngram": {
                    "type": "custom",
                    "tokenizer": "icu_tokenizer",
                    "char_filter": ["punc_char_filter"],
                    "token_filter": [
                        "edge_n_gram_filter"
                    ]
                },
                "sinhala": {
                    "type": "custom",
                    "tokenizer": "icu_tokenizer",
                    "char_filter": ["punc_char_filter"]
                },
                "english":{
                    "type": "custom",
                    "tokenizer": "classic",
                    "char_filter": ["punc_char_filter"],
                },
                "sinhala-search": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "char_filter": ["punc_char_filter"]
                },
            },
            "char_filter": {
                "punc_char_filter": {
                    "type": "mapping",
                    "mappings": [".=>", "|=>", "-=>", "_=>", "'=>", "/=>", ",=>", "?=>"]
                }
            },
            "token_filter": {
                "edge_n_gram_filter": {
                    "type": "edge_ngram",
                    "min_gram": "2",
                    "max_gram": "20",
                    "side": "front"
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "id": {
                "type": "long"
            },
            "Song Title": {
                "type": "text",
                "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        },
                },
                "analyzer": "sinhala-ngram",
                "search_analyzer": "sinhala-search"
            },
            "Lyrics ": {
                "type": "text",
                "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        },
                },
                "analyzer": "sinhala-ngram",
                "search_analyzer": "sinhala-search"
            },
            "Lyricist": {
                "type": "text",
                "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        },
                },
                "analyzer": "sinhala-ngram",
                "search_analyzer": "sinhala-search"
            },
            "Singer": {
                "type": "text",
                "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        },
                },
                "analyzer": "sinhala-ngram",
                "search_analyzer": "sinhala-search"
            },
            "Music": {
                "type": "text",
                "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        },
                },
                "analyzer": "sinhala-ngram",
                "search_analyzer": "sinhala-search"
            },
            "Album": {
                "type": "text",
                "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        },
                },
                "analyzer": "sinhala-ngram",
                "search_analyzer": "sinhala-search"
            },
            "Year": {
                "type": "text",
                "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        },
                },
            },
            "Metaphor": {
                "type": "text",
                "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        },
                },
                "analyzer": "sinhala",
                "search_analyzer": "sinhala-search"
            },
            "Interpretation": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    },
                },
                "analyzer": "sinhala",
                "search_analyzer": "sinhala-search"
            },
            " Source domain": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    },
                },
                "analyzer": "sinhala",
                "search_analyzer": "sinhala-search"
            },
            " Target domain": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    },
                },
                "analyzer": "sinhala",
                "search_analyzer": "sinhala-search"
            },
            # "number_of_visits": {
            #     "type": "long"
            # },
            # "number_of_shares": {
            #     "type": "long"
            # }
        }
    }
}

def index():
    # res = es_client.indices.create(index=INDEX, body=configs)
    # print(res)

    helpers.bulk(es_client, create_bulk())
    # print(res)


def create_bulk():
    for i in range(128):
        with open("processed/" + str(i) + ".json") as json_file:
            json_data = json.load(json_file)
        print(json_data)
        yield {
            "_index": INDEX,
            "_source": {
                "Song Title": json_data['Song Title'],
                "Lyrics ": json_data['Lyrics '],
                "Lyricist": json_data['Lyricist'],
                "Singer": json_data['Singer'],
                "Music": json_data['Music'],
                "Album": json_data['Album'],
                "Year": json_data['Year'],
                "Metaphor": json_data['Metaphor'],
                "Interpretation": json_data['Interpretation'],
                " Source domain": json_data[' Source domain'],
                " Target domain": json_data[' Target domain'],
            },
        }


# Call elasticsearch bulk API to create the index
if __name__ == "__main__":
    index()
