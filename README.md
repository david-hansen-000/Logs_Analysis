# Logs_Analysis
Analyze a News Log for Valuable Info

# A Review of the News
This project performs queries on a database and returns the results.

# Requirements
VirtualBox: https://www.virtualbox.org/wiki/Download_Old_Builds_5_1
vagrant: https://www.vagrantup.com/downloads.html
virtual machine: either 
https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip
or
https://github.com/udacity/fullstack-nanodegree-vm
classroom environment: https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
# Installation and Setup
After installing VirtualBox and vagrant set up the virtual machine in one of two ways:

1.  Dowload this file: https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip 
- unzip the file if not performed automatically
- cd into the vagrant directory:
 ```sh
$ cd FSND-Virtual-Machine/vagrant
 ```
 OR
2. clone the directory from here: https://github.com/udacity/fullstack-nanodegree-vm
- cd into the vagrant directory
```sh
$ cd fullstack-nanodegree-vm/vagrant
```

Once the classroom environment virtual machine is setup and the user is in the vagrant directory run 

```sh
$ vagrant up
```
When running for the first time it downloads a virtual machine and sets it up for the user according to the configuration in the VagrantFile.

Now unzip the classroom environment (https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) into the same directory as the vagrant directory above. 

Run:
```sh
psql -d news -f newsdata.sql
```
While in the postgresql shell create the views:
```
create view not_ok_dates as
select count(id) as bad_count, date(time) as dates from log 
where status != '200 OK' 
group by date(time) 
order by date(time);

create view ok_dates as 
select count(id) good_count, date(time) as dates from log
where status = '200 OK'
group by date(time) 
order by date(time);

create view high_error_view as
select not_ok_dates.dates as dates, 
(not_ok_dates.bad_count * 1.0 / ok_dates.good_count * 1.0) * 100.0 as percent 
from not_ok_dates 
join ok_dates on not_ok_dates.dates = ok_dates.dates 
where (not_ok_dates.bad_count * 1.0 / ok_dates.good_count * 1.0) * 100.0 > 1.0;

create view top3_view as 
select slug, count(path) as popular from log
inner join articles on path like concat('/article/',slug,'%') 
group by slug 
order by popular desc limit 3;

create view popular_artists_view as 
select authors.name, popular from (select author, count(path) as popular from log
inner join articles on path like concat('/article/',slug,'%') 
group by articles.author order by popular desc) as popular_views 
inner join 
authors on authors.id = popular_views.author;
```
Also copy these files into the vagrant directory.

- news_page.py
- plain_news.py
- news_get.py 

While in the vagrant directory run 
```sh
vagrant ssh
cd /vagrant
psql -d news -f newsdata.sql
```

# Running the News Program
The program can run and get the results in one of two ways. The first way runs a web server from the command line and gets the results in the web browser. The second way returns the results directly to the command line.

1. By web browser
-- cd into the vagrant file as above and run the virtual machine if not already up
```sh
$ vagrant up
$ vagrant ssh
## Now we're in the virtual machine
$ cd /vagrant
$ python3 news_page.py
```
- The last command runs a simple web server. Open a browser and type in the address bar: 
```
http://localhost:8000
```
- There are three buttons available to retrieve three different queries.
--"Retrieve the Top 3 Most Viewed Titles" button will start a query of the news database of the top three articles with the most views and display the results in a new page in plain text format.
-- "Retrieve Artists" button will start a query of the news database of the artists in the database with the number of views each artist has received and display the results in a new page in plain text format.
-- "Retrieve Days with High Errors" will start a query of the news database and retrieve any days where over 1% of requests returned errors and display the results in a new page in plain text format.

The second way:
2. from the command line 
```sh
$ python3 plain_news.python
```

# Views Used in the Project
Here are the views used in this project:
```
create view not_ok_dates as
select count(id) as bad_count, date(time) as dates from log 
where status != '200 OK' 
group by date(time) 
order by date(time);

create view ok_dates as 
select count(id) good_count, date(time) as dates from log
where status = '200 OK'
group by date(time) 
order by date(time);

create view high_error_view as
select not_ok_dates.dates as dates, 
(not_ok_dates.bad_count * 1.0 / ok_dates.good_count * 1.0) * 100.0 as percent 
from not_ok_dates 
join ok_dates on not_ok_dates.dates = ok_dates.dates 
where (not_ok_dates.bad_count * 1.0 / ok_dates.good_count * 1.0) * 100.0 > 1.0;

create view top3_view as 
select slug, count(path) as popular from log
inner join articles on path similar to concat('/article/',slug,'%') 
group by slug 
order by popular desc limit 3;

create view popular_artists_view as 
select authors.name, popular from (select author, count(path) as popular from log
inner join articles on path similar to concat('/article/',slug,'%') 
group by articles.author order by popular desc) as popular_views 
inner join 
authors on authors.id = popular_views.author;
```
