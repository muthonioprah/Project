# textdump
waste recycling system prototype

### To get started
1.create a virtual env
2.pip install -r requirements.txt
3.create a .env file with the following variables. 
```
FLASK_APP=main.py
FLASK_ENV=development
DEBUG=True
SQLALCHEMY_DATABASE_URI=
SECRET_KEY=

AT_USERNAME=
AT_API_KEY=
```
where:

SQLALCHEMY_DATABASE_URI is the database URI eg postgres, mysql
AT_USERNAME  is africastalking username
AT_API_KEY is africastalking api key

4. Use alembic to create tables by running the following in your terminal
```
$ alembic init alembic

$ alembic revision --autogenerate -m "create tables"

$ alembic upgrade head

```

5. run the application

```
$ flask run
```

