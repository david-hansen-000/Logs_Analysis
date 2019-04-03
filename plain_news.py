#!/usr/bin/python3

from news_get import get_sql
from datetime import date
from news_page import top3, popular_artists, high_errors


print("\nNews Review\n\n")
print("Retrieve the Top 3 Most Viewed Titles\n\n{}\n".format(top3()))
print("Retrieve Artists\n\n{}\n".format(popular_artists()))
print("Retrieve Days with High Errors\n\n{}\n".format(high_errors()))
