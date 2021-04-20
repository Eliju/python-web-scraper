from jproperties import Properties


def get_configs(file_name):
    configs = Properties()
    with open(file_name, 'rb') as config_file:
        configs.load(config_file)
        config_file.close()
    items_view = configs.items()
    configs_dict = {}

    for item in items_view:
        configs_dict[item[0]] = item[1].data
    return configs_dict
