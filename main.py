import web_page_investigator

if __name__ == '__main__':
    html = web_page_investigator.open_url("https://www.imdb.com/search/title/?genres=film-noir")
    df_movies = web_page_investigator.get_values_from_page(html)
    print(df_movies.iloc[:,:2])
