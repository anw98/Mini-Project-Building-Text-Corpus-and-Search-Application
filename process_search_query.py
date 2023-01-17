import re


def process_search_query(query):
    possible_keywords = {}
    possible_keywords["Lyricist"] = ['ගායකයා', 'ගයනවා', 'ගායනා', 'ගැයු', 'ගයන', 'ගයපු', 'කියපු', 'කියන']
    possible_keywords["lyrics "] = ['පද', 'රචනය', 'රචකයා', 'ලියන', 'ලීව', 'රචිත', 'ලියපු', 'ලිව්‌ව', 'රචනා', 'රචක',
                                   'ලියපු']
    possible_keywords["Music"] = ['සංගීත', 'තනු', 'තනුව', 'සංගීතය', 'සංගීතවත්']
    possible_keywords["qualitative"] = ['හොදම'  'හොඳම', 'ජනප්‍රිය', 'ප්‍රචලිත', 'ප්‍රසිද්ධ', 'ජනප්‍රියම',
                                      'ප්‍රචලිතම' 'ප්‍රචලිතම']
    # possible_keywords["qualitative"] = []
    # possible_keywords["qualitative"] = []
    # possible_keywords["qualitative"] = []

    tokens = query.strip().split(" ")

    frequent_words = ['ගීත', 'සින්දු', 'ගී', 'ගීය', 'ගීතය', 'සින්දුව']
    # Drop more frequent words from token list
    for i in frequent_words:
        if i in tokens:
            tokens.remove(i)
    print("tokens", tokens)

    boosts = {"title": 2, "artist": 1, "lyrics": 1, "music": 1, "genre": 1, "guitar_key": 1, 'beat': 1,
              'number_of_visits': 1, 'number_of_shares': 1, 'song_lyrics': 2}

    # increment boosts if keywords related to the field is in tokens
    for token in tokens:
        for field in possible_keywords.keys():
            if token in possible_keywords[field]:
                boosts[field] = 4

    # check if beat pattern is present
    for token in tokens:
        if bool(re.search(r'\d/\d', token)) or bool(re.search(r'\d-\d', token)):
            boosts['beat'] += 1

    boosted_title = "title^{}".format(boosts["title"])
    boosted_artist = "artist^{}".format(boosts["artist"])
    boosted_lyrics = "lyrics^{}".format(boosts["lyrics"])
    boosted_music = "music^{}".format(boosts["music"])
    boosted_genre = "genre^{}".format(boosts["genre"])
    boosted_guitar_key = "guitar_key^{}".format(boosts["guitar_key"])
    boosted_beat = "beat^{}".format(boosts["beat"])
    boosted_song_lyrics = "song_lyrics^{}".format(boosts["song_lyrics"])

    boost_fields = [
        boosted_title,
        boosted_artist,
        boosted_lyrics,
        boosted_music,
        boosted_genre,
        boosted_guitar_key,
        boosted_beat,
        boosted_song_lyrics
    ]

    processed_query = " ".join(tokens)
    print("Processed query :", processed_query)
    print("Boosted fields :", boost_fields)

    # check for qualitative tokens and numbers to do a range query
    range_query = False
    number_token = False
    for token in tokens:
        if token in possible_keywords["qualitative"]:
            range_query = True
        elif token.isdigit():
            number_token = True
            requested_number = int(token)

    # Execute sorted range multi search query based on number_of_views
    if range_query:
        if not number_token:
            requested_number = 10
        print("Range query using :", processed_query, "upto : ", requested_number, "results.")
        body = {
            "size": requested_number,
            "sort": [
                {"number_of_visits": {"order": "desc"}},
            ],
            "query": {
                "multi_match": {
                    "query": processed_query,
                    "fields": boost_fields,
                    "operator": 'or',
                    "type": "best_fields",
                    "fuzziness": "AUTO"
                }
            },
            "aggs": {
                "Genre": {
                    "terms": {
                        "field": "genre.keyword",
                        "size": 10
                    }
                },
                "Music": {
                    "terms": {
                        "field": "music.keyword",
                        "size": 10
                    }
                },
                "Artist": {
                    "terms": {
                        "field": "artist.keyword",
                        "size": 10
                    }
                },
                "Lyricist": {
                    "terms": {
                        "field": "lyrics.keyword",
                        "size": 10
                    }
                },
                "Beat": {
                    "terms": {
                        "field": "beat.keyword",
                        "size": 10
                    }
                },
                "Guitar Key": {
                    "terms": {
                        "field": "guitar_key.keyword",
                        "size": 10
                    }
                }
            }
        }
        return body

    # Execute normal multi search query
    else:
        print("Normal multi search query from :", processed_query)
        body = {
            "query": {
                "multi_match": {
                    "query": processed_query,
                    "fields": boost_fields,
                    "operator": 'or',
                    "type": "best_fields",
                    "fuzziness": "AUTO"
                }
            },
            "aggs": {
                "Genre": {
                    "terms": {
                        "field": "genre.keyword",
                        "size": 10
                    }
                },
                "Music": {
                    "terms": {
                        "field": "music.keyword",
                        "size": 10
                    }
                },
                "Artist": {
                    "terms": {
                        "field": "artist.keyword",
                        "size": 10
                    }
                },
                "Lyricist": {
                    "terms": {
                        "field": "lyrics.keyword",
                        "size": 10
                    }
                },
                "Beat": {
                    "terms": {
                        "field": "beat.keyword",
                        "size": 10
                    }
                },
                "Guitar Key": {
                    "terms": {
                        "field": "guitar_key.keyword",
                        "size": 10
                    }
                }
            }
        }
        return body
