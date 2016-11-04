from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from nltk.stem.snowball import SnowballStemmer

import pickle

data_path = 'data/'

def build_tfidf_vectorizer():
    """
    Creating empty TfidfVectorizer
    """

    with open(data_path + 'stop_words.txt', 'r') as f:
        stop_words = [w.strip() for w in f]

    stemmer = SnowballStemmer('russian')
    tkzr = CountVectorizer(token_pattern='[a-zA-Zа-яА-Я]+').build_tokenizer()

    stem_tokenize = lambda tokens: [stemmer.stem(item) for item in tokens if item not in stop_words]
    tokenize = lambda text: stem_tokenize(tkzr(text))

    return TfidfVectorizer(max_df=0.8, min_df= 5,
                           tokenizer=tokenize,
                           stop_words=stop_words)

texts = pickle.load(open(data_path + 'texts_fontanka.pickle', 'rb'))
tf_idfs_vectorizer = build_tfidf_vectorizer()
tf_idfs_vectorizer.fit(texts[:, 1])

svm = pickle.load(open(data_path + 'svm.pickle', 'rb'))
news_cats = pickle.load(open(data_path + 'news_cats.pickle', 'rb'))

def predict(text):
    """
    predcts category of provided text
    """
    tf_idf = tf_idfs_vectorizer.transform(text)
    raw_cat = svm.predict(tf_idf)[0]
    return news_cats[raw_cat]
