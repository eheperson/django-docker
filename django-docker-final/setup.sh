#create root directory for the whole project
mkdir docker-webapp
cd docker-webapp

echo ""
echo " > project root directory is created : OK"
echo ""

# let's create ignore files for docker and git
touch .gitignore
touch .dockerignore.

echo ""
echo " > ignore files are created under docker-webapp/ : OK"
echo ""

# create and activate a virtual environment
python3 -m venv venv
#
echo ""
echo " > python virtualenvironment is created as 'venv' under docker-webapp/ : OK"
echo ""
#
source $PWD/venv/bin/activate
#
echo ""
echo " > 'venv' is activated : OK"
echo ""
#
# include venv/ directory to ignore files
echo "# ignoring virtualenv directory" >> .gitignore
echo "/venv/" >> .gitignore
echo "# ignoring virtualenv directory" >> .dockerignore.
echo "*/venv" >> .dockerignore.
#
echo ""
echo " > 'venv' is ignored : OK"
echo ""
#
# include MacOS files to ignore files
echo "# ignoring MacOS files" >> .gitignore
echo ".DS_Store" >> .gitignore
echo "# ignoring MacOS files" >> .dockerignore.
echo ".DS_Store" >> .dockerignore.
#
echo ""
echo " > MacOS files are ignored : OK"
echo ""
#
# install requirement dependencies
pip install django
pip install gunicorn
pip install psycopg2
#
echo ""
echo " > python dependencies are installed : OK"
echo ""
#
# create a directory for django project
mkdir main
cd main
#
echo ""
echo " > 'main/'  project directory is created: OK"
echo ""
#
# start django project within directory created at last step
django-admin startproject webpapp .
#
echo ""
echo " > django-project is created as 'main/webapp' : OK"
echo ""
#
# get rid of some required processes
python manage.py makemigrations
python manage.py migrate
#
echo ""
echo " > django-project initial migrations are done : OK"
echo ""
#
# create a requirements.txt file
pip freeze >> requirements.txt
#
echo ""
echo " > 'requirements.txt file is created : OK"
echo ""
#
# we need to create seperate Dockerfiles for development and production sides for the project itself
# docker-webapp/main/Dockerfile.dev
# docker-webapp/main/Dockerfile.prod
touch Dockerfile.dev
touch Dockerfile.prod
#
echo ""
echo " > Dockerfiles are created under 'main/webapp' : OK"
echo ""
#
# we will create an entrypoint file within main/ dir
# information about entry file will be added later.
# docker-webapp/main/entrypoint.prod.sh
touch entrypoint.prod.sh
#update the entrypoint file permissions
chmod +x entrypoint.prod.sh
#
echo ""
echo " > entrypoint.prod.sh under 'main/webapp' : OK"
echo ""
#
cd ..
#
# as a next step we are going to create seperated .env files to serve our secret parameters
# we have to create .env files at root directory of project
# docker-webapp/.env.dev
# docker-webapp/.env.prod
# docker-webapp/.env.prod.db
touch .env.dev
touch .env.prod
touch .env.prod.db
#
echo ""
echo " > .env files are created under 'main/webapp' : OK"
echo ""
#
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
#
echo ""
echo " > .env.dev file is updated: OK"
echo ""
#
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
#
echo ""
echo " > .env.prod file is updated: OK"
echo ""
#
# update .env.prod.db file
echo "POSTGRES_USER=webapp" >> .env.prod.db
echo "POSTGRES_PASSWORD=webapp" >> .env.prod.db
echo "POSTGRES_DB=webapp_prod" >> .env.prod.db
#
echo ""
echo " > .env.prod.db file is updated: OK"
echo ""
#
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
#
echo ""
echo " > .env files are ignored : OK"
echo ""
#
# we have to create some .yml files for docker-compose 
# Also .yml files being seperated for both development and production sides 
# docker-webapp/docker-compose.prod.yml
# docker-webapp/docker-compose.dev.yml
#
touch docker-compose.prod.yml
touch docker-compose.dev.yml
#
echo ""
echo " > .yaml files are created under docker-webapp/  : OK"
echo ""
#
# As a next step we are going to set our nginx server
# we need to create an /nginx directory within the root directory of project
# then create "Dockerfile" and "nginx.conf" files inside of nginx/ directory
# docker-webapp/nginx/Dockerfile
# docker-webapp/nginx/nginx.conf
mkdir nginx
touch nginx/Dockerfile
touch nginx/nginx.conf
#
echo ""
echo " > nginx files are created under docker-webapp/nginx/  : OK"
echo ""
#
# before the last step create a readme file
# docker-webapp/README.md
# touch README.md
#
# to automate run process create seperated bash files for both development and production
# docker-webapp/run.dev.sh
# docker-webapp/run.prod.sh
#
touch run.prod.sh
touch run.dev.sh
#
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
#
echo ""
echo " > run.dev.sh file is updated: OK"
echo ""
#
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
#
echo ""
echo " > run.prod.sh file is updated: OK"
echo ""
#
# -------- additional -----------
# to the purpose of the serving mediafiles and staticfiles with success create relational folder under main/ directory
# docker-webapp/main/mediafiles/
# docker-webapp/main/staticfiles/
mkdir main/mediafiles
#
echo ""
echo " > mediafiles/ directory are created under docker-webapp/main/  : OK"
echo ""
#
mkdir main/staticfiles
#
echo ""
echo " > staticfiles/ directory are created under docker-webapp/main/  : OK"
echo ""
#
echo ""
echo ""
echo "* * * * NOW U R A FREE HORSE! * * * *"
echo ""
echo ""
echo ":)"