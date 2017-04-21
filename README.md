# DressChampion

*To promote something is to champion it.*

`dress-champion` is a Flask application for creating custom dress/product promotions.
 
### Dataset

`dress-champion` uses workers to consume the 'dresses' and 'ratings' topic on Kafka, filling its own MySQL database with data. You can run these workers as follows:

```python manage.py consume dresses```

```python manage.py consume ratings```

### REST API

There is also a RESTful API that offers the following functionality, for a user interface can (and should!) be build, to offer this functionality to customer success managers. 

#### Search dresses:

```GET http://127.0.0.1:5000/api/dresses?filter[objects]=[{"name":"season","op":"==","val":"SUMMER"}]```

More info on the search format on the [flask-restless docs page](https://flask-restless.readthedocs.io/en/stable/searchformat.html).

#### Create, query and update promotions:

```GET http://127.0.0.1:5000/api/promotions```

```POST http://127.0.0.1:5000/api/promotions```

```GET http://127.0.0.1:5000/api/promotions/3```

```PUT http://127.0.0.1:5000/api/promotions/3```

#### Add a dress to or remove it from a promotion

```POST http://127.0.0.1:5000/api/promotions/3/dresses/21B21C002-Q11```

```DELETE http://127.0.0.1:5000/api/promotions/3/dresses/21B21C002-Q11```

# Setup

## Database

```bash
$ mysql -uroot
CREATE USER 'dresschampuser'@'localhost' IDENTIFIED BY {PASSWORD};
CREATE DATABASE dresschamp;
GRANT ALL PRIVILEGES ON dresschamp.* To 'dresschampuser'@'localhost';
CREATE DATABASE dresschamp_test;
GRANT ALL PRIVILEGES ON dresschamp_test.* To 'dresschampuser'@'localhost';
FLUSH PRIVILEGES;
```

## App

#### Config
Create your app config by making a copy of `dress_champion/config.example.py`, rename to `config.py` in the same folder, and enter the settings for your local dev environment, based on the examples given there.
 
#### Virtual env
Create a Python 3.5 virtualenv and install dependencies with `make install-deps`. Dependencies can be manage easily with [pip-tools](https://github.com/jazzband/pip-tools)'s `requirements.in` file.

## Tests

Pytest tests can be run with the following make command: `make test`.
