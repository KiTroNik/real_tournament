# Real Tournament

Real tournament is a quiz game which you can play with your friends. It offers multiple rooms and communication via sockets.

## Installation

### In the root directory of the project:

Create virtual environment.

```bash
python3 -m venv myenv
```

Activate virtual environment.

```bash
source myenv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Run migrations.

```bash
python manage.py migrate
```

Start the server.

```bash
python manage.py runserver
```

Now you can go to http://127.0.0.1:8000/ and enjoy the quiz.

## Usage

To create or join the games you must create an account.
If you have account go to create game or join game and type id of your room.
If you are creator give id to your friends and wait for them, then start the game.


## Technologies 

* Python
* Javascript
* Django
* Django-Channels
* Django-rest-framework
* Redis
* SQlite3
