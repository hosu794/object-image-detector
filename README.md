# image-objects-detector

# How to run application

docker-compose run app python manage.py migrate
docker-compose up -d

# How to run tests
docker-compose run app python manage.py test

# How to initialize static files 
docker-compose run app python manage.py collectstatic




