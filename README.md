# Todo simple application
## Python/Flask application

## Run

### Create .env file in directory
```
POSTGRES_PASSWORD=example
POSTGRES_USER=example
POSTGRES_DB=todoapp
DB_HOST=db - db service name in docker-compose.yml
FLASK_APP=app
DEBUG=0
PORT=5000
# SMTP mail settings
MAIL_SERVER=server.name
MAIL_PORT=2525
MAIL_USE_TLS=0 - 1 or 0
MAIL_USE_SSL=0 - 1 or 0
MAIL_DEFAULT_SENDER=email send from
MAIL_USERNAME=email to loggin
MAIL_PASSWORD=email password
```

### Execute docker-compose run command
### One time for migrate:
```
docker exec -it todo_web flask db init
docker exec -it todo_web flask db migrate
docker exec -it todo_web flask db upgrade
```
### For run
```
docker-compose up -d
```

### After the application starts, navigate to `http://localhost:5000` in your web browser.


### Stop and remove the containers

```
docker-compose down
```
### Or just stop

```
docker-compose stop
```