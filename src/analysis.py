import spacy
from textblob import TextBlob
import en_core_web_sm
from colorama import Fore
import seaborn as sns
import pandas as pd
from math import sqrt
import matplotlib.pyplot as plt
import numpy as np
import pickle
############ print results #################

def print_company_results(companies):
    if len(companies) == 0:
        print('no company detected')
        return
    
    company_w = 'company' if len(companies)==0 else 'companies'
    
    print(f'{len(companies)} {company_w} detected :')
    for c in companies:
        print(f'    - {c}')
        
def print_sentiment_results(sentiment)->None:
    polarity, subjectivity = sentiment
    
    if polarity == 0 and subjectivity == 0:
        print('neutral')
        return
    
    polarity_color = Fore.RED if polarity<0 else Fore.GREEN
    subj_color = Fore.LIGHTYELLOW_EX if subjectivity>0.2 else Fore.WHITE
    print(f'''sentiment={polarity_color}{100 * polarity:.2f}%{Fore.RESET}; subjectivity = {subj_color}{100 * subjectivity:.2f}% {Fore.RESET}''')
        
    
################### analysis ########################

def analyze_sentiment(text):
    # get sentiment and subjectivity
    # which are values between -1 and 1
    blob = TextBlob(text)    
    sentiment = blob.sentiment
    
    return sentiment

# companies analysis

def search_companies(article_content:str):
    print('\n--------- Searching for companies ----------')

    nlp = spacy.load('en_core_web_md')
    doc = nlp(article_content)
    
    companies = set([
        X.text
        for X in doc.ents
        if X.label_ == 'ORG'
    ])
    
    print_company_results(companies)
    return companies

def plot_heat_map(text):
    nlp = en_core_web_sm.load()
    tokens = nlp(text)
    embeddings = [token.vector for token in tokens]

    for elem in tokens:
        print(elem)
    
    # Compute pairwise cosine distances
    cosine_distances = np.zeros((len(embeddings), len(embeddings)))

    for i in range(len(embeddings)):
        for j in range(len(embeddings)):
            cosine_distances[i, j] = cosine(embeddings[i], embeddings[j])

    # Plot the HeatMap
    # sns.heatmap(cosine_distances, xticklabels=tokens, yticklabels=tokens, annot=True, cmap="viridis")
    # plt.title("Pairwise Cosine Distances between Words")
    # plt.show()
    
    
################# Scandal Detection ########################""
    
def get_companies_sentences(companies:list, text:str) -> list[str]:
    res = []
    
    for sentence in text.split('.'):
        for company in companies:
            if company in sentence:
                res.append(sentence)
            
    return res    
    
def detect_scandal(companies, text):
    print('-------- computing embeding and word distances ---------\n This will take a few seconds ...')
    
    nlp = spacy.load('en_core_web_md')

    keywords = [
    "Spill",
    "Leak",
    "Contamination",
    "Erosion",
    "Deforestation",
    "Acidification",
    "Overfishing",
    "Dumping",
    "Poisoning",
    "Wastewater",
    "Smog",
    "Eutrophication",
    "Habitat",
    "Destruction",
    "Soot",
    "Sulfur",
    "dioxide",
    "Mercury",
    "Pesticides",
    "Herbicides",
    "Oil",
    "Cyanide",
    "Pollution",
    "Deforestation"
    ]
    
    company_sentences = get_companies_sentences(companies, text)
    similarities = {}
    
    for keyword in keywords:
        for sentence in company_sentences:

            kw_token = nlp(keyword)
            sentence_token = nlp(sentence)
            similarity = kw_token.similarity(sentence_token)
            
            similarities[similarity] = keyword + ' : ' + sentence
    
    max = np.max(list(similarities.keys()))
    sentence = similarities[max]
    return max, sentence

# topic detection
        
def detect_topic():
    print('------------ topic detection -------------')
    
    
    