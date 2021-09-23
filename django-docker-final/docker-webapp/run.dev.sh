docker-compose -f docker-compose.dev.yml down -v --remove-orphans
docker-compose -f docker-compose.dev.yml up -d --build
docker-compose -f docker-compose.dev.yml exec web python manage.py makemigrations --noinput
docker-compose -f docker-compose.dev.yml exec web python manage.py migrate --noinput


----------------------------------------------------
----------------------------------------------------
You can also verify in the logs via : docker-compose -f docker-compose.prod.yml logs -f 
----------------------------------------------------
----------------------------------------------------
echo 'You should be able to upload an image at http://localhost:8000/admin'
----------------------------------------------------
----------------------------------------------------


docker-compose -f docker-compose.prod.yml up -d --build
