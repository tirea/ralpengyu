import urllib.request
import pandas


def get_dictionary():
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
    text = [line.decode().split('\t') for line in urllib.request.urlopen(req).read().split(b'\n')]
    return pandas.DataFrame(text, columns=["Na'vi", "English", "POS"])


def main():
    dictionary = get_dictionary()
    print(dictionary)

    while True:
        line = input("Enter Na'vi sentence: ")
        if line in ("q", "quit"):
            break
        words = line.split()


if __name__ == '__main__':
    main()
