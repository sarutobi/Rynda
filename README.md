Rynda
=====
[![Build Status](https://travis-ci.org/sarutobi/Rynda.svg?branch=master)](https://travis-ci.org/sarutobi/Rynda)

http://rynda.org

Requirements
------------
- Python 2.7+
- spatialite
- GEOS
- PROJ.4
- Virtualenv (optional)

Quickstart
------------

(Optional) Create and activate virtualenv:
```
$ virtualenv rynda
$ source rynda/bin/activate
```
1. Clone the repository:
```
$ git clone https://github.com/sarutobi/Rynda.git
```
2. cd to cloned repository:
```
$ cd Rynda
```
3. Install all requirements:
```
$ pip install -r requirements\test.txt
```
4. Create database structure:
```
$ python manage.py migrate
```
5. Run the local server:
```
$ python manage.py runserver
```
6. Point your browser to [http://localhost:8000](http://localhost:8000)
7. To make tests, type:
```
$ python manage.py test
```
