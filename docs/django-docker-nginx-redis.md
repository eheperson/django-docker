

## Create Docker Network

    docker network create --subnet=168.100.0.1/16 app-net

## List Created Docker Networks
    
    docker network list

## Create and Start Mysql Database Container

    docker run -d --name app-db --cpus 0.5 --memory 512m -e MYQL_USER=ehe -e MYQL_ROOT_PASSWORD=root -e MYQL_DATABASE=web_app_db --net app-net mysql:5.7
<!--  -->
    docker ps
<!--  -->
    docker ps -a

## Create Web Application Container
    
    docker run -itd --name web-app-1 -v $PWD:/code --cpus 0.5 --memory 512m -p 8090:8090 --workdir /code --net app-net -e DOCKER_CONTAINER_ID=1 python:3.8

## To connect WebApp Container  terminal

    docker exec -it web-app-1 bash
