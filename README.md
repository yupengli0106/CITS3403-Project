# **Let's Go History!**

The project is based on MacOS. The aim of this project is to promote people to learn about some significant historical events and timelines through games on our website. It may be more interesting to play web games than to read boring textbooks. Players are randomly matched to historical questions from the database, and then enter the time in which that historical event occurred. Our system records the user's score and ranks them accordingly. As a result, users will be more motivated to learn historical knowledge for higher rankings.

## Getting Started

Activate the python virtual environment:

`$ . venv/bin/activate`

To run the app: before running the following command, you must ensure that the database is configured.

`$ python -m run`

To stop the app:

`$ ^C`

To exit the environment:

`$ deactivate`

### Prerequisites

Requires Python3, Flask, venv, and SQLite

### Installing

Install Python3: [Click here](https://realpython.com/installing-python/)

Setting up environment:

1. create the virtual environment:

   * Mac/Linux: `$ python3 -m venv venv`
   * Windows: `> py -3 -m venv venv`
2. activate the environemnt:

   * Mac/Linux: `$ . venv/bin/activate`
   * Windows: `> venv/Scripts/activate`
3. install Flask:
   `$ pip install flask`
4. install dependency:
   `$ pip install -r requirements.txt `

Install SQLite: [Click here](https://www.servermania.com/kb/articles/install-sqlite/ "sqlite")

Build the database:

`$ flask db init`   `$ flask db migrate`   `$ flask db upgrade`

 Run the app:

`$ python -m run`

## Running the tests

To run the unit test:

`$ python -m tests.UT  `

To run the selenium test:

`$ python -m tests.webTest `

### Break down into end to end tests

Unit tests: Mainly tested the functions of user registration, user login, administrator login, and administrator management the database, all functions are working well.

Selenium tests: Tested the web page functions for user to register, login, and play the game, all functions are working well.

## Deployment

* Running on [LocalHost](https://en.wikipedia.org/wiki/Localhost#:~:text=In%20computer%20networking%2C%20localhost%20is,any%20local%20network%20interface%20hardware.)

## Built With

* [Bootstrap](https://getbootstrap.com/docs/5.1/getting-started/introduction/) - The web framework used
* VSCode & Git

## Git Log

Please read `git-logs.txt` for details.

## Versioning

1.0

## Authors

* **Yupeng Li** - 22602567
* **Dongdong huang** - 22594433

## License

## Acknowledgments

Follow the Lectures and Workshops by *Tim*, and *Tom*.

[clipboard.js v2.0.11](https://clipboardjs.com/) Licensed MIT © *Zeno Rocha*

Quizzes from [TutorialSpoint](https://www.tutorialspoint.com/general_knowledge/general_knowledge_world_history_timeline.htm)
