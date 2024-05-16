from App.Core.database import db
from App.Core.config import Config
from sqlalchemy import create_engine
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
import string
import os
import re
import csv
import time

from sklearn.model_selection import train_test_split
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from nltk.tokenize import word_tokenize

path = '/resources'


sFactory = StemmerFactory()
sWordFactory = StopWordRemoverFactory()
stemmer = sFactory.create_stemmer()
stopword = sWordFactory.create_stop_word_remover()

base = os.getcwd() + '/App/Sentiment' + path


class Sentiment():
    app = None
    engine = None
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
    tfidf = None

    def init_app(self, app, max_features=10000):
        self.app = app
        with app.app_context():
            self.engine = db.engine
        self.max_features = max_features
        self.df = pd.read_csv(f'{base}/training.csv')

        self.load_library()
        self.generate_test()
        self.load_stopwords()

        self.X_train['Judul'] = self.X_train.Judul.apply(self.preprocessing)
        self.init_naive()
        return self
# TF-IDF

    def init_naive(self):

        self.tfidf = TfidfVectorizer(
            max_features=self.max_features,
            smooth_idf=False,
            ngram_range=(1, 1),
            lowercase=True,
            analyzer='word'
        )

        X_train_tfidf = self.tfidf.fit_transform(self.X_train['Judul'])
        X_test_tfidf = self.tfidf.transform(self.X_test['Judul'])

        # Implementasi Naive Bayes
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
#

    def generate_test(self):
        X = self.df[['Judul']]
        y = self.df[['Kategori']]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=.70, random_state=42)

    def load_stopwords(self):
        file_stopword = open(f"{base}/stopword.txt", "r")  # r = read
        self.stopwords = file_stopword.read().split('\n')
        file_stopword.close()

    def bersihkanDataset(self, teks):
        # casefolding
        teks = teks\
            .lower()\
            .replace('\\t', " ")\
            .replace('\\n', " ")\
            .replace('\\', "")

        teks = teks.encode('ascii', 'replace').decode('ascii')

        teks = teks.translate(str.maketrans("", "", string.punctuation))

        teks = teks.strip()

        teks = re.sub('\s+', ' ', teks)

        teks = re.sub(r"\b[a-z]\b", "", teks)

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

    def predict(self, source_file, result_path):
        mydict = []
        fields = ['Kategori', 'Judul', 'Isi', 'Casefolding', 'Filtering',
                  'Hapus StopWord',
                  'Tokenisasi',
                  'Stem',
                  'TFIDF', 'Prediksi', 'Hasil']

        with open(source_file, mode='r', encoding="utf8") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            # print(csv_reader)
            # exit()
            total_data = 0
            total_benar = 0
            accuracy = 0
            result_name = 'result_' + str(time.time()) + '.csv'
            result_file = result_path + result_name

            for row in csv_reader:

                filtering_teks = self.bersihkanDataset(row['Isi'])
                remove_stopword_teks = self.sastrawiStopword.remove(
                    filtering_teks)
                tokens = nltk.tokenize.word_tokenize(remove_stopword_teks)
                clean = [kata for kata in tokens if kata not in self.stopwords]
                kalimat = ' '.join(clean)
                stem_teks = self.stemmer.stem(kalimat)

                new_text_tfidf = self.tfidf.transform([stem_teks])
                predicted_category_isi = self.classifier.predict(
                    new_text_tfidf
                )[0]

                filtering_teks = self.bersihkanDataset(row['Judul'])
                remove_stopword_teks = self.sastrawiStopword.remove(
                    filtering_teks)
                tokens = nltk.tokenize.word_tokenize(remove_stopword_teks)
                clean = [kata for kata in tokens if kata not in self.stopwords]
                kalimat = ' '.join(clean)
                stem_teks = self.stemmer.stem(kalimat)

                new_text_tfidf = self.tfidf.transform([stem_teks])
                predicted_category = self.classifier.predict(
                    new_text_tfidf
                )[0]

                if predicted_category_isi != predicted_category:
                    predicted_category = predicted_category_isi

                mydict.append({
                    'Kategori': row['Kategori'],
                    'Judul': row['Judul'],
                    'Isi': row['Isi'],
                    'Casefolding': row['Judul'].lower(),
                    'Filtering': filtering_teks,
                    'Hapus StopWord': remove_stopword_teks,
                    'Tokenisasi': ','.join(tokens),
                    'Stem': stem_teks,
                    'TFIDF': new_text_tfidf,
                    'Prediksi': predicted_category,
                    'Hasil': predicted_category == row['Kategori'],
                })
                if predicted_category == row['Kategori']:
                    total_benar += 1
                total_data += 1
            accuracy = int((total_benar / total_data) * 100)

        with open(result_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fields)

            writer.writeheader()
            writer.writerows(mydict)
        return {
            'total_data': total_data,
            'total_benar': total_benar,
            'accuracy': accuracy,
            'result_file': result_name,
        }
    pass

    def singlePredict(self, judul, isi, Kategori):
        filtering_teks = self.bersihkanDataset(isi)
        remove_stopword_teks = self.sastrawiStopword.remove(
            filtering_teks)
        tokens = nltk.tokenize.word_tokenize(remove_stopword_teks)
        clean = [kata for kata in tokens if kata not in self.stopwords]
        kalimat = ' '.join(clean)
        stem_teks = self.stemmer.stem(kalimat)
        new_text_tfidf = self.tfidf.transform([stem_teks])
        predicted_category_isi = self.classifier.predict(
            new_text_tfidf
        )[0]

        filtering_teks = self.bersihkanDataset(judul)
        remove_stopword_teks = self.sastrawiStopword.remove(
            filtering_teks)
        tokens = nltk.tokenize.word_tokenize(remove_stopword_teks)
        clean = [kata for kata in tokens if kata not in self.stopwords]
        kalimat = ' '.join(clean)
        stem_teks = self.stemmer.stem(kalimat)
        new_text_tfidf = self.tfidf.transform([stem_teks])
        predicted_category = self.classifier.predict(
            new_text_tfidf
        )[0]

        if predicted_category_isi != predicted_category:
            predicted_category = predicted_category_isi

        return {
            'Kategori': Kategori,
            'Judul': judul,
            'Isi': isi,
            'Casefolding': judul.lower(),
            'Filtering': filtering_teks,
            'Hapus StopWord': remove_stopword_teks,
            'Tokenisasi': ','.join(tokens),
            'Stem': stem_teks,
            # 'TFIDF': json.dumps(new_text_tfidf),
            'Prediksi': predicted_category,
            'Hasil': predicted_category == Kategori,
        }
    pass


pass
