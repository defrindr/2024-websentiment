import pandas as pd  # untuk pemrosesan file csv
import string  # untuk melakukan tokenisasi
import numpy as np  # untuk memudahkan perhitungan pada array
import re  # untuk membantu proses tokenisasi
import os

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize
from sklearn.naive_bayes import CategoricalNB, MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import App.Models.Dataset as DatasetInstance

from sqlalchemy import create_engine
from App.Core.config import Config
from App.Core.database import db

# Connect to the database
# Replace with your connection string

sFactory = StemmerFactory()
stemmer = sFactory.create_stemmer()

path = os.getcwd() + '/App/Sentiment'

file_stopword = open(path+"/resources/stopword.txt", "r")  # r = read
stopwords = file_stopword.read().split('\n')
file_stopword.close()


class Sentiment():
    tfidf = None
    naiveBaseClassifier = None
    app = None
    engine = None

    def init_app(self, app):
        self.app = app
        with app.app_context():
            self.engine = db.engine
            self.training()

    def cleanupText(self, teks):
        # menghapus tab
        # menghapus baris baru
        # menghapus backslash
        teks = teks\
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
        teks = re.sub(r"\b[a-zA-Z]\b", "", teks)
        # menghapus angka
        teks = re.sub(r"[\d]+", "", teks)
        return teks

    def filtering(self, token):
        clean = [kata for kata in token if kata not in stopwords]
        return clean

    def stem(self, token):
        token = ' '.join(token)
        return stemmer.stem(token)

    def training(self):
        # dataFrame = pd.read_csv(path + '/resources/clean_dataset.csv')
        dataFrame = pd.read_sql(
            """
                SELECT datasets.id, datasets.kategoriId as Kategori, datasets.Stem, datasets.flag 
                FROM datasets 
                WHERE datasets.flag = 1
                """,
            con=self.engine.raw_connection()
        )
        max_features = 10000

        X_train, X_test, y_train, y_test = train_test_split(
            dataFrame['Stem'],
            dataFrame['Kategori'],
            test_size=.3,
            random_state=50
        )

        # hitung idf
        self.tfidf = TfidfVectorizer(
            max_features=max_features,
            smooth_idf=False,
            ngram_range=(1, 3)
        )

        X_train_tfidf = self.tfidf.fit_transform(X_train)
        X_test_tfidf = self.tfidf.transform(X_test)

        # implementasi naive bayes
        self.naiveBaseClassifier = MultinomialNB()
        self.naiveBaseClassifier.fit(X_train_tfidf, y_train)

        y_pred = self.naiveBaseClassifier.predict(X_test_tfidf)

        akurasi = accuracy_score(y_test, y_pred)
        print('Akurasi:\n', akurasi)

        classification_rep = classification_report(y_test, y_pred)
        print('Laporan Klasifikasi:\n', classification_rep)
    pass

    def predict(self, teks):
        teks = self.cleanupText(teks)
        token = teks.split(' ')
        token = self.filtering(token)
        teks = self.stem(token)

        new_text_tfidf = self.tfidf.transform([teks])
        predicted_category = self.naiveBaseClassifier.predict(
            new_text_tfidf
        )[0]
        return predicted_category
    pass


pass
