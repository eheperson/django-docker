
## Project directory structure 

docker-compose-example
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
        ├── .gitignore
        ├── .git/
        ├── .dockerignore.
        ├── .env.dev
        ├── docker-compose.django.yml.old
        ├── docker-compose.yml
        └── readme.md

## Django Setup

Prepare the environment

    mkdir docker-compose-example
    cd docker-compose-example
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
    rm app/requirements.txt
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

Verify that the webapp_prod database was created along with the default Django tables. 
Test out the admin page at http://localhost:8000/admin. 
<!--  -->
!! The static files are not being loaded anymore. 
This is expected since Debug mode is off. We'll fix this shortly.

## Production Dockerfile 

Did you notice that we're still running the database flush (which clears out the database) and migrate commands every time the container is run? This is fine in development, 

but let's create a new entrypoint file for production.

    touch app/entrypoint.prod.sh
    # check the app/entypoint.prod.sh file

Update the file permissions locally:

    $ chmod +x app/entrypoint.prod.sh

To use this  entrypoint.prod.sh file, 
create a new Dockerfile called Dockerfile.prod for use with production builds

    touch app/Dockerfile.prod

    # Here, we used a Docker multi-stage build to reduce the final image size. 
    # Essentially, builder is a temporary image that's used for building the Python wheels. 
    # The wheels are then copied over to the final production image and the builder image is discarded.

Did you notice that we created a non-root user? 
By default, Docker runs container processes as root inside of a container. 
This is a bad practice since attackers can gain root access to the 
Docker host if they manage to break out of the container. 
If you're root in the container, you'll be root on the host.

Update the web service within the docker-compose.prod.yml file to build with Dockerfile.prod:

    The old  docker-compose.prod.yml saved as docker-compose.prod.old.yml

Now, Try it out:

    docker-compose -f docker-compose.prod.yml down -v
    docker-compose -f docker-compose.prod.yml up -d --build
    docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput

## Nginx Setup

Next, let's add Nginx into the mix to act as a reverse proxy for 
Gunicorn to handle client requests as well as serve up static files.

Add the service to docker-compose.prod.yml:

    nginx:
        build: ./nginx
        ports:
            - 1337:80
        depends_on:
            - web
    # old docker-compose.prod.yml saved as docker-compose.prod.beforenginx.yml

Then, in the local project root, create the following files and folders:

    └── nginx
        ├── Dockerfile
        └── nginx.conf
<!--  -->

    # cd to  docker-compose-example/

    mkdir nginx
    cd nginx

    touch Dockerfile
    touch nginx.conf

Update docker-compose-example/nginx/Dockerfile as follow :

    echo "FROM nginx:1.21-alpine" >> Dockerfile
    echo "" >> Dockerfile
    echo "RUN rm /etc/nginx/conf.d/default.conf" >> Dockerfile
    echo "COPY nginx.conf /etc/nginx/conf.d" >> Dockerfile

Update docker-compose-example/nginx/nginx.conf as follow : 

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
        }

    }

Then, update the web service, in docker-compose.prod.yml, replacing ports with expose:

    web:
        build:
            context: ./app
            dockerfile: Dockerfile.prod
        command: gunicorn webapp.wsgi:application --bind 0.0.0.0:8000
        expose:
            - 8000
        env_file:
            - ./.env.prod
        depends_on:
            - db
    # the docker-compose.prod.yml file before this step saved as docker-compose.prod.beforenginxstep2.yml

    # Now, port 8000 is only exposed internally, to other Docker services. 
    # The port will no longer be published to the host machine.

Now, Test it out again :

    docker-compose -f docker-compose.prod.yml down -v
    docker-compose -f docker-compose.prod.yml up -d --build
    docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput

Ensure the app is up and running at http://localhost:1337.

Bring the containers down once done:

    docker-compose -f docker-compose.prod.yml down -v

## Settings for static files 

### Static files for development side

