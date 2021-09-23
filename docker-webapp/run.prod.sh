docker-compose -f docker-compose.prod.yml down -v --remove-orphans
docker-compose -f docker-compose.prod.yml exec web python manage.py makemigrations --noinput
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput


----------------------------------------------------
----------------------------------------------------
You can also verify in the logs via : docker-compose -f docker-compose.prod.yml logs -f 
----------------------------------------------------
----------------------------------------------------
echo 'You should be able to upload an image at http://localhost:1337/admin'
----------------------------------------------------
----------------------------------------------------


