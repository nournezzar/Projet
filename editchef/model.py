import tensorflow as tf 
import re 
import nltk 
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
#from keras.preprocessing.text import Tokenizer
#from keras.preprocessing.sequence import pad_sequences
import numpy as np

nltk.download('stopwords')

seed_value = 42
np.random.seed(seed_value)
tf.random.set_seed(seed_value)

class ArticleClassifier:
    def __init__(self):
        self.model = tf.keras.models.load_model(r'C:\Users\Latitude7480\Downloads\Auth-20240525T055617Z-001\Auth\prj\editchef\model99.h5')

    def preprocess_text(self, text):
        print('dans le pre trait ')
        stop_words = set(stopwords.words('english'))
        stemmer = SnowballStemmer('english')
        
        text = re.sub('[^a-zA-Z]', ' ', text)
        words = text.lower().split()
        words = [stemmer.stem(word) for word in words if not word in stop_words]
        cleaned_text = ' '.join(words)
        
        return cleaned_text

    def classify(self, article,nbrev):
        cleaned_article = self.preprocess_text(article)
        
        vocabulary_size = 10000
        max_text_len = 250
       # tokenizer = Tokenizer(num_words=vocabulary_size)
        #tokenizer.fit_on_texts([cleaned_article])
        #sequences = tokenizer.texts_to_sequences([cleaned_article])
        #X_DeepLearning = pad_sequences(sequences, maxlen=max_text_len)
        
       # probabilities = self.model.predict(X_DeepLearning)[0]
        #top_reviewers = self.get_top_reviewers(probabilities, nbrev)

        #return top_reviewers
    
    def get_top_reviewers(self, probabilities, n):
        top_indices = np.argsort(probabilities)[::-1][:n]
        return top_indices