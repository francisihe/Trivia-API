# Full Stack API Final Project


## Full Stack Trivia

Trivia API powers the trivia app that enables friends play a trivia game to see the most knowledgeable about a subject matter. The application allows the following:

1. Display of questions - both all questions and by category. Questions show the question, category and difficulty rating by default and you can show/hide the answer.
2. Delete questions.
3. Adding new questions and answers.
4. Searching for questions based on a text query string.
5. Playing the quiz game, randomizing either all questions or within a specific category.

This is to practive application structure, implementation and testing of an API


## About the Stack

The application makes use of Flask and SQLAlchemy server on the backend, and React on the frontend.


### Backend
The backend API endpoints are defined in the `__init__.py` file located here *./backend/flaskr/`__init__.py`* with references to the models.py for DB and SQLAlchemy.

API tests are written in the *./backend/test_flaskr.py* file.


### Frontend

The frontend containing an already created React app serves data from the backend server.

The components QuestionView.js, FormView.js and Quizview.js define what endpoints to consume, what HTTP method is required and the requests made.

This demonstrates the skill of reading and understanding code to build out endpoints of the backend API


>View the [README within ./frontend for more details.](./frontend/README.md)
