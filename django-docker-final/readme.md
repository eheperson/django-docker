
#  FAQs for anyone

**Why we need seperated files for production and development sides**

* Environment variables differs from development to production and that is the reason of why are using seperate files.
* Did you notice that we created a non-root user? 
* By default, Docker runs container processes as root inside of a container. 
* This is a bad practice since attackers can gain root access to the 
* Docker host if they manage to break out of the container. 
* If you're root in the container, you'll be root on the host.
  
**Why we are using .env files**

* info will be added 

**Why dockerfiles are required**

* info will be added 

**What is the function of .yaml files**

* info will be added 

**Why volumes are required in .yaml**

* info will be added 

**What is the funcion of gunicorn**

* We will run Gunicorn rather than the Django development server. 
* In addition we are going to remove the volume from the web service(webapp) since we don't need it in production. 

**What is the function of nginx**

* Next, let's add Nginx into the mix to act as a reverse proxy for Gunicorn to handle client requests as well as serve up static files.

**Why entrypoint.prod.sh file is required**

* Did you notice that we're still running the database flush (which clears out the database) and migrate commands every time the container is run? This is fine in development, but let's create a new entrypoint file for production.

#  some NOTES

* Since Gunicorn is an application server, it will not serve up static files.
* So, how should both static and media files be handled in this particular configuration?

**Serving  staticfiles :**

    STATIC_URL = "/static/"
    STATIC_ROOT = BASE_DIR / "staticfiles"

* For production, add a volume to the web and nginx services in docker-compose.prod.yml so that each container will share a directory named "staticfiles":

* We need to also create the "/home/app/web/staticfiles" folder in Dockerfile.prod: 
  
    #add following files to main/Dockerfile.prod
    #just a new line added  below "# create the appropriate directories" :
    RUN mkdir $APP_HOME/staticfiles

*Why is this necessary?*

* Docker Compose normally mounts named volumes as root. And since we're using a non-root user, we'll get a permission denied error when the collectstatic command is run if the directory does not already exist

* To get around this, you can either :

    Create the folder in the Dockerfile (source)
    Change the permissions of the directory after it's mounted (source)
    Next, update the Nginx configuration to route static file requests to the "staticfiles" folder:

    location /static/ {
        alias /home/app/web/staticfiles/;
    }

* Serving  staticfiles :

    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "mediafiles"

    For production, add another volume to the web and nginx services:

    location /media/ {
        alias /home/app/web/mediafiles/;
    }

    We need to also create the "/home/app/web/mediafiles" folder in Dockerfile.prod:
    add following line to app/Dockerfile.prod
        #just a new line added  below "# create the appropriate directories" :
        RUN mkdir $APP_HOME/mediafiles


