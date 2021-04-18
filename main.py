import site_iterator
import file_writer
import helpers


if __name__ == '__main__':
    dict_configs = helpers.get_configs('web_scraper.properties')
    dict_for_movies = site_iterator.iterate_site('imdb', dict_configs)
    for key, value in dict_for_movies.items():
        file_writer.write_df_to_csv(key, value, dict_configs)



