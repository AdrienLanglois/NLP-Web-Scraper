import os
from webscraper import scrap
from utils import save_json,read_json
import pandas as pd
import analysis
from colorama import Fore

def choose_url():
    return 0
    
    choice = input('''     Choose a website :
        1 : CCN
        2 : IGN France
        3 : IGN Middle East (English)
        0 : skip webscraping (analyse existing data)
    ''')
    return int(choice)

def print_headline(title, url):
    print(f"\n\nEnriching {Fore.CYAN}'{title}'{Fore.RESET}")
    print(f"Read More : {Fore.BLUE}'{url}'{Fore.RESET}")

def main():
    
    # choose a website to scrap and scrap it
    user_selection = choose_url()
    if user_selection != 0: # 0 means 'skip webscraping'
        scrap(user_selection)
        
    # load the articles
    articles = read_json(user_selection)
    articles_df = pd.DataFrame(articles)
    
    # article analysis
    for [url, date, title, body] in articles_df.values[:1]:
        print_headline(title, url)

        companies = analysis.search_companies(title + body)
        
        print('\n--------- Sentiment Analysis ----------')
        title_sentiment_results = analysis.analyze_sentiment(title)
        body_sentiment_results = analysis.analyze_sentiment(body)
        
        # print sentiment analysis results
        print('title :', end='')
        analysis.print_sentiment_results(title_sentiment_results)
        print('body :', end='')
        analysis.print_sentiment_results(body_sentiment_results)
        
        # scandal detection
        scandal_metric, scandal_sentence = analysis.detect_scandal(companies, title + body)

if __name__ == '__main__':
    main()