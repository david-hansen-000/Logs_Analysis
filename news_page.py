#!/usr/bin/python3

from flask import Flask, request, Response, redirect
from news_get import get_sql
from datetime import date

app = Flask(__name__)

"""Set up the base html for the root page."""
html = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>News Review</title>
    <style>
      h1, form {
        text-align: left;
      }
      .btn-group {
        display:inline-block;
      }

    </style>
  </head>
  <body>
    <h1>News Review</h1>
    <form method="post">
      <div class="btn-group">
        <button name="top3" type="submit">
          Retrieve the Top 3 Most Viewed Titles
        </button>
        <button name="pop_artists" type="submit">
          Retrieve Artists
        </button>
        <button name="high_error_days" type="submit">
          Retrieve Days with High Errors
        </button>
      </div>
    </form>
  </body>
</html>
'''


@app.route('/', methods=['GET', 'POST'])
def news_items():
    """Set up the flow to follow to determine which page to show."""
    if request.method == 'POST':
        if 'top3' in request.form:
            return redirect('/top3')
        if 'pop_artists' in request.form:
            return redirect('/artists')
        if 'high_error_days' in request.form:
            return redirect('/higherrors')
    return html


@app.route('/top3', methods=['GET', 'POST'])
def get_top3():
    results = top3()
    response = Response(results, status=200, mimetype="text/plain")
    response.headers["Content-Type"] = "text/plain; charset=utf-8"
    return response


@app.route('/artists', methods=['GET', 'POST'])
def get_popular_artists():
    results = high_errors
    response = Response(results, status=200, mimetype="text/plain")
    response.headers["Content-Type"] = "text/plain; charset=utf-8"
    return response


@app.route('/higherrors', methods=['GET', 'POST'])
def get_high_errors():
    results = high_errors()
    response = Response(results, status=200, mimetype="text/plain")
    response.headers["Content-Type"] = "text/plain; charset=utf-8"
    return response

def top3():
    """"This section queries the database for the top three
    most popular articles."""
    sql = "select slug, popular from top3_view"
    results = "".join(
      '\"%s\" -- %d views\n'
      % (slug.title().replace('-', ' '), popular) for slug, popular in get_sql(sql))
    return results


def popular_artists():
    """This section queries the database for the artists of
    the articles."""
    sql = "select name, popular from popular_artists_view"
    results = "".join(
      '%s -- %d views\n'
      % (name, popular) for name, popular in get_sql(sql))
    return results


def high_errors():
    """"This section queries the database for the dates
    with more than 1% error rate."""
    sql = "select dates, percent from high_error_view"
    dateformat = "%B %d, %Y"
    results = "".join(
      '%s -- %.1f%% errors'
      % (date.strftime(dates, '%B %d, %Y'), percent)
      for dates, percent in get_sql(sql))
    return results

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
