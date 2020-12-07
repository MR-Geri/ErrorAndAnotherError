import nltk
import pandas as pd
import re
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords
import datetime
from gensim.models import Word2Vec


patterns = r"[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
stopwords_ru = stopwords.words("russian")
morph = MorphAnalyzer()


def lemmatize(doc):
    doc = re.sub(patterns, ' ', doc)
    tokens = []
    for token in doc.split():
        if token and token not in stopwords_ru:
            token = token.strip()
            token = morph.normal_forms(token)[0]

            tokens.append(token)
    if len(tokens) > 2:
        return tokens
    return None


def main():
    t = datetime.datetime.now()
    nltk.download('stopwords')
    df_pos = pd.read_csv("../content/positive.csv", sep=";", header=None)
    df_neg = pd.read_csv("../content/negative.csv", sep=";", header=None)
    print(1, datetime.datetime.now() - t)
    df = df_pos.iloc[:, 3].append(df_neg.iloc[:, 3])
    print(2, datetime.datetime.now() - t)
    df = df.dropna().drop_duplicates()
    print(3, datetime.datetime.now() - t)
    data = df.apply(lemmatize)
    print(4, datetime.datetime.now() - t)
    data = data.dropna()
    print(5, datetime.datetime.now() - t)
    w2v_model = Word2Vec(
        min_count=10,
        window=2,
        size=300,
        negative=10,
        alpha=0.03,
        min_alpha=0.0007,
        sample=6e-5,
        sg=1)
    print(6, datetime.datetime.now() - t)
    w2v_model.build_vocab(data)
    print(7, datetime.datetime.now() - t)
    w2v_model.train(data, total_examples=w2v_model.corpus_count, epochs=30, report_delay=1)
    print(8, datetime.datetime.now() - t)
    w2v_model.init_sims(replace=True)
    print(9, datetime.datetime.now() - t)
    #
    w2v_model.wv.most_similar(positive=["любить"])
    w2v_model.wv.most_similar(positive=["мужчина"])
    w2v_model.wv.most_similar(positive=["день", "завтра"])
    w2v_model.wv.most_similar(positive=["папа", "брат"], negative=["мама"])
    w2v_model.wv.most_similar_to_given("хороший", ["приятно", "город", "мальчик"])  # наиболее близкое


if __name__ == '__main__':
    main()