# Prepare the environment

    #create root directory for the whole project
    mkdir docker-webapp
    cd docker-webapp

    # let's create ignore files for docker and git
    touch .gitignore
    touch .dockerignore.

    # create and activate a virtual environment
    python3 -m venv venv
    source /venv/bin/activate

    # include venv/ directory to ignore files
    echo "# ignoring virtualenv directory" >> .gitignore
    echo "/venv/" >> .gitignore
    echo "# ignoring virtualenv directory" >> .dockerignore.
    echo "*/venv" >> .dockerignore.

    # include MacOS files to ignore files
    echo "# ignoring MacOS files" >> .gitignore
    echo ".DS_Store" >> .gitignore
    echo "# ignoring MacOS files" >> .dockerignore.
    echo ".DS_Store" >> .dockerignore.

    # install requirement dependencies
    pip install django
    pip install gunicorn
    pip install psycopg2

    # create a directory for django project
    mkdir main
    cd main

    # start django project within directory created at last step
    django-admin startproject webpapp .

    # get rid of some required processes
    python manage.py makemigrations
    python manage.py migrate

    # create a requirements.txt file
    pip freeze >> requirements.txt

    # we need to create seperate Dockerfiles for development and production sides for the project itself
    # docker-webapp/main/Dockerfile.dev
    # docker-webapp/main/Dockerfile.prod
    touch Dockerfile.dev
    touch Dockerfile.prod

    # we will create an entrypoint file within main/ dir
    # information about entry file will be added later.
    # docker-webapp/main/entrypoint.prod.sh
    touch entrypoint.prod.sh
    #update the entrypoint file permissions
    chmod +x entrypoint.prod.sh

    # as a next step we are going to create seperated .env files to serve our secret parameters
    # we have to create .env files at root directory of project
    # docker-webapp/.env.dev
    # docker-webapp/.env.prod
    # docker-webapp/.env.prod.db
    touch .env.dev
    touch .env.prod
    touch .env.prod.db

    # we have to add .env files to ignore files 
    # because of the security
    echo "# ignore .env files " >> .gitignore
    echo ".env.dev" >> .gitignore
    echo ".env.prod" >> .gitignore
    echo ".env.prod.db" >> .gitignore
    echo "# ignore .env files " >> .dockerignore.
    echo ".env.dev" >> .dockerignore.
    echo ".env.prod" >> .dockerignore.
    echo ".env.prod.db" >> .dockerignore.

    # we have to create some .yml files for docker-compose 
    # Also .yml files being seperated for both development and production sides 
    # docker-webapp/docker-compose.prod.yml
    # docker-webapp/docker-compose.dev.yml
    touch docker-compose.prod.yml
    touch docker-compose.dev.yml

    # As a next step we are going to set our nginx server
    # we need to create an /nginx directory within the root directory of project
    # then create "Dockerfile" and "nginx.conf" files inside of nginx/ directory
    # docker-webapp/nginx/Dockerfile
    # docker-webapp/nginx/nginx.conf
    mkdir nginx
    touch nginx/Dockerfile
    touch nginx/nginx.conf

    # before the last step create a readme file
    # docker-webapp/README.md
    touch README.md

    # to automate run process create seperated bash files for both development and production
    # docker-webapp/run.dev.sh
    # docker-webapp/run.prod.sh

    # -------- additional -----------
    # to the purpose of the serving mediafiles and staticfiles with success create relational folder under main/ directory
    # docker-webapp/main/mediafiles/
    # docker-webapp/main/staticfiles/
    mkdir main/mediafiles
    mkdir main/staticfiles

After Preparation steps, project directory structure must be looks like follow :

    docker-webapp/
            ├── .dockerignore.
            ├── .env.dev
            ├── .env.prod
            ├── .env.prod.db
            ├── .git/
            ├── .gitignore
            └── main/
            │   ├── mediafiles/
            │   ├── staticfiles/
            │   ├── webapp/
            │   │   ├── __init__.py
            │   │   ├── asgi.py
            │   │   ├── settings.py
            │   │   ├── urls.py
            │   │   └── wsgi.py
            │   ├── Dockerfile.dev
            │   ├── Dockerfile.prod
            │   ├── entrypoint.prod.sh
            │   ├── manage.py
            │   └── requirements.txt
            ├── docker-compose.dev.yml
            ├── docker-compose.prod.yml
            ├── nginx/
            │   ├── Dockerfile
            │   └── nginx.conf
            ├── readme.md
            ├── run.dev.sh
            ├── run.prod.sh
            └── venv/
    
# Update .env Files 

    # first we will update .env.dev file:
    echo "DEBUG=1" >> .env.dev
    echo "SECRET_KEY=foo" >> .env.dev
    echo "DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]" >> .env.dev
    echo "SQL_ENGINE=django.db.backends.postgresql" >> .env.dev
    echo "SQL_DATABASE=webapp_dev" >> .env.dev
    echo "SQL_USER=webapp" >> .env.dev
    echo "SQL_PASSWORD=webapp" >> .env.dev
    echo "SQL_HOST=db" >> .env.dev
    echo "SQL_PORT=5432" >> .env.dev

