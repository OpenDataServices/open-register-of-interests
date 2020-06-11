# Open Register of Interests

This repository contains the "declared." front end and data store for declarations from the open registers of interest project.

Related respositories:

- [oroi-scrape](https://github.com/OpenDataServices/oroi-scrape)
- [oroi-depoly](https://github.com/OpenDataServices/oroi-deploy)
- [oroi-standard](https://github.com/OpenDataServices/oroi-standard)


## Installing

### Docker

Use the docker files found in [oroi-depoly](https://github.com/OpenDataServices/oroi-deploy) e.g.
```
docker-compose -f docker-compose-declaration_nav-load.yml up -d
```


### Local

Services required: 
- elasticsearch 7.7.1
- postgres:11.8


Note this has been tested with python 3.8
```
$ virtualenv .ve --python=python3
$ source .ve/bin/activate
$ pip install -r requirements.txt
``` 

## Loading scraped data

```
$ oroi/manage.py load_scrape_data postgresql://postgres-uri table_name
```

Omit `table_name` to load all tables

Example:

```
$ oroi/manage.py load_scrape_data postgresql://datastore:datastore@127.0.0.1:5432/datastore ukparl_twfy
```

## Rebuild the elasticsearch index

```
$ oroi/manage.py search_index --rebuild # See also --help
```

## Create the "ALL" data CSV download

To avoid having to create a CSV file at the time of request it is generated statically.
Use the following command to create the download:

```
$ manage.py csv_user_dump_all
```

The settings for CSV file including the output location are set in oroi/settings.py
