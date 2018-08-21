# BUILD A PRODUCT: StackOverflow-lite API
[![Build Status](https://travis-ci.org/kiburualex/StackOverFlowLiteApi.svg?branch=master)](https://travis-ci.org/kiburualex/StackOverFlowLiteApi)
<a href="https://codeclimate.com/github/kiburualex/StackOverFlowLiteApi/maintainability"><img src="https://api.codeclimate.com/v1/badges/c024f75da2dbf983f64b/maintainability" /></a>
[![Coverage Status](https://coveralls.io/repos/github/kiburualex/StackOverFlowLiteApi/badge.svg?branch=master)](https://coveralls.io/github/kiburualex/StackOverFlowLiteApi?branch=master)

## Introduction
* An API for the StackOverFLow hosted  **[```here:```](https://kiburualex.github.io/StackOverflow-Lite/UI/)**). front end app.
* StackOverFLowLite a platform where people can ask questions and provide answers. .

## Technologies used.
* **[Python](https://www.python.org/downloads/)**
* **[Flask](flask.pocoo.org/)**
* **[Flask-RESTPlus](http://flask-restplus.readthedocs.io/en/stable/)** 

## Link to heroku:
https://kiburu-stacklyte-api-heroku.herokuapp.com/

## [Pivotal Tacker API Stories](https://www.pivotaltracker.com/n/projects/2189516)

## Current endpoints

* #### Ask a question.
    `POST /api/v1/questions`: 
    ```
    headers = {content_type:application/json}

    {
        "id": 1,
        "title": "Build an API",
        "description": "How does one build an api",
        "user": "john doe",
        "answers": []
    }
    ```
* #### Fetch all questions.
    `GET /api/v1/questions`
    ```
    headers = {content_type:application/json}
    ```


* #### Fetch a specific question.   
    `GET /api/v1/questions/<id>` 
    ```
    headers = {content_type:application/json} 
    ```
    

* #### Provide an answer to a question.
    `POST /api/v1/questions/id/answer`:
    ```
    headers = {content_type:application/json}

    {
        "id": 1,
        "answer": "Sample Answer",
        "user": "Leah"
    }
    ```

* #### Delete a question.
    `DELETE /api/v1/questions/id/`:
    ```
    headers = {content_type:application/json}

    ```

## Installation guide and usage

 #### **Clone the repo.**
    ```
    $ git clone https://kiburualex.github.io/StackOverflow-Lite/UI/
    ```
 #### **Create virtual environment & Activate.**
    ```
    $ virtualenv -p python3 venv 
    $ source venv/bin/activate
    ```
 #### **Install Dependancies.**
    ```
    (myenv)$ pip install -r requirements.txt
    ```
#### **Run the app**
   ```
    (myenv)$ python run.py
   ```
#### **Run Tests**
  ```
  (myenv)$ pytest --cov=tests
  ```

