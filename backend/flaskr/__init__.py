import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
CATEGORIES_PER_PAGE = 6

def paginate_questions(request, selection):
  page = request.args.get("page", 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

def paginate_categories(request, selection):
  page = request.args.get("page", 1, type=int)
  start = (page - 1) * CATEGORIES_PER_PAGE
  end = start + CATEGORIES_PER_PAGE

  categories = [category.format() for category in selection]
  current_categories = categories[start:end]

  return current_categories

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app) #resources={"/*" :{origins: '*'}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization, true")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,PATCH,DELETE,OPTIONS")
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    
    categories = Category.query.all()
    formatted_categories = paginate_categories(request, categories)
    #[category.format() for category in categories]

    if len(categories) == 0:
      abort(404)
    
    return jsonify({
      "success": True,
      "categories": formatted_categories
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():

    questions = Question.query.all()
    formatted_questions = paginate_questions(request, questions)
    categories = Category.query.all()

    if len(categories) == 0:
      abort(404)

    return jsonify({
      "success": True,
      "questions": formatted_questions,
      "total_questions": len(questions),
      "current category": None,
      "categories": {category.id: category.type for category in categories}
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):

    try:

      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()
      questions = Question.query.all()
      formatted_questions = paginate_questions(request, questions)

      return jsonify({
        "success": True,
        "deleted question": question_id,
        "message": "This question has been deleted",
        "questions": formatted_questions
      })
    
    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  #Note to self: Was unable to view the frontend for /add and /quizzes after writing backend code. Check.

  @app.route('/questions', methods=['POST'])
  def add_question():

    body = request.get_json()
    
    new_question = body.get('question', None)
    answer_text = body.get('answer', None)
    difficulty_score = body.get('difficulty', None)
    new_category = body.get('category', None)

    searchTerm = body.get('searchTerm', None)
    
    try:
      
      if searchTerm:
        questions = Question.query.filter(Question.question.ilike('%' + searchTerm + '%')).all()

        formatted_questions = [question.format() for question in questions]

        return jsonify({
          "success": True,
          "questions": formatted_questions,
          "total_questions": len(formatted_questions)
        })

      else:
        question = Question(question=new_question, answer=answer_text, difficulty=difficulty_score, category=new_category)
        question.insert()

        questions = Question.query.order_by(Question.id).all()
        formatted_questions = paginate_questions(request, questions)
        
        return jsonify({
          "success": True,
          #"message": "Your question has been added",
          "added question": question.id,
          "questions": formatted_questions,
          "total_questions": len(questions)
        })
      
    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  #Note to self: this conflicts as a stand alone with the get_questions route. Input it as an "if" statement.

  # @app.route('/questions', methods=['POST'])
  # def search_questions():
    
  #   body = request.get_json()
  #   searchTerm = body.get('searchTerm', None)

  #   if searchTerm:
  #     questions = Question.query.filter(Question.question.ilike('%' + searchTerm + '%')).all()
      
  #     formatted_questions = paginate_questions(request, questions)

  #     return jsonify({
  #       "success": True,
  #       "questions": formatted_questions, #[question.format() for question in questions],
  #       "total_questions": len(questions)
  #     })

  #   else:
  #     abort(400)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):

    try:

      questions = Question.query.order_by(Question.id).filter(Question.category == category_id).all()
      formatted_questions = paginate_questions(request, questions)

      return jsonify({
        "success": True,
        "questions": formatted_questions,
        "total_questions": len(questions)
      })
    
    except:
      abort(422)
  
  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  
  @app.route('/quizzes', methods=['POST'])
  def get_quizzes():
    try:
        body = request.get_json()
        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)
        category_id = quiz_category['id']
      
    #Referenced https://github.com/BenMini/TriviaAPI and
    #https://stackoverflow.com/questions/26182027/how-to-use-not-in-clause-in-sqlalchemy-orm-query
    #on how to use .notin_()

        if category_id == 0:
            questions = Question.query.filter(
                Question.id.notin_(previous_questions)).all()

        else:
            questions = Question.query.filter(
                Question.id.notin_(previous_questions),
                Question.category == category_id).all()
    
    #referenced https://www.w3schools.com/python/ref_random_choices.asp on random.choice()

        question = None
        if questions:
            question = random.choice(questions)

        return jsonify({
            "success": True,
            "question": question.format()
        })

    except:
      abort(422)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "Resource Not Found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "Not Processable"
      }), 422
  
  app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "Bad Request"
      }), 400


  return app

    