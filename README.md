# Letterboxd_Scraper
Scrapy Spider that crawls every movie in a genre of your choosing.

Run by going into project directory and using command:

$ scrapy crawl movies -a genre=""

Within the genre attribute input one of the Genres available on the dropdown menu on letterboxd.com/films
If you want to save the scraped data add to the previous command '-o File.extension'. .csv, .json, and .xml supported by scrapy

Data collected for each movie:

Title, Year of release, Director(s), Average letterboxd rating, Running Time, Views, Likes, and number of ratings for each possible rating of min half a star and max five stars in steps of halves.

Error logs are caused by movies that are missing numeric data. These are left out of the final dataset.
