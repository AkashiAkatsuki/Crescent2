import MeCab

def tokenize(text):
    mecab = MeCab.Tagger()
    mecab_results = mecab.parse(text).split('\n')[:-2]
    def parse_mecab_result(mecab_result):
        name, descriptions = mecab_result.split('\t')
        category = descriptions.split(',')[0]
        return name, category
    tokens = [parse_mecab_result(m) for m in mecab_results]
    return tokens