Since Gunicorn is an application server, it will not serve up static files. 
So, how should both static and media files be handled in this particular configuration?

Update settings.py:

    STATIC_URL = "/static/"
    STATIC_ROOT = BASE_DIR / "staticfiles"

Now, any request to http://localhost:8001/static/* will be served from the "staticfiles" directory.

To test, first re-build the images and spin up the new containers per usual. Ensure static files are still being served correctly at http://localhost:8001/admin.

localhost:8001 setting is in docker-compose.yml  file

    docker-compose -f docker-compose.yml down -v
    docker-compose -f docker-compose.yml up -d --build
    docker-compose -f docker-compose.yml exec web python manage.py migrate --noinput

### Static files for production side

For production, add a volume to the web and nginx services 
in docker-compose.prod.yml so that each container will share a directory named "staticfiles":

    old docker-compose.prod.yml renamed as docker-compose.prod.beforestaticprod.yml

We need to also create the "/home/app/web/staticfiles" folder in Dockerfile.prod:
add following files to app/Dockerfile.prod
the app/Dockerfile.prod renamed as app/Dockerfile.beforestatic.prod

    #just a new line added  below "# create the appropriate directories" :

    RUN mkdir $APP_HOME/staticfiles



Why is this necessary?

Docker Compose normally mounts named volumes as root. And since we're using a non-root user, we'll get a permission denied error when the collectstatic command is run if the directory does not already exist

To get around this, you can either:

Create the folder in the Dockerfile (source)
Change the permissions of the directory after it's mounted (source)
We used the former.

Next, update the Nginx configuration to route static file requests to the "staticfiles" folder:

    # the nginx.conf file before this step renamed as nginx.conf.old

Spin down the development containers:

    docker-compose down -v

Now let's test : 

    docker-compose -f docker-compose.prod.yml up -d --build
    docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
    docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear

Again, requests to http://localhost:1337/static/* will be served from the "staticfiles" directory.

Navigate to http://localhost:1337/admin and ensure the static assets load correctly.

You can also verify in the logs 
    
     via docker-compose -f docker-compose.prod.yml logs -f 
 
that requests to the static files are served up successfully via Nginx:

Bring the containers once done:

    docker-compose -f docker-compose.prod.yml down -v

# Serving Media files

## Serving Media file for Development side

To test out the handling of media files, start by creating a new Django app:

    docker-compose up -d --build
    docker-compose exec web python manage.py startapp upload

Add the new app to the INSTALLED_APPS list in settings.py:

    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",

        "upload",
    ]

update app/upload/views.py: 

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

Add a "templates", directory to the "app/upload" directory, and then add a new template called upload.html:

    touch /app/upload/templates/upload.html
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

update app/webapp/urls.py: 

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

app/webapp/settings.py:

    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "mediafiles"

Now, let's test :

    docker-compose -f docker-compose.yml down -v
    docker-compose -f docker-compose.yml up -d --build
    docker-compose -f docker-compose.yml exec web python manage.py migrate --noinput

You should be able to upload an image at http://localhost:8001/, and then view the image at http://localhost:8001/media/IMAGE_FILE_NAME.

## Serving Media file for Production side

For production, add another volume to the web and nginx services:

    old docker-compose.prod.yml renamed as docker-compose.prod.beforemediafiles.yml


We need to also create the "/home/app/web/mediafiles" folder in Dockerfile.prod:
add following line to app/Dockerfile.prod
the app/Dockerfile.prod renamed as app/Dockerfile.beforemedia.prod

    #just a new line added  below "# create the appropriate directories" :

    RUN mkdir $APP_HOME/mediafiles

Update the Nginx config again:

    # actual nginx.conf renamed as nginx.beforemedia.conf

Re-build:

    docker-compose down -v

    docker-compose -f docker-compose.prod.yml up -d --build
    docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
    docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear

Test it out one final time:

    Upload an image at http://localhost:1337/.
    Then, view the image at http://localhost:1337/media/IMAGE_FILE_NAME.