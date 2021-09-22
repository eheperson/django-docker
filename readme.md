
## Project directory structure 

docker-compose-test
        └── app
        │   ├── webapp
        │   │   ├── __init__.py
        │   │   ├── asgi.py
        │   │   ├── settings.py
        │   │   ├── urls.py
        │   │   └── wsgi.py
        │   ├── manage.py
        │   ├── Dockerfile
        │   └── requirements.txt
        ├── docker-compose.yml
        └── 

## Django Setup

Prepare the environment

    mkdir docker-compose-example
    cd docker-compose-test
    mkdir app
    

    python3 -m venv venv
    source /venv/bin/acivate
    pip install Django

    mkdir app
    cd app

    django-admin startproject webapp .

    python manage.py makemigrations
    python manage.py migrate

    nano Dockerfile
    #Dockerfile is at the app/Dockerfile
    # there is a "Dockerfile.django.old" file in the project root directory.
    # rename actual "Dockerfile" as "Dockerfile.old" and this "Dockerfile.django.old" file as "Dockerfile" 
    # there are a lot of steps for this docker-compose-example project and almost for each step
    # we need to update actual "Dockerfile". I prefered to store old Dockerfiles with ".old" extension.
    # I could be able to replace actual "Dockerfile" with required ".old" dockerfile easily with that choice.

    pip freeze >> requirements.txt

    cd ..
    touch .env.dev 
    echo "DEBUG=1" >> .env.dev
    echo "SECRET_KEY=foo" >> .env.dev
    echo "DJANGO_ALLOWED_HOSTS=localhost 0.0.0.0 [::1]" >> .env.dev

<!--  -->
After creating and editing .env.dev file change the webapp/settings.py file as follow :

    SECRET_KEY = 'django-insecure-ri3)q%km$!dz&f2$e(zm%!$rl=k40n&@sf_y6v9a&dl@2a_pra' 
    to
    SECRET_KEY = os.environ.get("SECRET_KEY")

    DEBUG = True
    to
    DEBUG = int(os.environ.get("DEBUG", default=0))

    ALLOWED_HOSTS = []
    to
    ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
    # 'DJANGO_ALLOWED_HOSTS' should be a single string of hosts with a space between each.
    # For example: 'DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'

    #Do not forget to add 'import os' to the top of the 'settings.py'

<!--  -->
Bıild the image : 

    docker-compose build

Once the image is built, run the container:

    docker-compose up -d

Navigate to http://localhost:8000/ to again view the welcome screen.
Check for errors in the logs if this doesn't work via docker-compose logs -f.

## PostgreSQL Setup

    cd docker-compose-example
    
    # activate venv if not active
    pip install psycopg2
    pip freeze >> requirements.txt

Check the docker-compose.yml file.
A new service is added as 'db' to docker-compose.yml:
This service for the postgreSql container.

We'll need some new environment variables for the web service as well to the .env.dev

    echo "SQL_ENGINE=django.db.backends.postgresql" >> .env.dev
    echo "SQL_DATABASE=webapp_dev" >> .env.dev
    echo "SQL_USER=webapp" >> .env.dev
    echo "SQL_PASSWORD=webapp" >> .env.dev
    echo "SQL_HOST=db" >> .env.dev
    echo "SQL_PORT=5432" >> .env.dev

Now we need to update DATABASE variable at webapp/settings.py as follow:

    #
    #
    # from :
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
    #
    #
    # to :
    DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
        }
    }

As a next step, we will update Dockerfile to install the appropriate packages required for Psycopg2

Build the new image and spin up the two containers:

    docker-compose up -d --build

Run the migrations:

    docker-compose exec web python manage.py migrate --noinput

## Gunicorn Setup

Change the directory of the working terminal to project root and continue :
!!! Activate venv if not activated

    pip install gunicorn
    pip freeze >> app/requirements.txt

Since we still want to use Django's built-in server in development, create a new compose file called docker-compose.prod.yml for production.


We will run Gunicorn rather than the Django development server. 
In addition we are going to remove the volume from the web service(webapp) since we don't need it in production. 

As a newt step we are going to use separate environment variable files for both 'development' and production.
Environment variables differs from development to production and that is the reason of why are using seperate 
environment variable files to define environment variables for both services that will be passed to the container at runtime.

Let's create and update ".env.prod" file at the root directory of project:

    touch .env.prod

    echo "DEBUG=0" >> .env.prod
    echo "SECRET_KEY=change_me" >> .env.prod
    echo "DJANGO_ALLOWED_HOSTS=localhost 0.0.0.0 [::1]" >> .env.prod
    echo "SQL_ENGINE=django.db.backends.postgresql" >> .env.prod
    echo "SQL_DATABASE=webapp_prod" >> .env.prod
    echo "SQL_USER=webapp" >> .env.prod
    echo "SQL_PASSWORD=webapp" >> .env.prod
    echo "SQL_HOST=db" >> .env.prod
    echo "SQL_PORT=5432" >> .env.prod
    echo "DATABASE=postgres" >> .env.prod
<!--  -->

    touch .env.prod.db

    echo "POSTGRES_USER=webapp" >> .env.prod.db
    echo "POSTGRES_PASSWORD=webapp" >> .env.prod.db
    echo "POSTGRES_DB=webapp_prod" >> .env.prod.db

Bring down the development containers (and the associated volumes with the -v flag):

    docker-compose down -v

Then, build the production images and spin up the containers:

    docker-compose -f docker-compose.prod.yml up -d --build

