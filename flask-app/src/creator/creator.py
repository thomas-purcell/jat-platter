from flask import Blueprint, request, jsonify, make_response
import json
from src import db
import logging

creator = Blueprint('creator', __name__)
logger = logging.getLogger('platter')

@creator.route('/recipes', methods=['GET', 'POST'])
def recipes():
    if request.method == 'GET':
        cursor = db.get_db().cursor()
        query = '''
            SELECT creatorID, recipeID, title, description, servings, difficulty, originID, categoryID, date_created
            FROM Recipes
            ORDER BY date_created DESC
        '''

        cursor.execute(query)
        column_headers = [x[0] for x in cursor.description]
        json_data = []
        theData = cursor.fetchall()
        for row in theData:
            json_data.append(dict(zip(column_headers, row)))
        return jsonify(json_data)
    elif request.method == 'POST':
        try:
            cursor = db.get_db().cursor()
            body = request.get_json()

            insert_recipe = '''
                INSERT INTO Recipes (creatorID, title, description, servings, difficulty, originID, categoryID)
                values (%s, %s, %s, %s, %s, %s, %s)
            '''

            if str(body['cuisine_origin']) == '':
                originId = None
            else:
                originId = int(body['cuisine_origin'])

            if str(body['category']) == '':
                categoryId = None
            else:
                categoryId = int(body['category'])

            recipe_data = (
                int(body['creatorID']), 
                str(body['title']), 
                str(body['description']), 
                int(body['servings']), 
                str(body['difficulty']), 
                originId,
                categoryId
            )

            cursor.execute(insert_recipe, recipe_data)
            db.get_db().commit()

            recipeID = str(cursor.lastrowid)

            insert_instruction = '''
                INSERT INTO Instructions (instructionID, recipeID, cookTime, prepTime)
                values (%s, %s, %s, %s)
            '''

            instruction_data = (int(recipeID), int(recipeID), int(body['cook_time']), int(body['prep_time']))
            cursor.execute(insert_instruction, instruction_data)
            db.get_db().commit()
            
            return recipeID
        except Exception as e:
            logger.exception(e)
            return 'Could not create new recipe', 400

# Gets the recipe with the given id 
@creator.route('/recipes/<recipeID>', methods=['GET'])
def get_recipes_id(recipeID):
    cursor = db.get_db().cursor()
    query = '''
    SELECT *
    FROM Recipes
    WHERE recipeID = {0};
    '''.format(recipeID)

    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

# Deletes the recipe with the given id 
@creator.route('/recipes/<recipeID>', methods=['DELETE'])
def del_recipes_id(recipeID):
    cursor = db.get_db().cursor()
    query = '''
    DELETE FROM Recipes
    WHERE recipeID = {0};
    '''.format(recipeID)

    cursor.execute(query)
    db.get_db().commit()

    return 'Success'

# Updates the name of the recipe with the given id 
@creator.route('/recipes/<recipeID>', methods=['PUT'])
def put_recipes_id(recipeID):
    cursor = db.get_db().cursor()
    body = request.get_json()

    title = str(body['title'])

    query = '''
    UPDATE Recipes
    SET title = '{0}'
    WHERE recipeID = {1};
    '''.format(title, recipeID)

    cursor.execute(query)
    db.get_db().commit()

    return 'Success'

# Gets all recipes for the given user 
@creator.route('/creator/<creatorID>/recipes', methods=['GET'])
def get_creator_public_recipes(creatorID):
    cursor = db.get_db().cursor()
    query = '''
    SELECT recipeID, title, servings, difficulty, description, originID, categoryID, date_created
    FROM Recipe_Creator
    JOIN Recipes USING (creatorID)
    WHERE creatorID = {0};
    '''.format(creatorID)

    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

# Gets all users following the creator with the given id
@creator.route('/creator/<creatorID>/following')
def get_creator_followers(creatorID):
    cursor = db.get_db().cursor()
    query = '''
    SELECT Following.criticID
    FROM Recipe_Creator
    JOIN Following USING (creatorID)
    WHERE creatorID = {0};
    '''.format(creatorID)

    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

# Gets a list of all recipe creator accounts
@creator.route('/accounts/creator', methods=['GET'])
def get_creators():
    cursor = db.get_db().cursor()
    query = '''
    SELECT *
    FROM Recipe_Creator;
    '''
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

# Gets the recipe creator account with the given id 
@creator.route('/accounts/creator/<creatorID>', methods=['GET', 'PUT'])
def get_creator_from_id(creatorID):
    if request.method == 'GET':
        cursor = db.get_db().cursor()
        query = '''
        SELECT *
        FROM Recipe_Creator
        WHERE creatorID = {0};
        '''.format(creatorID)
        cursor.execute(query)
        column_headers = [x[0] for x in cursor.description]
        json_data = []
        theData = cursor.fetchall()
        for row in theData:
            json_data.append(dict(zip(column_headers, row)))
        return jsonify(json_data)
    elif request.method == 'PUT':

        body = request.get_json()
        firstName = body['firstName']
        lastName = body['lastName']

        query = f'''
            UPDATE Recipe_Creator SET fName=\'{firstName}\', lName=\'{lastName}\' WHERE creatorId={str(creatorID)};
        '''
        cursor = db.get_db().cursor()
        cursor.execute(query)
        db.get_db().commit()

        return 'Success'

