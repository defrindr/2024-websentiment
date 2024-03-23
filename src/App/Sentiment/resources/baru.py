import nltk
import pandas as pd
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_predict
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import string
import re

from sklearn.model_selection import train_test_split
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from nltk.tokenize import word_tokenize

path = './nr'


class Sentiment:
    df = None
    X_train = None
    X_test = None
    y_train = None
    y_test = None
    stopwords = None
    sastrawiStopword = None
    stemmer = None
    classifier = None
    max_features = None

    def init_app(self, max_features=10000):
        self.max_features = max_features
        self.df = pd.read_csv(f'{path}/training.csv')

        self.load_library()
        self.generate_test()
        self.load_stopwords()

        self.X_train['Judul'] = self.X_train.Judul.apply(self.preprocessing)
        self.init_naive()
        return self

    def init_naive(self):
        # hitung idf
        tfidf = TfidfVectorizer(
            max_features=self.max_features,
            smooth_idf=False,
            ngram_range=(1, 1),
            lowercase=True,
            analyzer='word'
        )

        X_train_tfidf = tfidf.fit_transform(self.X_train['Judul'])
        X_test_tfidf = tfidf.transform(self.X_test['Judul'])

        # implementasi naive bayes
        self.classifier = MultinomialNB(alpha=0.7, fit_prior=False)
        self.classifier.fit(X_train_tfidf, self.y_train)
        y_pred = self.classifier.predict(X_test_tfidf)
        akurasi = accuracy_score(self.y_test, y_pred)
        print('Akurasi:\n', akurasi)

    def load_library(self):
        stopwordFactory = StopWordRemoverFactory()
        self.sastrawiStopword = stopwordFactory.create_stop_word_remover()

        sFactory = StemmerFactory()
        self.stemmer = sFactory.create_stemmer()

    def generate_test(self):
        X = self.df[['Judul']]
        y = self.df[['Kategori']]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=.25, random_state=42)

    def load_stopwords(self):
        file_stopword = open(f"{path}/stopword.txt", "r")  # r = read
        self.stopwords = file_stopword.read().split('\n')
        file_stopword.close()

    def bersihkanDataset(self, teks):
        # casefolding
        # menghapus tab
        # menghapus baris baru
        # menghapus backslash
        teks = teks\
            .lower()\
            .replace('\\t', " ")\
            .replace('\\n', " ")\
            .replace('\\', "")

        # Menghapus karakter khusus
        teks = teks.encode('ascii', 'replace').decode('ascii')
        # menghapus tanda baca
        teks = teks.translate(str.maketrans("", "", string.punctuation))
        # menghapus spasi di awal dan akhir kalimat
        teks = teks.strip()
        # menghapus dobel spasi
        teks = re.sub('\s+', ' ', teks)
        # menghapus karakter tunggal
        teks = re.sub(r"\b[a-z]\b", "", teks)
        # menghapus angka
        teks = re.sub(r"[\d]+", "", teks)
        return teks

    def stem(self, kalimat):
        stop = self.sastrawiStopword.remove(kalimat)
        tokens = nltk.tokenize.word_tokenize(stop)
        clean = [kata for kata in tokens if kata not in self.stopwords]
        kalimat = ' '.join(clean)
        return self.stemmer.stem(kalimat)

    def preprocessing(self, kalimat):
        kalimat = self.bersihkanDataset(kalimat)
        return self.stem(kalimat)


app = Sentiment().init_app()
