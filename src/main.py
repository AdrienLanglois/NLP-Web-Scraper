import os
from webscraper import scrap
from utils import save_json

def choose_url():
    return 1
    
    choice = input('''     Choose a website :
        1 : CCN
        2 : IGN France
        3 : IGN Middle East (English)
    ''')
    return int(choice)

def main():
    # choose a website to scrap
    user_selection = choose_url()
    articles = scrap(user_selection)
    save_json(articles)
    

if __name__ == '__main__':
    main()