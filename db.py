from datetime import datetime
from random import choice
from emoji import emojize
from pymongo import MongoClient
import settings

client = MongoClient(settings.MONGO_LINK)

db = client[settings.MONGO_DB]


def get_or_create_user(db, effective_user, chat_id):
    user = db.users.find_one({"user_id": effective_user.id})
    if not user:
        user = {
            "user_id": effective_user.id,
            "first_name": effective_user.first_name,
            "last_name": effective_user.last_name,
            "username": effective_user.username,
            "chat_id": chat_id,
            "emoji": emojize(choice(settings.USER_EMOJI), use_aliases=True)
        }
        db.users.insert_one(user)
    return user


def save_anketa(db, user_id, anketa_data):
    user = db.users.find_one({"user_id": user_id})
    anketa_data['created'] = datetime.now()
    if 'anketa' not in user:
        db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'anketa': [anketa_data]}}
        )
    else:
        db.users.update_one(
            {'_id': user['_id']},
            {'$push': {'anketa': anketa_data}}
        )


def subscribe_user(db, user_data):
    if not user_data.get('subscribed'):
        db.users.update_one(
            {'_id': user_data['_id']},
            {'$set': {'subscribed': True}}
        )


def unsubscribe_user(db, user_data):
    db.users.update_one(
        {'_id': user_data['_id']},
        {'$set': {'subscribed': False}}
    )


def get_subscribed(db):
    return db.users.find({"subscribed": True})


def save_cat_image_vote(db, user_data, image_name, vote):
    image = db.images.find_one({"image_name": image_name})
    if not image:
        image = {
            "image_name": image_name,
            "votes": [{"user_id": user_data["user_id"], "vote": vote}]
        }
        db.images.insert_one(image)
    elif not user_voted(db, image_name, user_data["user_id"]):
        db.images.update_one(
            {"image_name": image_name},
            {"$push": {"votes": {"user_id": user_data["user_id"], "vote": vote}}}
        )


def user_voted(db, image_name, user_id):
    if db.images.find_one({"image_name": image_name, "votes.user_id": user_id}):
        return True
    return False


def get_image_rating(db, image_name):
    rating = db.images.aggregate([
        {
            '$match': {
                'image_name': image_name
            }
        }, {
            '$unwind': {
                'path': '$votes'
            }
        }, {
            '$group': {
                '_id': '$image_name', 
                'rating': {
                    '$sum': '$votes.vote'
                }
            }
        }
    ])
    rating = next(rating, None)
    if rating:
        return rating['rating']
    return 0
