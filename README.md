# Tourbook (Fullstack Nanodegree Capstone Project)

The fifth and final project for the Udacity Full Stack Web Developer Nanodegree. Requires a combination of all skills learned in the previous projects.

The Tourbook models an application with which users can track their outdoor adventures. For each tour they can decide whether it is public or private. Some users will have moderator rights: they can create, update or delete the available outdoor categories. Finally the application will also need users with admin rights that can look into problems, fix malformatted data or problematic entries.

## Motivation

Building a geospatially enabled API has been on my wish list for quite a while. The perfect choice for this was something rather simple but still super useful which naturally lead me to the idea of a tourbook app. Eventually it will also feature a Vue.js frontend coupled with OpenLayers to let users easily create and view their tours.

Based on what I learned in the Fullstack Nanodegree I seized the opportunity to learn a little bit more about structuring flask applicatons and chose to implement three "novelties": 1) the application factory pattern, 2) Blueprints for routing and 3) Pluggable Views instead of normal route decorators.

Because this app is meant to be geospatially enabled I decided to use the PostGIS extension for PostgreSQL instead of simply using lat/lon columns.

## Specifications

* Models
    * Tours with attributes user_id, activity_id, name, description, date, starttime, endtime, accesslevel_id, location
    * Activities with attributes name, description
    * Accesslevels with attributes name
* Endpoints
    * GET /tours, /tours/id, /activites and /activities/id
    * DELETE /tours/id and /activities/id
    * POST /tours and /activities
    * PATCH /tours/id and /activities/id
* Roles
    * Anonymous
        * Can only view public tours
    * User, same as Anonymous plus:
        * Can create new tours
        * Can view private tours created by him
        * Can modify tours created by him
        * Can delete tours created by him
        * Can view all activities
    * Moderator, same as User plus:
        * Can modify activities
        * Can create activities
        * Can delete activities
    * Admin, same as Moderator plus:
        * Can view, modify and delete any tour, even if it is private
* Tests
    * One test for success behavior of each endpoint
    * One test for error behavior of each endpoint
    * Two tests of RBAC for each role

## Prerequisites & Setup Local

1. Clone this GitHub Repo.
1. Create a virtual environment for Python with `py -3.8 -m venv env` (on Windows) within the GitHub Repo.
1. Activate the virtual environment with `env\Scripts\activate.bat`.
1. Install dependencies with `pip install -r requirements.txt`
1. Create a Postgres database with the PostGIS extension:
    ```bash
    createdb udacity-capstone
    psql -d udacity-capstone -c 'create extension postgis;'
    ```
1. Load sample data with `python load_data.py`
1. Query the app interactively with `flask shell`:
    ```python
    tour = Tour.query.first()
    tour.to_geojson()
    ```

    Returns:

    ```bash
    {'type': 'Point',
    'coordinates': [7.1, 46.1],
    'properties': {'id': 1,
    'activity': {'id': 1, 'name': 'Mountainbiking', 'description': 1},
    'name': 'Admin Entry',
    'description': None,
    'date': '2021-02-13',
    'starttime': None,
    'endtime': None,
    'accesslevel': {'id': 1, 'name': 'Public'}}}
    ```
1. Open `Tourbook-API.postman_collection.json` and get examples on how to query the API at `/api/tours/`, `/api/tours/<id>`, `/api/activities/` and `/api/activities/<id>`.

## Development Prerequisites
1. Install the Heroku CLI
    - On Windows run `choco install heroku-cli`
    - On Linux (Ubuntu 16+) run `sudo snap install --classic heroku`
    - Check successful installation with `heroku version`. For further usage run `heroku login`

1. Setup the Heroku Database
    - On Windows use `cmd.exe` and login with:

        ```sh
        # login remote
        heroku pg:psql --app <APP NAME>
        # create extension
        create extension postgis;
        ```
1. Setup local development
    - Run `python manage.py db init`.
    - For flask migrations to work properly modify `migrations/script.py.mako` and add `import geoalchemy2`.
1. Manage migrations

    By providing a `manage.py` file we can tell Heroku to run database migrations for us

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

    Now we can run our local migrations using our manage.py file, to mirror how Heroku will run behind the scenes for us when we deploy our application:

    ```bash
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    ```

    Those last commands are the essential process that Heroku will run to ensure your database is architected properly. We, however, won't need to run them again unless we're testing the app locally.

1. Configuration Files
    - Create and update `requirements.txt` upon every dependency change with `pip freeze > requirements.txt`
    - Create a file `runtime.txt` which contains a single string specifying the python version for Heroku, e.g. `python-3.8.7`
    - Specify environment variables:
        - in `.env` for local development
        - in `.env.prod` for pushing them to heroku. Use `setup.sh` to push environment variables to Heroku.

        ```sh
        # .env
        FLASK_APP=tourbook.py
        FLASK_ENV=development
        DATABASE_URL=postgres://localhost:5432/<DB NAME>

        # .env.prod
        ALGORITHMS="RS256"
        API_AUDIENCE=<AUTH0 API IDENTIFIER>
        AUTH0_DOMAIN=<AUTH0 PERSONAL DOMAIN>
        ```

    - Use `Procfile` to tell Heroku what to run. In our case one line with `web: gunicorn 'app:create_app()'` is enough but it can be helpful to specify more, e.g. release tasks:

        ```sh
        web: gunicorn 'app:create_app()'
        release: bash ./release-tasks.sh
        ```

    - Use `Procfile.windows` to tell Heroku what to run locally

        ```sh
        web: flask run
        release: bash ./release-tasks.sh
        ```

    - Use `release-tasks.sh` to specify multiple tasks that should be run after the build process, e.g.

        ```sh
        python manage.py db upgrade
        python load_data.py
        # Other commands...
        ```

## Set Up the Heroku App

```sh
$ heroku create <APP NAME> # also adds a git remote 'heroku'
$ heroku addons:create heroku-postgresql:hobby-dev --app <APP NAME> # creates a Postgres DB and adds its URL as environment variable DATABASE_URL
$ setup.sh # push environment variables for production to Heroku
$ heroku config # check the app's environment variables
```

## Run the App

### Heroku

1. Push to Heroku `git push heroku main`
1. Open in browser `heroku open`
1. If everything worked well you should be greeted with `"Hello, World!"`.

### Locally

1. Provided that you created an `.env` file as specified above just run `flask run`.
1. Navigate to `http://localhost:5000/` and you should be greeted with `"Hello, World!"`

## Testing

Create a test database and install the PostGIS extension:

``` bash
createdb capstone_test
psql -d capstone_test -c 'create extension postgis;'
```

Tests can be run for each role. Each role only encompasses tests necessary to validate the specific access rights of that role and it is assumed that everything else will work in the same way as it does for the roles with lower access rights. Role hierarchy is: public (not authenticated) -> user (authenticated) -> moderator (can modify Activity) -> admin (has access to and can modify everything)

Run tests like this:

```bash
python test_public.py
python test_user.py
python test_moderator.py
python test_admin.py
```