import pandas

with open("NaviDictionary.tsv", "r") as f:
    dict_text = [line.split('\t') for line in f.read().split('\n')]
dictionary = pandas.DataFrame(dict_text, columns=["Na'vi", "English", "POS"])


class Word:
    def __init__(self, nav, eng, pos):
        self.nav = nav
        self.eng = eng
        self.pos = pos

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
        out += f"\n   -- subject: {self.subj}"
        out += f"\n   -- direct: {self.do}"
        out += f"\n   -- indirect: {self.ido}"
        for a in self.adv:
            out += f"\n   -- adverb: {a}"
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
