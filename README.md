# udacity_fullstack-capstone
The fifth and final project for the Udacity Full Stack Web Developer Nanodegree. Requires a combination of all skills learned in the previous projects.


## Prerequisites
1. Install the Heroku CLI
    - On Windows run `choco install heroku-cli`
    - On Linux (Ubuntu 16+) run `sudo snap install --classic heroku`
    - Check successful installation with `heroku version`. For further usage run `heroku login`

2. Configuration Files
    - Create and update `requirements.txt` upon every dependency change with `pip freeze > requirements.txt`
    - Set up environment variables within `setup.sh`
    - Use `Procfile` to tell Heroku what to run. In our case one line with `web: gunicorn app:app` is enough (given that our python application resides within app.py)

3. Database
    - By providing a `manage.py` file we can tell Heroku to run database migrations for us
    - Run `pip install flask_script flask_migrate psycopg2-binary` to install necessary packages
    - Now we can run our local migrations using our manage.py file, to mirror how Heroku will run behind the scenes for us when we deploy our application:

        ```python
        python manage.py db init
        python manage.py db migrate
        python manage.py db upgrade
        ```

        Those last commands are the essential process that Heroku will run to ensure your database is architected properly. We, however, won't need to run them again unless we're testing the app locally.

## Set Up the Heroku App

```sh
$ heroku create <APP NAME> # also adds a git remote 'heroku'
$ heroku addons:create heroku-postgresql:hobby-dev --app <APP NAME> # creates a Postgres DB and adds its URL as environment variable DATABASE_URL
$ heroku config --app <APP NAME> # check the app's environment variables
```