<!--  -->

    # update .env.prod file
    echo "SDEBUG=0" >> .env.prod
    echo "SSECRET_KEY=change_me" >> .env.prod
    echo "SDJANGO_ALLOWED_HOSTS=localhost 0.0.0.0 [::1]" >> .env.prod
    echo "SSQL_ENGINE=django.db.backends.postgresql" >> .env.prod
    echo "SSQL_DATABASE=webapp_prod" >> .env.prod
    echo "SSQL_USER=webapp" >> .env.prod
    echo "SSQL_PASSWORD=webapp" >> .env.prod
    echo "SSQL_HOST=db" >> .env.prod
    echo "SSQL_PORT=5432" >> .env.prod
    echo "SDATABASE=postgres" >> .env.prod

<!--  -->

    # update .env.prod.db file
    echo "POSTGRES_USER=webapp" >> .env.prod.db
    echo "POSTGRES_PASSWORD=webapp" >> .env.prod.db
    echo "POSTGRES_DB=webapp_prod" >> .env.prod.db

# Update main/webapp/settings.py

    #docker-webapp/main/webapp/setting.py
    import os

    # SECRET_KEY = 'django-insecure-@k%qjsf%@9@v$i^_g==@%#l1*jkd2z2s$3&a53qq!yimv3__(z'
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # SECURITY WARNING: don't run with debug turned on in production!
    # DEBUG = True
    DEBUG = int(os.environ.get("DEBUG", default=0))

    # ALLOWED_HOSTS = []
    ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
    # 'DJANGO_ALLOWED_HOSTS' should be a single string of hosts with a space between each.
    # For example: 'DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'

<!--  -->

    #docker-webapp/main/webapp/setting.py

    # https://docs.djangoproject.com/en/3.2/ref/settings/#databases
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #         'NAME': BASE_DIR / 'db.sqlite3',
    #     }
    # }
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

<!--  -->

    #docker-webapp/main/webapp/setting.py

    # STATIC_URL = '/static/'
    STATIC_URL = "/static/"
    STATIC_ROOT = BASE_DIR / "staticfiles"

<!--  -->

    #docker-webapp/main/webapp/setting.py

    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "mediafiles"

# Update docker-compose.prod.yml file

    # Here, we used a Docker multi-stage build to reduce the final image size. 
    # Essentially, builder is a temporary image that's used for building the Python wheels. 
    # The wheels are then copied over to the final production image and the builder image is discarded.

    #docker-webapp/docker-compose.prod.yml
    version: '3.8'

    services:
        web:
            build:
                context: ./app
                dockerfile: Dockerfile.prod
            command: gunicorn webapp.wsgi:application --bind 0.0.0.0:8000
            volumes:
                - static_volume:/home/app/web/staticfiles
                - media_volume:/home/app/web/mediafiles
            expose:
                - 8000
            env_file:
                - ./.env.prod
            depends_on:
                - db
        db:
            image: postgres:13.0-alpine
            volumes:
                - postgres_data:/var/lib/postgresql/data/
            env_file:
                - ./.env.prod.db
        nginx:
            build: ./nginx
            volumes:
                - static_volume:/home/app/web/staticfiles
                - media_volume:/home/app/web/mediafiles
            ports:
                - 1337:80
            depends_on:
            - web

    volumes:
        postgres_data:
        static_volume:
        media_volume:

# Update docker-compose.dev.yml file

    #docker-webapp/docker-compose.dev.yml
    version: '3.8'

    services:
        web:
            build: 
                context: ./app
                dockerfile: Dockerfile.dev
            command: python manage.py runserver 0.0.0.0:8000
            volumes:
              - ./app/:/usr/src/app/
            ports:
              - 8000:8000
            env_file:
              - ./.env.dev
            depends_on:
              - db
        db:
            image: postgres:13.0-alpine
            volumes:
              - postgres_data:/var/lib/postgresql/data/
            environment:
              - POSTGRES_USER=webapp
              - POSTGRES_PASSWORD=webapp
              - POSTGRES_DB=webapp_dev

    volumes:
        postgres_data:

