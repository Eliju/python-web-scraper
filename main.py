import site_iterator


if __name__ == '__main__':
    df_movies = site_iterator.iterate_site('imdb')
    print(df_movies.iloc[:,:3])