# Gets a list of reviews for the specified recipe
@creator.route('/recipes/<recipeID>/review', methods=['GET'])
def get_recipe_reviews(recipeID):
    cursor = db.get_db().cursor()
    query = '''
    SELECT reviewID, stars, comment, criticID, date_reviewed
    FROM Recipes
    JOIN Reviews USING (recipeID)
    WHERE recipeID = {0};
    '''.format(recipeID)

    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

# Gets all of the instructions for the given recipe
@creator.route('/recipes/<recipeID>/instructions', methods=['GET', 'POST'])
def get_recipe_instructions(recipeID):
    if request.method == 'GET':
        cursor = db.get_db().cursor()
        query = '''
        SELECT instructionID, cookTime, prepTime, step, stepNum
        FROM Recipes
        JOIN Instructions USING (recipeID)
        JOIN Instruction_Step USING (instructionID)
        WHERE Recipes.recipeID = {0};
        '''.format(recipeID)

        cursor.execute(query)
        column_headers = [x[0] for x in cursor.description]
        json_data = []
        theData = cursor.fetchall()
        for row in theData:
            json_data.append(dict(zip(column_headers, row)))
        return jsonify(json_data)
    elif request.method == 'POST':
        try:
            cursor = db.get_db().cursor()
            insert_step = '''
                INSERT INTO Instruction_Step (instructionID, recipeID, step, stepNum)
                values (%s, %s, %s, %s)
            '''
            body = request.get_json()
            step_data = (int(recipeID), int(recipeID), str(body['instruction_step_description']), int(body['instruction_step_number']))
            cursor.execute(insert_step, step_data)
            db.get_db().commit()
            return 'Success!', 200
        except Exception as e:
            logger.exception(e)
            return 'Could not create new recipe instruction', 400


@creator.route('/categories', methods=['POST'])
def categories():
    try:
        cursor = db.get_db().cursor()
        insert_stmt = '''
            INSERT INTO Categories (course, dietType)
            values (%s, %s)
        '''
        body = request.get_json()
        data = (str(body['course_name']), str(body['diet_type']))
        cursor.execute(insert_stmt, data)
        db.get_db().commit()

        return 'Success!'
    except Exception as e:
        logger.exception(e)
        return 'Could not create new category', 400

@creator.route('/cuisine', methods=['POST'])
def cuisine():
    try: 
        cursor = db.get_db().cursor()
        insert_stmt = '''
            INSERT INTO Cuisine_Origins (Origin, Description)
            values (%s, %s)
        '''
        body = request.get_json()
        data = (str(body['origin_region']), str(body['origin_description']))
        cursor.execute(insert_stmt, data)
        db.get_db().commit()

        return 'Success!'
    except Exception as e:
        logger.exception(e)
        return 'Could not create new cuisine origin', 400


@creator.route('/ingredients', methods=['POST'])
def ingredients():
    try:
        cursor = db.get_db().cursor()
        insert_stmt = '''
            INSERT INTO Ingredients (name)
            values (%s)
        '''
        body = request.get_json()
        data = (str(body['ingredient_name']))
        cursor.execute(insert_stmt, data)
        db.get_db().commit()

        return 'Success!'
    except Exception as e:
        logger.exception(e)
        return 'Could not create new ingredient', 400

@creator.route('/recipes/<recipeID>/ingredients', methods=['POST', 'DELETE'])
def recipe_ingredients(recipeID):
    if request.method == 'POST':
        try:
            cursor = db.get_db().cursor()
            insert_stmt = '''
                INSERT INTO Recipe_Ingredients (ingredientID, recipeID, amount, unit)
                values (%s, %s, %s, %s)
            '''
            body = request.get_json()
            data = (int(body['recipe_ingredient']), int(recipeID), float(body['recipe_ingredient_amount']), str(body['recipe_ingredient_unit']))
            cursor.execute(insert_stmt, data)
            db.get_db().commit()
            
            return 'Success!'
        except Exception as e:
            logger.exception(e)
            return 'Could not add new recipe ingredient', 400
    elif request.method == 'DELETE':
        try:
            cursor = db.get_db().cursor()
            delete_stmt = '''
                DELETE FROM Recipe_Ingredients WHERE recipeID = %s AND ingredientID = %s
            '''
            body = request.get_json()
            data = (int(recipeID), int(body['ingredientID']))
            cursor.execute(delete_stmt, data)
            db.get_db().commit()

            return 'Success!'
        except Exception as e:
            logger.exception(e)
            return 'Could not delete recipe ingredient', 400
