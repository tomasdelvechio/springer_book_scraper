# Springer Books Scraper

This script simply goes through all the books in this spreadsheet https://docs.google.com/spreadsheets/d/1HzdumNltTj2SHmCv3SRdoub8SvpIEn75fa4Q23x0keU/htmlview?urp=gmail_link and downloads them into different folders (that it previously created) according to each book's topic.
The base directory where the books are downloaded is by default the one where this script is run in. To change it, change the constant `BASE_DIR` to whatever you like, such as `BASE_DIR = /home/books/springer_books`

## Running the script

`python ./springer_book_scraper.py`

without arguments, the script download all PDFs of all topics

## Show help

```bash
python ./springer_book_scraper.py -h
usage: springer_book_scraper.py [-h] [--topics TOPICS [TOPICS ...]]
                                [--list-topics]

Download all links from the Google Spreadsheet URL

optional arguments:
  -h, --help            show this help message and exit
  --topics TOPICS [TOPICS ...]
                        List of topics to download
  --list-topics         Show all available topics
```

## Filter by topics

This example only downloads of the specified topics:

```bash
python ./springer_book_scraper.py --topics "Biomedical and Life Sciences" "Medicine" "Computer Science" "Economics and Finance"
```

**show available topics**

```bash
python ./springer_book_scraper.py --list-topics
"Behavioral Science"
"Behavioral Science and Psychology"
"Biomedical and Life Sciences"
"Business and Economics"
"Business and Management"
"Chemistry and Materials Science"
"Computer Science"
"Earth and Environmental Science"
"Economics and Finance"
"Education"
"Energy"
"Engineering"
"Humanities, Social Sciences and Law"
"Intelligent Technologies and Robotics"
"Law and Criminology"
"Literature, Cultural and Media Studies"
"Mathematics and Statistics"
"Medicine"
"Physics and Astronomy"
"Religion and Philosophy"
"Social Sciences"
```

## Features

 * Download all files from Springer
 * Filter by topic
 * Download each topic in a directory
 * Progress bar for each document (thks @tomasjuran)
 * Resume download if cancell or fail (thks @tomasjuran)
