import urllib.request
import pandas

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
dict_text = [line.decode().split('\t') for line in urllib.request.urlopen(req).read().split(b'\n')]
dictionary = pandas.DataFrame(dict_text, columns=["Na'vi", "English", "POS"])


def get_pos(word):
    return dictionary.loc[dictionary["Na'vi"] == word, "POS"].values[0]


def get_row(word):
    return dictionary.index.values[dictionary["Na'vi"] == word]


def main():
    # print(dictionary)
    # print(dictionary[dictionary["Na'vi"] == "taron"])

    while True:
        line = input("Enter Na'vi sentence: ")
        if line in ("q", "quit"):
            break
        words = line.split()
        rows = [get_row(w)[0] for w in words]
        print(rows)
        print(dictionary.iloc[rows, :])


if __name__ == '__main__':
    main()
