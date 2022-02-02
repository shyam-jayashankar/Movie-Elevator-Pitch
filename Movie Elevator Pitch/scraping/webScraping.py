import requests
import string
from bs4 import BeautifulSoup
from dateutil.parser import parse
import concurrent.futures
import pandas as pd
import argparse
import os
import configparser

def process_rating(rating):
    try:
        return float(rating.replace("/10",''))
    except:
        return ''

def get_movie_title(soup):
    try:
        return soup.find("h1", {"data-testid": "hero-title-block__title"}).text
    except:
        return ''

def get_movie_description(soup):
    try:
        return soup.find("div", {"data-testid": "storyline-plot-summary"}).text
    except:
        return ''

def get_movie_rating(soup):
    try:
        return soup.find("div", {"data-testid": "hero-rating-bar__aggregate-rating__score"}).text
    except:
        return ''

def get_movie_popularity(soup):
    try:
        return soup.find("div", {"data-testid": "hero-rating-bar__popularity__score"}).text
    except:
        return ''

def scrape_imdb_data(imdb_page_url):
    # print("Processing for url: ", url)
    page = requests.get(imdb_page_url).text
    soup = BeautifulSoup(page, "html.parser")

    movie_title = get_movie_title(soup)
    movie_description = get_movie_description(soup)
    movie_rating = process_rating(get_movie_rating(soup))
    movie_popularity = get_movie_popularity(soup)
    return {"title": movie_title,
            "description": movie_description,
            "rating": movie_rating,
            "popularity": movie_popularity
            }


def get_imdb_urls(imdb_ids):
    url = "https://www.imdb.com/title/+/"
    urls = list()
    for id in imdb_ids:
        urls.append(url.replace('+', id))
    return urls

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_file', help='Configuration file', required=True)
    args = parser.parse_args()
    config_file = args.config_file

    config = configparser.ConfigParser()
    config.read_file(open(config_file))

    data_loc = config.get('webScraping', 'dataset_loc')
    if not os.path.isfile(data_loc):
        print('Please provide a valid location of the dataset.')
        exit()

    df = pd.read_csv(data_loc, error_bad_lines=False)

    imdb_title_list = df.imdb_title_id.to_list()
    print("Number of titles :", len(imdb_title_list))
    urls = get_imdb_urls(imdb_title_list)

    urls.remove('https://www.imdb.com/title/tt9914942/')
    urls = urls[:30000]
    print("Number of urls :", len(urls))
    final_data = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = []
        for url in urls:
            futures.append(executor.submit(scrape_imdb_data, imdb_page_url=url))
        for future in concurrent.futures.as_completed(futures):
            final_data.append(future.result())
    # urls = ['https://www.imdb.com/title/tt9914942/']
    # final_data=[]
    # for url in urls:
    #     a = scrape_imdb_data(url)
    #     print(a)
    #     final_data.append(a)
    print("final length = ", len(final_data))
    df2 = pd.DataFrame(final_data)
    scraped_data_loc = config.get('webScraping', 'final_data')
    df2.to_csv(scraped_data_loc, index=False)

    # urls = ["https://www.imdb.com/title/tt1375666/", ]
    #
    # for url in urls:
    #     x = IMDBScraper(url)
    #
    #     print(x.scrape_data())