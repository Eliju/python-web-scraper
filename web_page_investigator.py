import re
import pandas as pd


def get_values_from_page(html):
    titles = get_titles(html)
    years = get_years(html)
    genres = get_genres(html)
    descriptions = get_descriptions(html)
    images = get_images(html)
    ranks = get_ranks(html)
    directors = get_director(html)
    stars = get_stars(html)
    classification_details = get_classification_details(html)
    rating_values = get_rating_values(html)
    metascores = get_metascores(html)
    list_movie_details = [ranks, titles, years, genres, descriptions, images, directors,stars, classification_details, rating_values, metascores]
    return list_movie_details


def get_titles(html):
    pattern = "<h3 class=.*?<a href=./title/tt.*?/.\n>.*?</a>"
    elements = get_elements(html, pattern)
    titles = [re.sub('\. ', '.  ', element) for element in elements]
    titles = [element.strip().split('.  ')[1].strip() for element in titles]
    return titles


def get_years(html):
    #pattern = "<span class=.lister-item-year text-muted unbold.>.*?</span>"
    pattern = "(<a href=./title/.*?<div class=.lister-item-image float-left.>|<a href=./title/.*?lister-page-next next-page|<a href=./title/.*?lister-page-prev prev-page)"
    match_results = re.findall(pattern, html, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
    match_results = [re.sub("<a href=./title/.*?<span class=.lister-item-year text-muted unbold.>", "", element, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL, count=1) for element in match_results]
    match_results = [re.sub("(</span.*?<div class=.lister-item-image float-left.>|</span.*?lister-page-next next-page|</span.*?lister-page-prev prev-page)", "", element, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL, count=1) for element in match_results]
    years = [re.sub("<.*?>", "", element, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL) for element in [re.sub("\n", "", element.strip(), flags=re.IGNORECASE | re.MULTILINE | re.DOTALL) for element in [re.sub("<.*?\n>", "", element, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL) for element in match_results]]]
    return years


def get_genres(html):
    pattern = "<span class=.genre.>\n.*?</span>"
    elements = get_elements(html, pattern)
    genres = [element.strip() for element in elements]
    return genres


def get_descriptions(html):
    pattern = "<p class=.text-muted.>\n.*?</p>"
    elements = get_elements(html, pattern)
    descriptions = [element.strip() for element in elements]
    return descriptions


def get_images(html):
    pattern = 'loadlate=".*?"'
    match_results = re.findall(pattern, html, re.IGNORECASE | re.MULTILINE)
    images = [re.sub('"', '', image) for image in [re.sub('loadlate="', '', image) for image in match_results]]
    return images


def get_ranks(html):
    pattern = "<span class=.lister-item-index unbold text-primary.>.*?</span>"
    elements = get_elements(html, pattern)
    ranks = [re.sub(',', '', element, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL) for element in [re.sub('\.', '', element, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL) for element in elements]]
    return ranks


def get_director(html):
    pattern = "(<a href=./title/.*?<div class=.lister-item-image float-left.>|<a href=./title/.*?lister-page-next next-page|<a href=./title/.*?lister-page-prev prev-page)"
    match_results = re.findall(pattern, html, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
    directors = ["" if element.find('Director') == -1 else element for element in match_results]
    directors = [re.sub(
          "<span class=.ghost.>.</span>.*?Stars:.*?<div class=.lister-item-image float-left.>|<span class=.ghost.>.</span>.*?Stars:.*?lister-page-next next-page|<span class=.ghost.>.</span>.*?Stars:.*?lister-page-prev prev-page",
          "", element, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL) for element in
                   [re.sub("</a>.*?Directors:\n<a href=./name/.*?>", " Director: ", element,
                        flags=re.IGNORECASE | re.MULTILINE | re.DOTALL) for element
                 in [re.sub("</a>.*?Director:\n<a href=./name/.*?>", " Director: ", element,
                            flags=re.IGNORECASE | re.MULTILINE | re.DOTALL) for element
                     in [re.sub("<a href=./title/.*?<a href=./title/.*?>", "", element,
                                flags=re.IGNORECASE | re.MULTILINE | re.DOTALL, count=1) for element in
                         directors]]]]

    directors = [re.sub("\n","", element, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL) for element in
                 [re.sub("<.*?>","", element, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL) for element in directors]]
    directors = [element.split(' Director: ') for element in directors]
    directors = ['Director: ' + element[1].strip() if len(element) == 2 else 'Director:\'\'' for element in directors]
    return directors


def get_stars(html):
    pattern = "Stars:.*?</p>"
    elements = get_elements(html, pattern)
    stars = [re.sub('Stars:', 'Stars: ', element) for element in [element.strip() for element in elements]]
    return stars


def get_classification_details(html):
    pattern = " {4}<a href=./title/.*?<span class=.genre.>"
    elements = get_elements(html, pattern)
    classification_details = [element.replace('  ', '') for element in [re.sub('\(.*?\)', '|', element) for element in elements]]
    classification_details = [element.split('|') for element in classification_details]
    classification_details = [[item.strip() for item in element] for element in classification_details]
    return classification_details


def get_rating_values(html):
    pattern = "(<a href=./title/.*?<div class=.lister-item-image float-left.>|<a href=./title/.*?lister-page-next next-page|<a href=./title/.*?lister-page-prev prev-page)"
    match_results = re.findall(pattern, html, re.IGNORECASE | re.MULTILINE | re.DOTALL)
    rating_values = ["" if element.find('rating') == -1 else element for element in match_results]
    rating_values = [re.sub("/>", "", element, flags = re.MULTILINE | re.DOTALL) for element in [re.sub("<meta itemprop=", "", element, flags = re.MULTILINE | re.DOTALL) for element in [re.sub("</a>.*?aggregateRating.>", "", element, flags = re.MULTILINE | re.DOTALL) for element in [re.sub("<a href=./title/.*?<a href=./title/.*?>", "", element, flags=re.MULTILINE | re.DOTALL, count = 1) for element in rating_values]]]]
    rating_values = [re.sub("<span.*?<div class=.lister-item-image float-left.>|<span.*?lister-page-next next-page|<span.*?lister-page-prev prev-page", "", element, flags = re.MULTILINE | re.DOTALL) for element in rating_values]
    rating_values = [re.sub("content=\"", "content=", element, flags = re.MULTILINE | re.DOTALL) for element in [re.sub("<.*?>", "", element, flags = re.MULTILINE | re.DOTALL) for element in rating_values]]
    rating_values = [re.sub("\n", " ", element, flags = re.MULTILINE | re.DOTALL) for element in rating_values]
    rating_values = [re.sub("\"bestRating", "bestRating", element, flags = re.MULTILINE | re.DOTALL) for element in [re.sub("\"ratingCount", "ratingCount", element, flags = re.MULTILINE | re.DOTALL) for element in rating_values]]
    rating_values = [element.split('"') for element in rating_values]
    rating_values = [[item.strip() for item in element] for element in rating_values]
    rating_values = [element[:-1] for element in rating_values]
    return rating_values


def get_metascores(html):
    pattern = "(<a href=./title/.*?<div class=.lister-item-image float-left.>|<a href=./title/.*?lister-page-next next-page|<a href=./title/.*?lister-page-prev prev-page)"
    match_results = re.findall(pattern, html, re.IGNORECASE | re.MULTILINE | re.DOTALL)
    metascores = [re.sub("</span>.*?<div class=.lister-item-image float-left.>|</span>.*?lister-page-next next-page|</span>.*?lister-page-prev prev-page", "", element, flags=re.DOTALL) for element in [re.sub("</a>.*?class=\"metascore", " \"metascore", element, flags=re.DOTALL) for element in [re.sub("<a href=./title/.*?<a href=./title/.*?>", "", element, flags = re.DOTALL, count = 1) for element in match_results]]]
    metascores = ["" if element.find('metascore') == -1 else element for element in metascores]
    metascores = [re.sub(">", " ", element) for element in metascores]
    metascores = [element.split('"') for element in metascores]
    metascores = [[item.strip() for item in element] for element in metascores]
    return metascores


def get_elements(html, pattern):
    match_results = re.findall(pattern, html, re.IGNORECASE | re.MULTILINE | re.DOTALL)
    elements = [re.sub("<.*?>", "", element) for element in [re.sub("\n", "", element.strip()) for element in [re.sub("<.*?\n>", "", element) for element in match_results]]]
    return elements


def get_max_number_of_items(html):
    pattern = '<span>.*?-.*? of .*? titles.</span>'
    match_results = re.search(pattern, html, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
    max_number = re.sub('<span>.*? of ', '', match_results.group())
    max_number = re.sub(' titles.</span>', '', max_number)
    max_number = max_number.replace(',','')
    return int(max_number)