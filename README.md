# Scraping Heroes of the Storm Competitive Data
This repository is meant to serve as a resource for anyone interested in analyzing
data in the heroes of the storm competitive scene.  The project uses Python to
collect information from [https://masterleague.net/] and inserts it into a
SQLite database. The database contains basic match information that is
appropriate for Elo or Glicko rating systems.

## Requirements and Use
In order to update the databse, you will need Python 3 (I used version 3.6.3).
I personally use the [Anaconda Python Distribution](https://www.continuum.io/)
but I am not responsible for any individual issues you might have. In the
`update_hots_db.py` file, change the value of `min_match_id` to the correct
value. This is typically one greater than the highest match id with detailed
match information. Once you have edited this value, navigate to the directory
in a terminal and run `python update_hots_db.py` to update the database.

The API allows a limited number of calls per day, so you may not be able to
update the database with each new competitive match in one day.

## Extracting SQLite Tables
If you are not familiar with SQL and prefer to import CSV files into your
preferred data analysis tool, you can use the
[DB Browser for SQLite](http://sqlitebrowser.org/) (I am not responsible for any
issues you might have with that tool since I am not one of the developers).
To extract the data:

* Click on File on the top left of the screen
* Go to 'Export' and click on 'Table(s) as CSV file'
* Select the table(s) you want, using ctrl-click to select multiple tables
* Click OK and choose an appropriate directory

You should now be able to open them with Excel or LibreOffice Calc, or import
them for other analysis.

## License
This project is licensed under the terms of the MIT license.
