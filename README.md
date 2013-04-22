Rynda
=====
http://rynda.org

Requirements
------------
- Python 2.7+
- Postgresql
- PostGIS
- GDAL
- Virtualenv (optional)

Installation
------------
1. PIP installation require additional packages:

- Python-dev
- Postgresql-server-dev
- libxml2-dev
- libxslt1-dev

2. Optional: create virtualenv and activate it
3. Clone repository
4. cd to cloned repository and execute

> pip install -r Rynda/requirements/&lt;file&gt;.txt

where &lt;file&gt; is one of:

- develop - for local developement
- production - for production server
- test - for testing purposes (this does not using postgresql database)

