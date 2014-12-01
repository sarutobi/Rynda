Rynda
=====
[![Build Status](https://travis-ci.org/sarutobi/Rynda.svg?branch=master)](https://travis-ci.org/sarutobi/Rynda)

http://rynda.org
http://openrynda.te-st.ru/

Технические требования
------------
- Python 2.7+
- spatialite
- GEOS
- PROJ.4
- Virtualenv (опционально, но строго рекомендуется)

Быстрый старт
------------

(Опционально) Создаем и активируем virtualenv:

```
$ virtualenv rynda
$ source rynda/bin/activate
```

1. Клонируем репозиторий:

```
$ git clone https://github.com/sarutobi/Rynda.git
```

2. переходим в клонированный репозиторий:

```
$ cd Rynda
```

3. Устанавливаем все зависимости:

```
$ pip install -r requirements\test.txt
```

4. Копируем mysettings.py.example в mysettings.py

5. Задаем структуру базы данных и пароль суперпользователя:

```
$ bash createdb.sh 
```

Дважды вводим пароль суперпользователя.

Имя суперпользователя по умолчанию: admin

6. Запускаем локальный сервер:

```
$ python manage.py runserver
```

7. Открываем в браузере [http://localhost:8000](http://localhost:8000)

8. Что бы протестировать систему запускаем:

```
$ python manage.py test
```
-------
http://rynda.org
http://openrynda.te-st.ru/

Requirements
------------
- Python 2.7+
- spatialite
- GEOS
- PROJ.4
- Virtualenv (optional, but strongly recommended)

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
$ pip install -r requirements/test.txt
```

4. Copy mysettings.py.example to mysettings.py

5. Create database structure and superuser password:

```
$ bash createdb.sh 
```

Enter superuser password twice.

defauit superuser name: admin

6. Run the local server:

```
$ python manage.py runserver
```

7. Point your browser to [http://localhost:8000](http://localhost:8000)

8. To make tests, type:

```
$ python manage.py test
```

