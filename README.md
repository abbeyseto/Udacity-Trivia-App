# Full Stack Trivia API 


## Introduction
Flaskr Backend API gets the list of categories of questions in the trivia app.
The Trivia questions are sorted into categories and also rated based on difficulty

This API will give the functionality to:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 


## Overview
This API majorly uses 3 methods as listed in the table below
Most of the get requested do not require arguments.
- Request Arguments: None

You can read more about HTTP request methods

# About the Stack

This is a  full stack application desiged with some key functional areas:

## Backend

The `./backend` directory contains a completed Flask and SQLAlchemy server. You will work primarily in app.py to define your endpoints and can reference models.py for DB and SQLAlchemy setup. It uses a Postgress database

Full Documentation on how to use the API can be found here  [API Documentation](https://documenter.getpostman.com/view/4874547/Szf6WoLP)
### Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


## Frontend

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server. 

### Getting Setup

> _tip_: this frontend is designed to work with [Flask-based Backend](../backend). It is recommended you stand up the backend first, test using Postman or curl, update the endpoints in the frontend, and then the frontend should integrate smoothly.

### Installing Dependencies

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

>_tip_: **npm i** is shorthand for **npm install**

## Required Tasks

## Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

## Authentication
There are currently no authentication methods for this API. This will come in the subsequent versions.

You can call these endpoints from your domain as CORS is enabled and you should not have issues getting responses.

If there are issues, contact the details as seen at the Authors subheading.

# Error Codes
Flaskr Backend API uses standard error codes. Some of which are listed below with their meaning.

| Error Code | Error Message |
| ------- | ------ |
| 200 | Succesful |
| 404 | Not Found |
| 405 | Method not allowed |
| 422 | Unprocessable Entity |
| 500 | Internat server error |


## Rate limit
There are currently no rate limits to the API calls for Flaskr Backend API

## Author
> Adenle Abiodun  adenleabbey@hotmail.com
