from urllib.request import urlopen

import pandas as pd
import re
import copy

import web_page_investigator


def open_url(url):
    page = urlopen(url)
    html = page.read().decode("utf-8")
    return html


def iterate_site(site, configs):
    dict_configs = configs

    base_url = dict_configs.get(site + '_base_url')
    search_string = dict_configs.get(site + '_genre_search')
    genres = dict_configs.get(site + '_genres')
    start_item = dict_configs.get(site + '_start_item')
    genre_list = genres.split(',')
    max_pages = int(dict_configs.get(site + '_max_pages'))
    next_item = int(dict_configs.get(site + '_start_from'))
    dict_of_dataframes = {}

    for g in range(0, len(genre_list)):
        dict_all_movies = {}
        genre = genre_list[g]

        url = base_url + search_string + genre + start_item + str('1')
        html = open_url(url)
        max_number = web_page_investigator.get_max_number_of_items(html)

        pages_to_be_fetched = (max_number / 50).__ceil__()
        if pages_to_be_fetched > max_pages:
            pages_to_be_fetched = max_pages

        for p in range(0, pages_to_be_fetched):
            if  dict_all_movies == {}:
                item_to_be_fetched = next_item + 1
            else:
                item_to_be_fetched = max([int(element) for element in dict_all_movies[0]]) + 1
            if item_to_be_fetched > max_number:
                break

            url = base_url + search_string + genre + start_item + str(item_to_be_fetched)
            html = open_url(url)
            if len(dict_all_movies) == 0:
                dict_all_movies = web_page_investigator.get_values_from_page(html)
            else:
                dict_movies = web_page_investigator.get_values_from_page(html)
                for i in range(0, len(dict_movies)):
                    values = dict_movies[i]
                    dict_all_movies[i] = dict_all_movies[i] + values

        movie_columns = ['Rank', 'Title', 'Year', 'Genre', 'Description',
                         'Image', 'Director', 'Stars', 'Classifications',
                         'Ratings', 'Metascore']

        df_movies = pd.DataFrame(dict_all_movies)
        df_movies = df_movies.T
        df_movies.columns = movie_columns
        df_movies['Duration'] = df_movies['Classifications'].apply(check_list_for_duration)
        df_movies['Restriction'] = df_movies['Classifications'].apply(check_list_for_restriction)
        df_movies.drop('Classifications', inplace=True, axis=1)
        df_movies['RatingValue'] = df_movies['Ratings'].apply(check_list_for_ratingvalue)
        df_movies['BestRating'] = df_movies['Ratings'].apply(check_list_for_bestrating)
        df_movies['CountRating'] = df_movies['Ratings'].apply(check_list_for_ratingcount)
        df_movies.drop('Ratings', inplace=True, axis=1)
        df_movies['Metascore_Favorable'] = df_movies['Metascore'].apply(check_list_for_metascore_favorable)
        df_movies['Metascore_Mixed'] = df_movies['Metascore'].apply(check_list_for_metascore_mixed)
        df_movies['Metascore_Unfavorable'] = df_movies['Metascore'].apply(check_list_for_metascore_unfavorable)
        df_movies.drop('Metascore', inplace=True, axis=1)
        dict_of_dataframes['df_for_' + genre] = copy.deepcopy(df_movies)

    return dict_of_dataframes


def check_list(item_list, str, str_replace, ix_offset):
    ret_val = ''
    if item_list is None:
        return
    if len(item_list) > 1:
        for ix in range(0,len(item_list)):
            if item_list[ix].find(str) > -1:
                ret_val = item_list[ix+ix_offset].replace(str_replace,'')
    return ret_val


def check_list_for_duration(item_list):
    return check_list(item_list, 'min', '', 0)


def check_list_for_restriction(item_list):
    return check_list(item_list, '-', '', 0)


def check_list_for_ratingvalue(item_list):
    return check_list(item_list, 'ratingValue', 'content=', 1)


def check_list_for_bestrating(item_list):
    return check_list(item_list, 'bestRating', 'content=', 1)


def check_list_for_ratingcount(item_list):
    return check_list(item_list, 'ratingCount', 'content=', 1)


def check_list_for_metascore_favorable(item_list):
    return check_list(item_list, 'metascore  favorable', '', 1)


def check_list_for_metascore_mixed(item_list):
    return check_list(item_list, 'metascore  mixed', '', 1)


def check_list_for_metascore_unfavorable(item_list):
    return check_list(item_list, 'metascore  unfavorable', '', 1)



