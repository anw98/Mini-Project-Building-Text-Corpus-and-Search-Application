import json
import re

import googletrans
from googletrans import Translator


# Fill missing valies by ""
def fill_missing(song):
    if "Lyricist" not in song or song["Lyricist"] == "Unknown":
        song['Lyrics'] = ""

    if "Singer" not in song or song["Singer"] == "Unknown":
        song['Singer'] = ""

    if "Music" not in song or song["Music"] == "Unknown":
        song['Music'] = ""

    if "Album" not in song or song["Album"] == "Unknown":
        song['Album'] = ""
    return song


# seperate title content to sonhala and english and extract sinhala title
# def separate_title(song):
#     title = song["title"]
#     for i in title:
#         if i == "–":
#             sep = "–"
#         if i == "|":
#             sep = "|"
#         if i == "-":
#             sep = "-"
#
#     title_list = title.split(sep)
#     title_sinhala = title_list[-1].strip()
#
#     song['title'] = title_sinhala
#     print(song['title'])
#     return song

#
# # clean beat data
# def clean_beat(song):
#     beat = song["beat"]
#     if type(beat) == type([]):
#         song['beat'] = beat[0].strip().split(" ", 1)[1]
#     elif beat == "N/A":
#         song['beat'] = ""
#     return song


# # replace dots in people names by space
# def remove_dots_in_names(song):
#     names = ["Lyricist", "Singer", "Music"]
#     for i in names:
#         field = song[i]
#         if type(field) == type([]):
#             for j in range(len(field)):
#                 field[j] = field[j].replace(".", " ")
#         else:
#             field = field.replace(".", " ")
#         song.update({i: field})
#     return song

#
# clean lyrics corpus
def clean_lyrics(song):
    lyrics = song['Lyrics ']
    lines = lyrics.split("\n")
    final = []
    for i, line in enumerate(lines):
        line = line.strip()
        line = re.sub('[.!?\\-—]', '', line)
        if not line or line.isspace() or '\u200d' in line:
            pass
        else:
            final.append(line)
    song["Lyrics"] = "\n".join(final)
    return song


# translate sinhala artist name, composer name, lyricist name and genre to sinhala
def translate(song):
    translator = Translator()
    fields_to_translate = ["Lyricist", "Singer", "Music", "Album"]
    for i in fields_to_translate:
        song[i] = song[i].split(' ')
        if type(song[i]) == list:
            translated = []
            for j in song[i]:
                j = j.strip()
                print(translator.translate(j, dest='sin'))
                # translated.append(translator.translate(j, dest='si').text)
        else:
            song[i] = song[i].strip()
            translated = translator.translate(song[i], dest='si').text
        song[i] = translated
    return song


def read_all_songs():
    with open('song/metaphors.json', 'r', encoding='utf-8-sig') as f:
        all_songs = json.loads(
            f.read())
        #print(all_songs[0])
        # song_list = []
        # for i in all_songs:
        #     print(i)
        #     song_list.append(list(i))
        #print(all_songs)
        # all_songs = json.loads(f.read())
        # res_list = [i for n, i in enumerate(all_songs) if i not in all_songs[n + 1:]]
        return all_songs


def process():
    all_songs = read_all_songs()
    for i in range(len(all_songs)):
        song = all_songs[i]



        #Fill the fields that are not found in original data with "නොදනී"
        song = fill_missing(song)

        # replace dots in names by space
        #song = remove_dots_in_names(song)


        #translate relevant fields to Sinhala
        # song = translate(song)

        # convert numbers to int
        # song['number_of_visits'] = int(song['number_of_visits'].replace(',', ''))
        # song['number_of_shares'] = int(song['number_of_shares'])

        # clean song lyrics
        song = clean_lyrics(song)


        #write processed data to processed/ directory
        with open('processed/' + str(i) + '.json', 'w') as f:
            json.dump(song, f)

# def test():
#     with open('processed/0.json', 'r', encoding='utf-8-sig') as f:
#         song = json.loads(
#             f.read())
#         print(song)



if __name__ == "__main__":
    process()
