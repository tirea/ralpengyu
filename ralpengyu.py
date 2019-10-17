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
    print(text)
    with open("NaviDictionaryUpdate.tsv", "w") as f_new:
        f_new.write(text.decode())


with open("NaviDictionaryUpdate.tsv", "r") as f:
    dict_text = [line.split('\t') for line in f.read().split('\n')]
total_words = len(dict_text)
dictionary = pandas.DataFrame(dict_text, columns=["Na'vi", "English", "POS"])

suffixes = {
    "t", "it", "ti",
    "l", "ìl",
    "r", "ur", "ru",
}


def affix_split(word, base):
    if not base:
        return []
    affixes = word.split(base)
    out = [base]
    for a in affixes:
        if not a:
            continue
        elif a in suffixes:
            out.append(a)
        else:
            return []
    return out


def process(word):
    breakdown = [word]
    line = None
    for row in range(total_words):
        # print(dictionary["Na'vi"].values[row])
        breakdown = affix_split(word, dictionary["Na'vi"].values[row])
        if breakdown:
            line = dictionary.iloc[row]
            break
    if line is None:
        raise ValueError(f"Could not process {word}")
    nav = line["Na'vi"]
    eng = line["English"]
    pos = line["POS"]
    print(breakdown)
    if pos in {"v.", "vin.", "vtr.", "vinm.", "vtrm.", }:
        return word_types.Verb(nav, eng, pos)
    if pos in {"n.", "pn.", }:
        if len(breakdown) <= 1:
            return word_types.Noun(nav, eng, pos, "")
        else:
            return word_types.Noun(nav, eng, pos, breakdown[1])


def clause(words):
    verb = None
    for w in words:
        if type(w) == word_types.Verb:
            verb = w
            break
    words.remove(verb)
    if verb is None:
        raise ValueError(f"No verb found in {words}")
    for w in words:
        if type(w) == word_types.Noun:
            if (w.case in {"l", "ìl", } and verb.vtr) or (not w.case and not verb.vtr):
                verb.subj = w
            if w.case in {"t", "it", "ti", } and verb.vtr:
                verb.do = w
            if w.case in {"r", "ur", "ru", }:
                verb.ido = w
            else:
                raise ValueError(f"Could not account for {w}")
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
            continue

        words = line.split()

        # rows = [get_row(w)[0] for w in words]
        # print(rows)
        # print(dictionary.iloc[rows, :])

        words = [process(w) for w in words]
        print(clause(words))


if __name__ == '__main__':
    main()
