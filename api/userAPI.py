import uuid
from flask import Flask, Blueprint, request, jsonify
from flask_cors import CORS
from firebase_admin import firestore

app = Flask(__name__)
CORS(app)

db = firestore.client()
user_Ref = db.collection('user')

userAPI = Blueprint('userAPI', __name__)

#Napraviti novog korisnika
@userAPI.route('/add', methods=['POST'])
def create():
    try:
        id = uuid.uuid4()
        user_Ref.document(id.hex).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Ocurred: {e}"

#Izlistati sve korisnike
@userAPI.route('/list')
def read():
    try:
        all_users = [doc.to_dict() for doc in user_Ref.stream()]
        return jsonify(all_users), 200
    except Exception as e:
        return f"AN Error Occurred {e}"
    
#Prikazati korisnika po ID-u
@userAPI.route('/get/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
       query = user_Ref.where('id' , '==', int(user_id)).stream()
       user = None
       for doc in query:
            user = doc.to_dict()
            break
       if user:
           return jsonify(user), 200
       else:
           return jsonify({'error' : 'User not found'}), 404
    except Exception as e:
        print(f"An Error Occurred: {e}")
        return jsonify({"error" : "Internal Server Error"}), 500

    
#Update korisnika po ID-u
@userAPI.route('/update/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        query = user_Ref.where('id', '==', int(user_id)).stream()
        user_doc = None
        for doc in query:
            user_doc = doc
            break
        if user_doc:
            user_Ref.document(user_doc.id).update(request.json)
            return jsonify({"success": True}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        print(f"An Error Occurred: {e}") 
        return jsonify({"error" : "Internal Server Error"}), 500

#Obrisati korisnika po ID-u
@userAPI.route('/delete/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        query = user_Ref.where('id', '==', int(user_id)).stream()
        user_doc = None
        for doc in query:
            user_doc = doc
            break
        if user_doc:
            user_Ref.document(user_doc.id).delete()
            return jsonify({"success": True}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        print(f"An Error Occurred: {e}")
        return jsonify({"error" : "Internal Server Error"}), 500


