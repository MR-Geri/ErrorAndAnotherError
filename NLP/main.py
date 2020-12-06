import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import pymorphy2
from tensorflow.keras.datasets import imdb


def main():
    # nltk.download('punkt')
    # nltk.download('stopwords')
    morph = pymorphy2.MorphAnalyzer()
    text = "Я - к.т.н, т.е. проучился долгое время. Имею образование."
    print(sent_tokenize(text, language="russian"))
    print(morph.parse("хочу"))


if __name__ == '__main__':
    main()
