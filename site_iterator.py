from urllib.request import urlopen

import pandas as pd
import re

import helpers
import web_page_investigator


def open_url(url):
    page = urlopen(url)
    html = page.read().decode("utf-8")
    return html


def iterate_site(site):
    dict_configs = helpers.get_configs('web_scraper.properties')

    base_url = dict_configs.get(site + '_base_url')
    search_string = dict_configs.get(site + '_genre_search')
    genres = dict_configs.get(site + '_genres')
    start_item = dict_configs.get(site + '_start_item')
    genre_list = genres.split(',')
    max_pages = int(dict_configs.get(site + '_max_pages'))

    dict_all_movies = {}

    for g in range(0, len(genre_list)):
        genre = genre_list[g]

        for p in range(0, max_pages):
            if len(dict_all_movies) == 0:
                next_item = 1
            else:
                next_item = max([int(element) for element in [re.sub('\.', '', element) for element in dict_all_movies[0]]]) + 1

            url = base_url + search_string + genre + start_item + str(next_item)
            html = open_url(url)
            if len(dict_all_movies) == 0:
                dict_all_movies = web_page_investigator.get_values_from_page(html)
            else:
                dict_movies = web_page_investigator.get_values_from_page(html)
                for i in range(0, len(dict_movies)):
                    values = dict_movies[i]
                    dict_all_movies[i] = dict_all_movies[i] + values

    df_movies = pd.DataFrame(dict_all_movies)
    return df_movies.T

