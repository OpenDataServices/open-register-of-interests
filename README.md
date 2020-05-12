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
