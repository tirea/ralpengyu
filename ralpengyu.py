import urllib.request
import pandas
import word_types


def update():
    site = "http://eanaeltu.learnnavi.org/dicts/NaviDictionary.tsv"
    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/77.0.3865.90 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
    req = urllib.request.Request(site, headers=hdr)
    text = urllib.request.urlopen(req).read()
    with open("NaviDictionaryUpdate.tsv", "w") as f_new:
        f_new.write(text)


with open("NaviDictionary.tsv", "r") as f:
    dict_text = [line.split('\t') for line in f.read().split('\n')]
total_words = len(dict_text)
dictionary = pandas.DataFrame(dict_text, columns=["Na'vi", "English", "POS"])


def get_pos(word):
    return dictionary.loc[dictionary["Na'vi"] == word, "POS"].values[0]


def get_row(word):
    return dictionary.index.values[dictionary["Na'vi"] == word]


def is_base(word, entry):
    if entry == word:
        return True
    if not entry:
        return False
    if word[0] == entry[0]:
        return is_base(word[1:], entry[1:])
    else:
        return is_base(word[1:], entry)


def process(word):
    line = dictionary.loc[dictionary["Na'vi"] == word]
    nav = line["Na'vi"].values[0]
    eng = line["English"].values[0]
    pos = line["POS"].values[0]
    if pos in ("v.", "vin.", "vtr.", "vinm.", "vtrm.", ):
        return word_types.Verb(nav, eng, pos)
    if pos in ("n.", "pn.", ):
        return word_types.Noun(nav, eng, pos)


def clause(words):
    verb = None
    for w in words:
        if type(w) == word_types.Verb:
            verb = w
            break
    if verb is None:
        raise ValueError(f"No verb found in {words}")
    for w in words:
        if type(w) == word_types.Noun:
            verb.do = w
            break
    return verb


def main():
    # print(dictionary)
    # print(dictionary[dictionary["Na'vi"] == "taron"])

    while True:
        line = input("Enter Na'vi sentence: ")
        if line in ("q", "quit"):
            break
        if line in ("update",):
            update()

        words = line.split()

        # rows = [get_row(w)[0] for w in words]
        # print(rows)
        # print(dictionary.iloc[rows, :])

        words = [process(w) for w in words]
        print(clause(words))


if __name__ == '__main__':
    main()
