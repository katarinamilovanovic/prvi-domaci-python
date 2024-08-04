import uuid
from flask import Blueprint, request, jsonify
from firebase_admin import firestore

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
    print(user_id)
    print(f"Fetching user with ID: {user_id}")

    try:
        user = user_Ref.document(user_id).get()
        print(f"User fetched: {user.to_dict() if user.exists else 'None'}")
        if user.exists:
            print(f"User data: {user.to_dict()}")
            return jsonify(user.to_dict()), 200
        else:
            print("User not found")
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(f"An Error Occurred: {e}")
        return jsonify({"error" : "Internal Server Error"}), 500

    
#Update korisnika po ID-u
@userAPI.route('/update/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user_Ref.document(user_id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

#Obrisati korisnika po ID-u
@userAPI.route('/delete/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user_Ref.document(user_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


