# udacity_fullstack-capstone
The fifth and final project for the Udacity Full Stack Web Developer Nanodegree. Requires a combination of all skills learned in the previous projects.


## Prerequisites
1. Install the Heroku CLI
    - On Windows run `choco install heroku-cli`
    - On Linux (Ubuntu 16+) run `sudo snap install --classic heroku`
    - Check successful installation with `heroku version`. For further usage run `heroku login`

2. Configuration Files
    - Create and update `requirements.txt` upon every dependency change with `pip freeze > requirements.txt`
    - Create a file `runtime.txt` which contains a single string specifying the python version for Heroku, e.g. `python-3.8.7`
    - Specify environment variables in `.env` for local development and in `.env.prod` for pushing them to heroku. Use `setup.sh` to push environment variables to Heroku. Use `createdb <DB NAME>` to create a database for the app.

        ```sh
        # .env
        FLASK_APP=app.py
        FLASK_ENV=development
        DATABASE_URL=postgres://localhost:5432/<DB NAME>

        # .env.prod
        ALGORITHMS="RS256"
        API_AUDIENCE=<AUTH0 API IDENTIFIER>
        AUTH0_DOMAIN=<AUTH0 PERSONAL DOMAIN>
        ```

    - Use `Procfile` to tell Heroku what to run. In our case one line with `web: gunicorn app:app` is enough (given that our python application resides within app.py), e.g.

        ```sh
        web: gunicorn app:app
        release: bash ./release-tasks.sh
        ```

    - Use `Procfile.windows` to tell Heroku what to run locally

        ```sh
        web: flask run
        release: bash ./release-tasks.sh
        ```

    - Use `release-tasks.sh` to specify multiple tasks that should be run after the build process, e.g.

        ```sh
        python manage.py db init
        python manage.py db migrate
        python manage.py db upgrade
        ```

3. Database
    - Run `pip install flask_script flask_migrate psycopg2-binary` to install necessary packages
    - By providing a `manage.py` file we can tell Heroku to run database migrations for us

        ```python
        import os

        from flask_script import Manager
        from flask_migrate import MigrateCommand

        from app import create_app

        manager = Manager(create_app)

        manager.add_command('db', MigrateCommand)

        # If run locally use .env file. This file is normally read by flask when
        # python-dotenv is installed, but flask_script does not use it.
        if os.path.exists('.env'):
            print('Importing environment from .env file')
            for line in open('.env'):
                var = line.strip().split('=')
                if len(var) == 2:
                    os.environ[var[0]] = var[1]

        if __name__ == '__main__':
            manager.run()
        ```

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
$ setup.sh # push environment variables for production to Heroku
$ heroku config # check the app's environment variables
```

## Run the App

1. Push to Heroku `git push heroku main`
2. Open in browser `heroku open`
3. If everything worked well you should be greeted with `"Hello, World!"`.