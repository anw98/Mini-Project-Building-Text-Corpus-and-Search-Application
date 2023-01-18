import re


def process_search_query(query):
    possible_keywords = {}
    possible_keywords["Singer"] = ['ගායකයා', 'ගයනවා', 'ගායනා', 'ගැයු', 'ගයන', 'ගයපු', 'කියපු', 'කියන']
    possible_keywords["Lyricist"] = ['පද', 'රචනය', 'රචකයා', 'ලියන', 'ලීව', 'රචිත', 'ලියපු', 'ලිව්‌ව', 'රචනා', 'රචක',
                                     'ලියපු']
    possible_keywords["Music"] = ['සංගීත', 'තනු', 'තනුව', 'සංගීතය', 'සංගීතවත්']
    possible_keywords["qualitative"] = ['හොදම', 'හොඳම', 'ජනප්‍රිය', 'ප්‍රචලිත', 'ප්‍රසිද්ධ', 'ජනප්‍රියම',
                                        'ප්‍රචලිතම' 'ප්‍රචලිතම']
    possible_keywords["Target"] = ['රූපක','රූපකයන්', 'උපමා', 'උපමාවන්']
    possible_keywords["Year"] = ['වර්ෂය', 'වර්ෂයේ', 'අවුරුද්දේ', 'අවුරුද්ද']

    tokens = query.strip().split(" ")

    frequent_words = ['ගීත', 'සින්දු', 'ගී', 'ගීය', 'ගීතය', 'සින්දුව']
    # Drop more frequent words from token list
    for i in frequent_words:
        if i in tokens:
            tokens.remove(i)
    print("tokens", tokens)

    boosts = {"Title": 1,
              "Lyrics": 1,
              "Lyricist": 1,
              "Singer": 1,
              "Music": 1,
              "Album": 1,
              'Year': 1,
              'Metaphor': 1,
              'Interpretation': 1,
              'Source': 1,
              'Target': 1,
              'Interpretation':1}


    # increment boosts if keywords related to the field is in tokens
    for token in tokens:
        for field in possible_keywords.keys():
            if token in possible_keywords[field]:
                boosts[field] = 4

    # check if beat pattern is present
    for token in tokens:
        if bool(re.search(r'\d/\d', token)) or bool(re.search(r'\d-\d', token)):
            boosts['beat'] += 1

    boosted_title = "Title^{}".format(boosts["Title"])
    boosted_lyrics = "Lyrics^{}".format(boosts["Lyrics"])
    boosted_lyricist = "Lyricist^{}".format(boosts["Lyricist"])
    boosted_singer = "Singer^{}".format(boosts["Singer"])
    boosted_music = "Music^{}".format(boosts["Music"])
    boosted_album = "Album^{}".format(boosts["Album"])
    boosted_year = "Year^{}".format(boosts["Year"])
    boosted_metaphor = "Metaphor^{}".format(boosts["Metaphor"])
    boosted_source = "Source^{}".format(boosts["Source"])
    boosted_target = "Target^{}".format(boosts["Target"])
    boosted_meaning = "Interpretation^{}".format(boosts["Interpretation"])

    boost_fields = [
        boosted_title,
        boosted_lyrics,
        boosted_lyricist,
        boosted_singer,
        boosted_music,
        boosted_album,
        boosted_year,
        boosted_metaphor,
        boosted_source,
        boosted_target,
        boosted_meaning
    ]

    processed_query = " ".join(tokens)
    print("Processed query :", processed_query)
    print("Boosted fields :", boost_fields)


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
            "Lyricist": {
                "terms": {
                    "field": "Lyricist.keyword",
                    "size": 10
                }
            },
            "Singer": {
                "terms": {
                    "field": "Singer.keyword",
                    "size": 10
                }
            },
            "Music": {
                "terms": {
                    "field": "Music.keyword",
                    "size": 10
                }
            },
            "Lyrics": {
                "terms": {
                    "field": "Lyrics.keyword",
                    "size": 10
                }
            },
            "Metaphor": {
                "terms": {
                    "field": "Metaphor.keyword",
                    "size": 10
                }
            },
            "Target": {
                "terms": {
                    "field": "Target.keyword",
                    "size": 10
                }
            },
            "Interpretation": {
                "terms": {
                    "field": "Interpretation.keyword",
                    "size": 10
                }
            }
        }
    }
    return body
