## Database Usage

The database is run using Flask-SQLAlchemy. The table definitions can be found in `mooches/models.py`

When you use `python manager.py runserver` the database will automatically seed itself if not already done.

Here is how you can work with the database at the `shell`.

```bash
$> python3 manager.py shell
>>> models.seed()

# to query the database
>>> records = models.Mooch.query.all()
>>> print(records[0].LastName) # get the last name

# to refresh the records in the DB with the spreadsheet
>>> models.update()
```

For more advanced usage check the SQLAlchemy docs or look at the examples in `mooches/models.py` and `mooches/main/views.py`

### Spreadsheet Scraping

I went a fancy route and use anonymous access to the google spreadsheet to sync it with the database.
The scraper is contained in `mooches/spreadsheets.py`. It downloads CSV copies of the spreadsheets and uses `csv.DictWriter` to parse the output.
Within the `models` file there is a mapping of spreadsheet keys with their database equivalent. This is used to enumerate the records into database objects.
