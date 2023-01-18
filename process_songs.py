import json
import re

import googletrans
from googletrans import Translator


# Fill missing valies by ""
def fill_missing(song):
    if "Lyricist" not in song or song["Lyricist"] == "Unknown":
        song['Lyricist'] = "නොදනී"

    if "Singer" not in song or song["Singer"] == "Unknown":
        song['Singer'] = "නොදනී"

    if "Music" not in song or song["Music"] == "Unknown":
        song['Music'] = "නොදනී"

    if "Album" not in song or song["Album"] == "Unknown":
        song['Album'] = "නොදනී"
    return song

# clean lyrics corpus
def clean_lyrics(song):
    lyrics = song['Lyrics']
    # print(lyrics)
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
                translated.append(translator.translate(j, dest='sinhala').text)
        else:
            song[i] = song[i].strip()
            translated = translator.translate(song[i], dest='sinhala').text
        song[i] = translated
    return song


def read_all_songs():
    with open('song/metaphors.json', 'r', encoding='utf-8-sig') as f:
        all_songs = json.loads(
            f.read())
        return all_songs


def process():
    all_songs = read_all_songs()
    for i in range(len(all_songs)):
        song = all_songs[i]

        # Fill the fields that are not found in original data with "නොදනී"
        song = fill_missing(song)

        # clean song lyrics
        song = clean_lyrics(song)
        print(song)
        # write processed data to processed/ directory
        with open('processed/' + str(i) + '.json', 'w') as f:
            json.dump(song, f)


# def test():
#     with open('processed/0.json', 'r', encoding='utf-8-sig') as f:
#         song = json.loads(
#             f.read())
#         print(song)


if __name__ == "__main__":
    process()
