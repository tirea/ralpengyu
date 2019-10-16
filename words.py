import pandas

with open("NaviDictionary.tsv", "r") as f:
    dict_text = [line.split('\t') for line in f.read().split('\n')]
dictionary = pandas.DataFrame(dict_text, columns=["Na'vi", "English", "POS"])


class Word:
    def __init__(self, word):
        self.nav = word
        self.eng = None
        self.pos = None

    def __str__(self):
        return self.nav


class Verb(Word):
    def __init__(self, nav, eng, pos):
        super().__init__(nav, eng, pos)
        self.subj = None
        self.do = None
        self.ido = None
        self.adv = []

    def __str__(self):
        out = super().__str__()
        out += f"   -- subject: {self.subj}"
        out += f"   -- direct: {self.do}"
        out += f"   -- indirect: {self.ido}"
        for a in self.adv:
            out += f"   -- adverb: {a}"
        return out


class Noun(Word):
    def __init__(self, nav, eng, pos):
        super().__init__(nav, eng, pos)
        self.adj = []

    def __str__(self):
        out = super().__str__()
        for a in self.adj:
            out += f"   -- adverb: {a}"
        return out
