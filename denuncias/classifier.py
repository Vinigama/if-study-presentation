from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize
import pickle
import re, string
from django.conf import settings

class Classifier():
    def __init__(self, comentario, tagger, model):
        self.tagger         = tagger
        self.model          = model
        self.comentario     = comentario


    def lemmatize_sentence(self, tokens):
        """ Função para reduzir uma palavra à sua forma base e agrupar diferentes formas da mesma palavra"""
        lemmatizer = WordNetLemmatizer()
        lemmatized_sentence = []
        for word, tag in self.tagger.tag(tokens):
            if tag.startswith('N'):
                pos = 'n'
            elif tag.startswith('V'):
                pos = 'v'
            else:
                pos = 'a'
            lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
        return lemmatized_sentence


    def remove_noise(self, tokens, stop_words = ()):
        """ Remoção de ruídos de comunicação """
        cleaned_tokens = []

        for token, tag in self.tagger.tag(tokens):
            token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                        '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
            token = re.sub("(@[A-Za-z0-9_]+)","", token)

            if tag.startswith("N"):
                pos = 'n'
            elif tag.startswith('V'):
                pos = 'v'
            else:
                pos = 'a'

            lemmatizer = WordNetLemmatizer()
            token = lemmatizer.lemmatize(token, pos)

            if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
                cleaned_tokens.append(token.lower())

        return cleaned_tokens

    def classify_model(self):
        """ Classificar o comentario em positivo ou negativo """
        custom_tokens = self.remove_noise(word_tokenize(self.comentario))
        return self.model.classify(dict([token, True] for token in custom_tokens))
    
