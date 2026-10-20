# CSDF & Information Retrieval --- Programs and Mini-Project

This repository contains 10 practical assignments (5 CSDF and 5 IR) plus
a Tweet Sentiment Analysis mini-project. These are simplified academic
demonstrations.

## Requirements

-   Python 3
-   Internet access for package installation and first-time NLTK
    resource downloads

Install the libraries needed by the relevant programs:

``` bash
pip install pillow nltk scikit-learn scrapy
```

## CSDF --- Cyber Security and Digital Forensics

### 1. Email Header Analysis

**File:** `email_header_analyzer.py`\
Parses an email header and displays sender, recipient, subject, date,
routing entries, and available SPF/DKIM/DMARC results. Flags basic
warning signs.

**Input:** `email_header.txt` in the same folder.\
**Run:** `python email_header_analyzer.py`

### 2. CAPTCHA Generation and Verification

**File:** `captcha.py`\
Generates a random CAPTCHA image with distortion lines and noise, then
verifies the user's typed answer.

**Install:** `pip install pillow`\
**Run:** `python captcha.py`

### 3. Wi-Fi Authentication Failure Detection

**File:** `wifi_intrusion_detection.py`\
Analyzes simulated Wi-Fi authentication logs and flags a device after
repeated failures.

**Run:** `python wifi_intrusion_detection.py`\
**Note:** Simulation only; it does not block devices on a real access
point.

### 4. Deleted-File and Partition Forensics

**File:** `forensic_recovery.py`\
Demonstrates basic JPG/PNG/PDF file carving, checks MBR/GPT indicators,
and calculates a SHA-256 hash for a disk image.

**Run:** `python forensic_recovery.py`\
**Input:** A test disk image such as `.img` or `.dd`. Recovery is
limited and not guaranteed. Do not use your actual drive for a demo.

### 5. Log Capturing and Event Correlation

**File:** `log_correlation.py`\
Writes simulated events to `system.log`, groups failed logins by IP
address, and alerts on repeated failures within five minutes.

**Run:** `python log_correlation.py`

## IR --- Information Retrieval

### 6. Text Document Similarity

**File:** `document_similarity.py`\
Preprocesses two documents using tokenization, stop-word removal, POS
tagging, and lemmatization; calculates TF-IDF vectors and cosine
similarity.

**Install:** `pip install nltk scikit-learn`\
**Run:** `python document_similarity.py`\
The first run downloads the required NLTK resources.

### 7. PageRank Algorithm

**File:** `pagerank.py`\
Calculates PageRank scores for a small directed web graph and displays
pages in rank order.

**Run:** `python pagerank.py`

### 8. MapReduce Character Frequency

**File:** `mapreduce_char_count.py`\
Demonstrates Map and Reduce stages to count alphabetic characters,
ignoring case and non-alphabetic characters.

**Run:** `python mapreduce_char_count.py`

### 9. Simple Web Crawler Using Scrapy

**File:** `simplecrawler/spiders/basic_spider.py`\
Crawls pages from a seed URL, extracts titles and links, applies
depth/page limits, and exports results to CSV.

**Install and create project:**

``` bash
pip install scrapy
scrapy startproject simplecrawler
```

Save `basic_spider.py` inside `simplecrawler/spiders/`. From the project
directory, run:

``` bash
scrapy crawl basic -a start_url=https://example.com -a max_pages=5 -s DEPTH_LIMIT=2 -s CONCURRENT_REQUESTS=1 -O report.csv
```

Crawl only sites you are permitted to access and respect their
robots.txt rules, terms, and rate limits.

### 10. XML Parsing, Web Graph and Topic-Specific PageRank

**Files:** `webdata.xml`, `xml_pagerank.py`\
Parses page details and links from XML, builds a directed graph, and
calculates topic-biased PageRank scores.

**Run:** `python xml_pagerank.py`\
Keep both files in the same folder. Enter a topic such as `AI` or
`Sports`.

## Mini-Project --- Tweet Sentiment Analysis

**File:** `tweet_analysis.py`\
Accepts tweets, uses NLTK VADER to classify each as positive, negative,
or neutral, and prints a summary report.

**Install:** `pip install nltk`\
**Run:** `python tweet_analysis.py`\
Enter tweets one by one and type `exit` to print the report. The first
run downloads VADER's sentiment lexicon.

## Notes

-   Run each command from the directory containing the relevant script,
    unless stated otherwise.
-   The filenames above are suggested names; match them to your saved
    files.
-   These programs are simplified academic demonstrations, not
    production-grade security or forensic tools.
-   For forensic work, preserve the original evidence and analyze a
    verified copy whenever possible.
