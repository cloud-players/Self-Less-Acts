# Self-Less-Acts
A photo sharing web app being hosted on AWS Cloud.

SelfieLessActs app is used to store information about anything that is good for the society that we observe.

Examples of such acts could be
- Picking up a piece of garbage and dumping it in a garbage can
- Road getting laid in your area
- Someone helping a blind man cross the road.
- You helping your mother at home in the kitchen.

The SelfLessActs application will allow users of the application to upload image of the act with a small caption and categories. A user of the application will be presented with a screen that,
- Shows them lists of categories on which Acts have been shared. An act is a combination of an image and a caption for that image.
- Allows them to select to a topic.
- On selection, they will be shown all Acts in a category sorted in reverse chronological order (latest image first).
- Upvote a particular Act.
- Upload an Act.
- Delete an Act.

## Tools Used
- **Django-REST-Framework** - to implement server side API endpoints.
- **SQLite3** - DataBase system to store information about Acts.
- **Docker-Container** - To implement microservices.
- **JavaScript** - To implement Client's Web App dynamically.
- **XMLHttpRequest** - To make a request to server to get or post the data.

## Steps to install required libraries
```$ cd serverfiles```

```$ sudo apt install python3-pip```

```$ pip install -r requirements.txt```

## Steps to build any project from the list of projects/microservices in serverfiles
```$ cd serverfiles```

```$ python <project_name>/manage.py makemigrations```

```$ python <project_name>/manage.py migrate```

```$ python <project_name>/manage.py runserver 0:<port_number>```

Now monolithic REST service is being split up into two microservices - one catering to the user management, and another catering to the act management. These two microservices is being started in separate docker containers, running on one AWS instance. The microservices will talk to each other via their respective REST interfaces.

## Steps to build docker images and publish it into docker_hub repository
``` $ cd serverfiles/dockerized_apps/<project_name>```

``` $ docker build -t <project_name> .```

``` $ docker tag <project_name> <dockerID>/<project_name>:latest```

``` $ docker push <dockerID>/<project_name>:latest```

## Steps to create a docker network to have our containers communicate with each other  
``` $ docker network create <network_name>```

## Steps to run docker container from remote repository  
``` $ docker run --network=<network_name> -p <port_no>:80 --name=<project_name> -it <dockerID>/<project_name>:latest```

## Steps to run docker container from local repository
``` $ docker run --network=myNetwork -p <port_no>:80 -it <project_name>```

## License

This project is made available under the [MIT License](http://www.opensource.org/licenses/mit-license.php).

## Credits 

This project is being developed and maintained by [Nikhil V Revankar](https://github.com/nikhil3198), [Manjunath Bhadrannavar](https://github.com/mbbs4461) and [Nihal Pawar](https://github.com/NihalPawar).
