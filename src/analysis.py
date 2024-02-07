import spacy
from textblob import TextBlob
import en_core_web_sm
# from spacy import displacy
# from collections import Counter


def check_companies():
    nlp = en_core_web_sm.load()
    paragraph = "new project annonced by Ubisoft"

    doc = nlp(paragraph)
    print([(X.text, X.label_) for X in doc.ents])



def analyze_sentiment(text):
    blob = TextBlob(text)    
    # Get the sentiment polarity (-1 for negative, 0 for neutral, 1 for positive)
    sentiment = blob.sentiment
    return sentiment

paragraph = "I love this product! It's amazing."
sentence = "This movie is very good"
a = "Ce film est très bien"
print(analyze_sentiment(paragraph))
print(analyze_sentiment(sentence))
print(analyze_sentiment(a))