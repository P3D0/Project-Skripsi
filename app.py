from flask import Flask,  render_template, request
import pandas as pd

#buat prediksi
import tensorflow as tf
from numpy import array
import numpy as np
import pickle


#Init model & load model
def init():
    global model

model = None
def load_model():
    global model
    model = tf.keras.models.load_model('ModelP3D02.h5')

#load csv pake pandas
def loadCSV():
    df = pd.read_csv('Preprocessing.csv')
    df1 = df.head(1000)
    return df1

def loadHasilLabel():
    df = pd.read_csv('Labeling.csv')
    df1 = df.head(1000)
    return df1


app = Flask(__name__)
#Dashboard
@app.route('/')
def home():
    return render_template('home.html')

#Preprocessing Data

@app.route('/preprocessing', methods=['GET', 'POST'])
def preprocessing():
    df1 = loadCSV()
    print(request.form.get)
    #Case Folding
    if request.form.get('Data') == 'Case Folding':
        judul = 'Case Folding'
        heading = ('Ulasan','Case Folding')
        df1 = df1[['content', 'cleaned_content']]
    #Text Cleaning
    elif  request.form.get('Data') == 'Text Cleaning':
        judul = 'Text Cleaning'
        heading = ('Case Folding','Text Cleaning')
        df1 = df1[['cleaned_content', 'cleaning_data']]
    #Normalisasi
    elif  request.form.get('Data') == 'Normalisasi':
        judul = 'Normalisasi'
        heading = ('Text Cleaning', 'Normalisasi')
        df1 = df1[['cleaning_data','Remove_noise']]
    #Crawling Data
    else:
        judul = 'Crawling Data'
        heading = ('Username','Ulasan')
        df1 = df1[['userName','content']]
    results = [tuple(x) for x in df1.values]
    return render_template('preprocessing.html', header = heading, results = results, judul = judul)


# @app.route('/datacrawling', methods=['GET', 'POST'])
# def datacrawling():
#     df1 = loadCSV()
#     heading = ('Username','Ulasan')
#     df1 = df1[['userName','content']]
#     results = [tuple(x) for x in df1.values]
#     return render_template('datacrawling.html', header = heading, results = results)


# @app.route('/casefolding', methods=['GET', 'POST'])
# def casefolding():
#     df1 = loadCSV()
#     heading = ('Ulasan','Case Folding')
#     df1 = df1[['content', 'cleaned_content']]
#     results = [tuple(x) for x in df1.values]
#     return render_template('casefolding.html', header = heading, results = results)

# @app.route('/textcleaning', methods=['GET', 'POST'])
# def textcleaning():
#     df1 = loadCSV()
#     heading = ('Case Folding','Text Cleaning')
#     df1 = df1[['cleaned_content', 'cleaning_data']]
#     results = [tuple(x) for x in df1.values]
#     return render_template('textcleaning.html', header = heading, results = results)

# @app.route('/normalisasi', methods=['GET', 'POST'])
# def normalisasi():
#     df1 = loadCSV()
#     heading = ('Text Cleaning', 'Normalisasi')
#     df1 = df1[['cleaning_data','Remove_noise']]
#     results = [tuple(x) for x in df1.values]
#     return render_template('normalisasi.html', header = heading, results = results)

#labeling
@app.route('/labeling', methods=['GET', 'POST'])
def labeling():
    df1 = loadHasilLabel()
    heading = ('Review', 'Skor Polaritas', 'Sentimen')
    df1 = df1[['Remove_noise','nilai','sentimen']]
    results = [tuple(x) for x in df1.values]
    return render_template('labeling.html', header = heading, results = results)


#dah kelar yang visualisasi sama load sentimen

@app.route('/visualisasi')
def visualisasi():
    return render_template('visualisasi.html')

@app.route('/sentimen', methods=['GET', 'POST'])
def sentimen():
    if request.method == 'GET':
        return render_template('sentimen.html')
    elif request.method == 'POST':
        terxt = request.form.get('textnya')

        #load pickle buat tokenizing
        with open('tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)
        #buat prediksi
        max_length = 200
        data = [terxt] #ngubah jadi dictionary
        enc = tokenizer.texts_to_sequences(data)
        enc = tf.keras.preprocessing.sequence.pad_sequences(enc, maxlen=max_length, dtype='int32', value=0)
        sentiment = model.predict(enc)[0]
        sentimennya = ' '
        print(sentiment)
        if (np.argmax(sentiment) == 0):
            sentimennya = 'Sentimen: Negatif'

            print('Sentimen: Negatif')
        elif (np.argmax(sentiment) == 1):
            sentimennya = 'Sentimen: Netral'

            print('Sentimen: Netral')
        else:
            sentimennya = 'Sentimen: Positif'

            print('Sentimen: Positif')

        print(terxt)
        return render_template('sentimen.html', sentiimen = sentimennya, kata = terxt)
        # return render_template('sentimen.html', sentiimen = data)


#buat 404
@app.route('/<name>')
def user(name):
    return f'404 Not Found {name}'



if __name__ == '__main__':
    init()
    load_model()
    app.run(debug=True)