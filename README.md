# expense_manager

Installation
1. Create .env file in directory with docker-compose.yml
and define variables below:
  * SECRET_KEY - django project secret key
  * DEBUG - 1 to enable django project debug mode, 0 otherwise
  * DB_HOST=db
  * DB_NAME - the same as POSTGRES_DB
  * DB_USER - the same as POSTGRES_USER
  * DB_PORT=5432
  * DB_PASS - the same as PASTGRES_PASSWORD
  * POSTGRES_DB - database name
  * POSTGRES_USER - postgres user name
  * POSTGRES_PASSWORD - password
  * CELERY_BROKER_URL=redis://redis:6379/0
  * CELERY_RESULT_BACKEND=redis://redis:6379/0
  * EMAIL_HOST - for example smtp.gmail.com
  * EMAIL_HOST_USER - your email
  * EMAIL_HOST_PASSWORD - app password

2. `docker-compose build`
3. `docker-compose up`

To see the API open http://localhost:8000/api/v1/ and you will see the swagger.
