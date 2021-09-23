docker-compose down -v --remove-orphans

docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear

echo "Upload an image at http://localhost:1337/"
echo "Then, view the image at http://localhost:1337/media/IMAGE_FILE_NAME"