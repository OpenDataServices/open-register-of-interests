# Open Register of Interests

## Loading scraped data

```
python oroi/manage.py load_scrape_data postgresql://postgres-uri table_name
```

Omit `table_name` to load all tables

Example:

```
python oroi/manage.py load_scrape_data postgresql://datastore:datastore@127.0.0.1:5432/datastore ukparl_twfy
```

## Create the "ALL" data CSV download

To avoid having to create a CSV file at the time of request it is generated statically.
Use the following command to create the download:

```
$ manage.py csv_user_dump_all
```

The settings for CSV file including the output location are set in oroi/settings.py
