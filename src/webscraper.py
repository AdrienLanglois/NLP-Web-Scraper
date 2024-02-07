from bs4 import BeautifulSoup
import requests
from colorama import Fore
import re
import sys
from datetime import datetime, timedelta

ARTICLE_LIMIT = 300

# return true if the article is more than a week old
def is_old(date: str) -> bool:
    
    # ignore the article if date not found (date == None)
    if not date:
        return True
    
    # extract relevant date info
    pattern = r"[a-zA-Z]+ \d+, \d{4}"
    date = re.findall(pattern, date.text)[0]
    
    article_date = datetime.strptime(date, '%B %d, %Y')
    today = datetime.now()
    difference = today - article_date
    
    return int(difference.days) > 7

def get_CNN_links():
    
    base_url = 'https://edition.cnn.com/'
    topics = ['', 'world', 'politics', 'health', 'entertainment', 'tech', 'sport', 'weather']
    article_links = []
    
    for topic in topics:        
        full_url = base_url+topic
        response = requests.get(full_url)
        if response.status_code != 200:
            print(Fore.RED + f"Failed to retrieve HTML content. Status code: {response.status_code}", Fore.RESET)
            continue
        
        soup = BeautifulSoup(response.text, 'lxml') 
        
        links = [
            a['href']
            for a in soup.find_all('a', class_='container__link')
            if a
        ]
        
        for l in links: article_links.append(l)
        
    print(f'\n {len(article_links)} articles found')
    return article_links[:ARTICLE_LIMIT]
    

def scrap_CNN():
    print('searching for articles ...')
    
    # search for article links    
    links = get_CNN_links()
    scraped_articles = []
    
    for i,link in enumerate(links):
        
        # print the progression
        sys.stdout.write(f"\rreading articles... {i}/{len(links)} [{int(100 * i/len(links))}%]")
        sys.stdout.flush()
        
        if not link.startswith('http'):
            link = 'https://edition.cnn.com' + link
        
        response = requests.get(link)
        if response.status_code != 200:
            print(f'\nFailed to access the article: {response.status_code}')
            continue
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        date = soup.find('div', class_='timestamp')
        
        if is_old(date):
            continue
        
        date = date.text.replace(r" +"," ")
        title = soup.find('h1').text
        content = [p.text for p in soup.find_all('p')]
        
        scraped_articles.append({
            'url': link,
            'date': date,
            'title': title,
            'body': content
        })
    
    return scraped_articles

def scrap_IGN(url):
    # make a request to the website
    response = requests.get(url)
    if response.status_code != 200:
        print(Fore.RED + f"Failed to retrieve HTML content. Status code: {response.status_code}", Fore.RESET)
        return
    
    # fetch articles links
    soup = BeautifulSoup(response.text, 'lxml')
    
    sections = soup.find_all('article', limit=ARTICLE_LIMIT)
    links = [section.a['href'] for section in sections if section.a]
    
    scraped_articles = []
    
    print('reading articles ...')
    
    # scrap every articles found
    for link in links:
        if not link.startswith('http'):
            link = url + link
        
        response = requests.get(link)
        if response.status_code != 200:
            print(f'Failed to access the article: {response.status_code}')
            continue
        
        soup = BeautifulSoup(response.text, 'lxml')
        date = soup.find('div', class_='article-publish-date')
        if not date:
            continue
        date = date.span.text        
        
        #########################################################
        ######## TO DO : ignore old article (>1 week) #########
        #######################################################
        
        title = soup.h1.text
        content = [p.text for p in soup.find_all('p')]
        
        scraped_articles.append({
            'url': link,
            'date': date,
            'title': title,
            'body': content
        })
                
    print(f'Finished ! {len(scraped_articles)} article found')
    return scraped_articles

def scrap(user_selection:int):
    match user_selection:
        case 1: return scrap_CNN()
        case 2: return scrap_IGN('https://fr.ign.com/') # IGN FR
        case 3: return scrap_IGN('https://me.ign.com/en/') # IGN EN
        case _: print('ERROR : bad user selection')