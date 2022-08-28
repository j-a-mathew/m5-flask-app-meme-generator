from audioop import add
from lib2to3.pgen2 import token
from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Meme, meme_schema, memes_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
# test to make sure data can be read by Insomnia
def getdata():
    return {'yes': 'm'}

# Add a meme to the database
@api.route('/memes', methods = ['POST'])
@token_required
def create_meme(current_user_token):
    name = request.json['name']
    user_token = current_user_token.token

    print(f'Printing TOKEN: {current_user_token.token}')

    meme = Meme(name, user_token=user_token)

    db.session.add(meme)
    db.session.commit()

    response = meme_schema.dump(meme)
    return jsonify(response)

# Get all memes by user
@api.route('/memes', methods = ['GET'])
@token_required
def get_memes(current_user_token):
    a_user = current_user_token.token
    memes = Meme.query.filter_by(user_token = a_user).all()
    response = memes_schema.dump(memes)
    return jsonify(response)

# Get a single meme
@api.route('/memes/<id>', methods = ['GET'])
@token_required
def get_single_meme(current_user_token, id):
    meme = Meme.query.get(id)
    response = meme_schema.dump(meme)
    return jsonify(response)

# Update a meme
@api.route('/memes/<id>', methods = ['POST', 'PUT'])
@token_required
def update_meme(current_user_token, id):
    meme = Meme.query.get(id)
    meme.name = request.json['name']
    meme.user_token = current_user_token.token

    db.session.commit()
    response = meme_schema.dump(meme)
    return jsonify(response)

# Delete a meme
@api.route('/memes/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    meme = Meme.query.get(id)
    db.session.delete(meme)
    db.session.commit()
    response = meme_schema.dump(meme)
    return jsonify(response)