# Update main/Dockerfile.dev file

    #docker-webapp/main/Dockerfile.dev

    # pull official base image
    FROM python:3.9.6-alpine

    # set work directory
    WORKDIR /usr/src/app

    # set environment variables
    # Prevents Python from writing pyc files to disc 
    # (equivalent to python -B option)
    ENV PYTHONDONTWRITEBYTECODE 1
    # Prevents Python from buffering stdout and stderr 
    # (equivalent to python -u option)
    ENV PYTHONUNBUFFERED 1

    # install psycopg2 dependencies
    RUN apk update \
        && apk add postgresql-dev gcc python3-dev musl-dev

    # install dependencies
    RUN pip install --upgrade pip
    COPY ./requirements.txt .
    RUN pip install -r requirements.txt

    # copy project
    COPY . .

# Update main/Dockerfile.prod file

    #docker-webapp/main/Dockerfile.prod

    ###########
    # BUILDER #
    ###########

    # pull official base image
    FROM python:3.9.6-alpine as builder

    # set work directory
    WORKDIR /usr/src/app

    # set environment variables
    ENV PYTHONDONTWRITEBYTECODE 1
    ENV PYTHONUNBUFFERED 1

    # install psycopg2 dependencies
    RUN apk update \
        && apk add postgresql-dev gcc python3-dev musl-dev

    # lint
    RUN pip install --upgrade pip
    RUN pip install flake8==3.9.2
    COPY . .
    RUN flake8 --ignore=E501,F401 .

    # install dependencies
    COPY ./requirements.txt .
    RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


    #########
    # FINAL #
    #########

    # pull official base image
    FROM python:3.9.6-alpine

    # create directory for the app user
    RUN mkdir -p /home/app

    # create the app user
    RUN addgroup -S app && adduser -S app -G app

    # create the appropriate directories
    ENV HOME=/home/app
    ENV APP_HOME=/home/app/web
    RUN mkdir $APP_HOME
    RUN mkdir $APP_HOME/staticfiles
    RUN mkdir $APP_HOME/mediafiles
    WORKDIR $APP_HOME

    # install dependencies
    RUN apk update && apk add libpq
    COPY --from=builder /usr/src/app/wheels /wheels
    COPY --from=builder /usr/src/app/requirements.txt .
    RUN pip install --no-cache /wheels/*

    # copy entrypoint.prod.sh
    COPY ./entrypoint.prod.sh .
    RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.prod.sh
    RUN chmod +x  $APP_HOME/entrypoint.prod.sh

    # copy project
    COPY . $APP_HOME

    # chown all the files to the app user
    RUN chown -R app:app $APP_HOME

    # change to the app user
    USER app

    # run entrypoint.prod.sh
    ENTRYPOINT ["/home/app/web/entrypoint.prod.sh"]

# Update main/entrypoint.prod.sh file

    #!/bin/sh

    # docker-webapp/main/entrypoint.prod.sh

    if [ "$DATABASE" = "postgres" ]
    then
        echo "Waiting for postgres..."

        while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
        done

        echo "PostgreSQL started"
    fi

    exec "$@"

# Update nginx/Dockerfile file

    # webapp/nginx/Dockerfile 

    FROM nginx:1.21-alpine

    RUN rm /etc/nginx/conf.d/default.conf
    COPY nginx.conf /etc/nginx/conf.d

# Update nginx/nginx.conf file

    # webapp/nginx/nginx.conf

    upstream webapp {
        server web:8000;
    }

    server {

        listen 80;

        location / {
            proxy_pass http://webapp;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $host;
            proxy_redirect off;
            client_max_body_size 100M;
        }

        location /static/ {
            alias /home/app/web/staticfiles/;
        }

        location /media/ {
            alias /home/app/web/mediafiles/;
        }

    }

# Update automation bash files :

## run.dev.sh

    # web-app/run.dev.sh
    # cd to root directory of project
    echo "docker-compose -f docker-compose.dev.yml down -v --remove-orphans" >> run.dev.sh
    echo "docker-compose -f docker-compose.dev.yml up -d --build" >> run.dev.sh
    echo "docker-compose -f docker-compose.dev.yml exec web python manage.py makemigrations --noinput" >> run.dev.sh
    echo "docker-compose -f docker-compose.dev.yml exec web python manage.py migrate --noinput" >> run.dev.sh
    echo "" >> run.dev.sh
    echo "" >>run.dev.sh
    echo "----------------------------------------------------" >> run.dev.sh
    echo "----------------------------------------------------" >> run.dev.sh
    echo "You can also verify in the logs via : docker-compose -f docker-compose.prod.yml logs -f " >> run.dev.sh
    echo "----------------------------------------------------" >> run.dev.sh
    echo "----------------------------------------------------" >> run.dev.sh
    echo "echo 'You should be able to upload an image at http://localhost:8000/admin'" >> run.dev.sh
    echo "----------------------------------------------------" >> run.dev.sh
    echo "----------------------------------------------------" >> run.dev.sh
    echo "" >> run.dev.sh
    echo "" >> run.dev.sh

## run.prod.sh

    # web-app/run.prod.sh
    # cd to root directory of project
    echo "docker-compose -f docker-compose.prod.yml down -v --remove-orphans" >> run.prod.sh
    echo "docker-compose -f docker-compose.prod.yml up -d --build" >> run.dev.sh
    echo "docker-compose -f docker-compose.prod.yml exec web python manage.py makemigrations --noinput" >> run.prod.sh
    echo "docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput" >> run.prod.sh
    echo "" >> run.prod.sh
    echo "" >> run.prod.sh
    echo "----------------------------------------------------" >> run.prod.sh
    echo "----------------------------------------------------" >> run.prod.sh
    echo "You can also verify in the logs via : docker-compose -f docker-compose.prod.yml logs -f " >> run.prod.sh
    echo "----------------------------------------------------" >> run.prod.sh
    echo "----------------------------------------------------" >> run.prod.sh
    echo "echo 'You should be able to upload an image at http://localhost:1337/admin'" >> run.prod.sh
    echo "----------------------------------------------------" >> run.prod.sh
    echo "----------------------------------------------------" >> run.prod.sh
    echo "" >> run.prod.sh
    echo "" >> run.prod.sh

# Additional Section

In this section we will add a new django-app to our django-project

To create an app :

    # run this command in same directory with manage.py
    docker-compose exec web python manage.py startapp upload

Add the new app to the INSTALLED_APPS list in main/webapp/settings.py:

    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",

        "upload",
    ]

Update main/upload/views.py as follow :

    from django.shortcuts import render
    from django.core.files.storage import FileSystemStorage


    def image_upload(request):
        if request.method == "POST" and request.FILES["image_file"]:
            image_file = request.FILES["image_file"]
            fs = FileSystemStorage()
            filename = fs.save(image_file.name, image_file)
            image_url = fs.url(filename)
            print(image_url)
            return render(request, "upload.html", {
                "image_url": image_url
            })
        return render(request, "upload.html")

Add a "templates", directory to the "app/upload" directory, 
and then add a new template called upload.html:

    mkdir main/upload/templates/upload
    touch main/upload/templates/upload/upload.html

<!--  -->

    <!-- upload.html -->
    {% block content %}

        <form action="{% url "upload" %}" method="post" enctype="multipart/form-data">
            {% csrf_token %}
            <input type="file" name="image_file">
            <input type="submit" value="submit" />
        </form>

        {% if image_url %}
            <p>File uploaded at: <a href="{{ image_url }}">{{ image_url }}</a></p>
        {% endif %}

    {% endblock %}


Update main/webapp/views.py as follow :

    from django.contrib import admin
    from django.urls import path
    from django.conf import settings
    from django.conf.urls.static import static

    from upload.views import image_upload

    urlpatterns = [
        path("", image_upload, name="upload"),
        path("admin/", admin.site.urls),
    ]

    if bool(settings.DEBUG):
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

After tht we can run our app