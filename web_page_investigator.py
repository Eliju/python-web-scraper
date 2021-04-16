from urllib.request import urlopen
import re


def open_url():
    url = "https://www.imdb.com/search/title/?genres=sci-fi"

    page = urlopen(url)
    html = page.read().decode("utf-8")

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


def get_titles(html):
    pattern = "<h3 class=.*?<a href=./title/tt.*?/.\n>.*?</a>"
    return get_elements(html, pattern)


def get_years(html):
    pattern = "<span class=.lister-item-year text-muted unbold.>.*?</span>"
    return get_elements(html, pattern)


def get_genres(html):
    pattern = "<span class=.genre.>\n.*?</span>"
    return get_elements(html, pattern)


def get_descriptions(html):
    pattern = "<p class=.text-muted.>\n.*?</p>"
    return get_elements(html, pattern)


def get_images(html):
    pattern = 'loadlate=".*?"'
    match_results = re.findall(pattern, html, re.IGNORECASE | re.MULTILINE)
    images = [re.sub('"', '', image) for image in [re.sub('loadlate="', '', image) for image in match_results]]
    return images


def get_ranks(html):
    pattern = "<span class=.lister-item-index unbold text-primary.>.*?</span>"
    return get_elements(html, pattern)


def get_director(html):
    pattern = "(<a href=./title/.*?<div class=.lister-item-image float-left.>|<a href=./title/.*?lister-page-next next-page)"
    match_results = re.findall(pattern, html, re.IGNORECASE | re.MULTILINE | re.DOTALL)
    directors = ["" if element.find('Director') == -1 else element for element in match_results]
    directors = [re.sub("</a>.*?<div class=.lister-item-image float-left.>|</a>.*?lister-page-next next-page", "", element, flags = re.MULTILINE | re.DOTALL) for element in [re.sub("</a>.*?Director:\n<a href=./name/.*?>", " Director: ", element, flags=re.DOTALL) for element in [re.sub("<a href=./title/.*?<a href=./title/.*?>", "", element, flags = re.DOTALL, count = 1) for element in directors]]]
    return directors


def get_stars(html):
    pattern = "Stars:.*?</p>"
    return get_elements(html, pattern)


def get_classification_details(html):
    pattern = " {4}<a href=./title/.*?<span class=.genre.>"
    return get_elements(html, pattern)


def get_rating_values(html):
    pattern = " {4}<a href=./title/.*?<meta itemprop=.ratingValue. content=..*?. />.*?<span class=.rating-bg.>"
    elements = get_elements(html, pattern)
    rating_values = [re.sub("Rate this", "", element) for element in [re.sub("</a>", "", element) for element in [re.sub("content=.", "content=", element) for element in [re.sub("<span.*?>", "", element) for element in [re.sub("<meta itemprop=", "", element) for element in [re.sub("<span .*?itemprop=", "", element ) for element in [re.sub("</div>", "", element) for element in [re.sub("<div.*?>", "", element) for element in [re.sub("Rate this.*?<meta", "", element).strip() for element in [re.sub(". />", "", element) for element in elements]]]]]]]]]]
    return rating_values


def get_metascores(html):
    pattern = "(<a href=./title/.*?<div class=.lister-item-image float-left.>|<a href=./title/.*?lister-page-next next-page)"
    match_results = re.findall(pattern, html, re.IGNORECASE | re.MULTILINE | re.DOTALL)
    metascores = [re.sub("</span>.*?<div class=.lister-item-image float-left.>|</span>.*?lister-page-next next-page", "", element, flags=re.DOTALL) for element in [re.sub("</a>.*?class=\"metascore", " \"metascore", element, flags=re.DOTALL) for element in [re.sub("<a href=./title/.*?<a href=./title/.*?>", "", element, flags = re.DOTALL, count = 1) for element in match_results]]]
    metascores = ["" if element.find('metascore') == -1 else element for element in metascores]
    metascores = [re.sub(">", " ", element) for element in metascores]
    return metascores


def get_elements(html, pattern):
    match_results = re.findall(pattern, html, re.IGNORECASE | re.MULTILINE | re.DOTALL)
    elements = [re.sub("<.*?>", "", element) for element in [re.sub("\n", "", element.strip()) for element in [re.sub("<.*?\n>", "", element) for element in match_results]]]
    return elements
