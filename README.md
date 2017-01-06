# Scraping Heroes of the Storm Competitive Data
This repository is meant to serve as a resource for anyone interested in analyzing data in the heroes of the storm competitive scene. 
The project uses the Python package Scrapy to collect information from [https://masterleague.net/] and inserts it into a SQLite
database. The database contains basic match information that is appropriate for Elo or Glicko rating systems. A second table
contains information about the individual players, with detailed match statistics if they were available (when a replay is
released). A third table includes all of the heroes, their roles, and the dates when Blizzard added them to the game.

## Requirements and Use
In order to run the spider, you need to Python (I used version 3.4) and Scrapy installed. I personally
use the [Anaconda Python Distribution](https://www.continuum.io/) but I am not responsible for any
individual issues you might have. With Anaconda just run

`conda install scrapy`

Once installed, navigate to the hots_scrapy directory in your terminal/powershell and enter

`scrapy crawl hots`

The scraping works by incrementing the match by 1 in the URL, which means it automatically ends when it
encounters a 404 error. Some matches are missing, so you cannot scrape the entire website at once.
To start at a different match, change the value in `start_urls`. Since Anaconda does not have 
[scrapy-deltafetch](https://github.com/scrapy-plugins/scrapy-deltafetch), I did not implement it so
you will need to manually change the starting URL every time.

## Updates
I will try to update the SQLite database at least once a week, but no guarantees. I happily welcome
any pull requests. The most pressing issue at the moment is to find a way to scrape match information
so analysts can look at how events during a match affect outcomes.

## Blog Post
I included the blog post that I originally wrote as a more detailed explanation of how I developed the
Scrapy spider so that anybody with a basic knowledge of Python and SQL should be able to understand
my code.

## Extracting SQLite Tables
If you are not familiar with SQL and prefer to import CSV files into your preferred data analysis tool,
you can use the [DB Browser for SQLite](http://sqlitebrowser.org/) (I am not responsible for any
issues you might have with that tool since I am not one of the developers). To extract the data:

* Click on File on the top left of the screen
* Go to 'Export' and click on 'Table(s) as CSV file'
* Select the table(s) you want, using ctrl-click to select multiple tables
* Click OK and choose an appropriate directory

You should now be able to open them with Excel or LibreOffice Calc, or import them for other analysis.

## License
This project is licensed under the terms of the MIT license.