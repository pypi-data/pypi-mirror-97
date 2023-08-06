ukrainian
========

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# ukrainian
This repository consists of Python scripts that generate learning aides for learning Ukrainian. I currently have three available scripts. Each has a separate function.
## *_get-table.py
This first script gets tables from http://lcorp.ulif.org.ua/dictua/ for each word available on the website. Once run, it will start downloading the tables from the website and searching for the additional words. The program requires you to have Google Chrome and to download the associated Google Chrome driver. You must put the driver in the ../tools directory. There are OS dependencies when using the Selenium/Chrome Driver combination. I have only tested this on MacOS Sierra, MacOS Catalina, and CentOS 8.0. I cannot ensure that it will work on other operating systems.

The get-table script uses a very "hacky" method to pull the table from lcorp.ulif.org/. If anyone is having issues pulling from an ASPX server due to the VIEWSTATE and EVENTVALIDATION fields in the request, then this is the best work-around I was able to find. Keep in mind that my method is very slow - it pulls tables at a rate of about 4 per minute. Since I pulled >260,000 tables, this was a total of 45 machine-days of runtime.
## read_html.py
The second script reads the tables that are downloaded from the first script. The script parses through the unpredictable tables and handles several different exceptions. The script deals with encoding issues as well. The table values are stored as dictionaries in JSON format.
## daily_article.py
The third script generates a website with a daily article. The website pulls the main article of the day from https://ua.korrespondent.net/ and adds the accents from the dictionaries generated in the read_html.py script.
