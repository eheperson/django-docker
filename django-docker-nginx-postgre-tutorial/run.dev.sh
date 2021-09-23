docker-compose -f docker-compose.yml down -v --remove-orphans
docker-compose -f docker-compose.yml up -d --build
docker-compose -f docker-compose.yml exec web python manage.py migrate --noinput

echo "You should be able to upload an image at http://localhost:8001/"
echo "then view the image at http://localhost:8001/media/IMAGE_FILE_NAME"
"