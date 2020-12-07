import nltk
import pandas as pd
import re
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords
import datetime


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
    df = df_pos.iloc[:, 3].append(df_neg.iloc[:, 3])
    df = df.dropna().drop_duplicates()
    data = df.apply(lemmatize)
    data = data.dropna()
    print(data)
    print(datetime.datetime.now() - t)


if __name__ == '__main__':
    main()
