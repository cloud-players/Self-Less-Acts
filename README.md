# Selfie-Less-Acts
A photo sharing web app being hosted on AWS Cloud.

SelfieLessActs app is used to store information about anything that is good for the society that we observe.

Examples of such acts could be
- Picking up a piece of garbage and dumping it in a garbage can
- Road getting laid in your area
- Someone helping a blind man cross the road.
- You helping your mother at home in the kitchen.

The SelfieLessActs application will allow users of the application to upload image of the act with a small caption and categories. A user of the application will be presented with a screen that,
- Shows them lists of categories on which Acts have been shared. An act is a combination of an image and a caption for that image.
- Allows them to select to a topic.
- On selection, they will be shown all Acts in a category sorted in reverse chronological order (latest image first).
- Upvote a particular Act.
- Upload an Act.
- Delete an Act

## Tools Used

- **Django-REST-Framework** - to implement server side API endpoints.
- **SQLite3** - DataBase system to store information about Acts.
- **JavaScript** - To implement Client's Web App dynamically.
- **XMLHttpRequest** - To make a request to server to get or post the data.

## Stepts to build any project from the list of projects/microservices in serverfiles
- cd serverfiles
- python <project_name>/manage.py makemigrations
- python <project_name>/manage.py migrate
- python <project_name>/manage.py runserver 0:<port_number>


## License

This project is made available under the [MIT License](http://www.opensource.org/licenses/mit-license.php).

## Credits 

This project is being developed and maintained by [Nikhil V Revankar](https://github.com/nikhil3198), [Manjunath Badrannavar](https://github.com/mbbs4461) and [Nihal Pawar](https://github.com/NihalPawar).
