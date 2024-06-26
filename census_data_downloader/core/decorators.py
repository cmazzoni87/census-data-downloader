#! /usr/bin/env python
# -*- coding: utf-8 -*
"""
Decorators to help manage our custom classes.
"""
TABLE_LIST = []


def register(cls):
    """
    A decorator to register new table configuration classes.
    """
    TABLE_LIST.append(cls)
    return cls


def downloader(func):
    """
    A decorator to download data inside a table configuration class.
    """
    def inner(*args, **kwargs):
        # Grab the TableConfig
        table_config = args[0]
        table_config.all_data = []
        # Grab the geotype downloader class by running the metaprogramming function
        downloader_klass = func(table_config)
        # For each year authorized on the config
        for year in table_config.years_to_download:
            # Create the geotype downloader instance
            downloader = downloader_klass(table_config, year)
            # check if kwargs are passed
            # Download the raw data
            if kwargs:
                downloader.download(kwargs)
            else:
                downloader.download()

            # Process the data
            processed_data = downloader.process()
            table_config.all_data.append(processed_data)
    return inner
