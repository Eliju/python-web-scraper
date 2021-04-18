def write_df_to_csv(filename, df_to_be_saved, configs):
    dict_config = configs
    folder = dict_config.get("folder_for_files")
    df_to_be_saved.to_csv(folder + filename + '.csv', index = False)