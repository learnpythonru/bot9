from db import user_voted, get_image_rating, get_or_create_user


def test_user_voted_true(mongodb):
    assert user_voted(mongodb, "images/cat_new.jpg", 840852) is True


def test_user_voted_false(mongodb):
    assert user_voted(mongodb, "images/cat_new.jpg", 1) is False


def test_get_image_rating(mongodb):
    assert get_image_rating(mongodb, "images/cat_new.jpg") == 3
    assert get_image_rating(mongodb, "images/no_image.jpg") == 0


def test_get_or_create_user(mongodb, effective_user):
    user_exist = mongodb.users.find_one({'user_id': effective_user.id})
    assert user_exist is None
    user = get_or_create_user(mongodb, effective_user, 123)
    user_exist = mongodb.users.find_one({'user_id': effective_user.id})
    assert user == user_exist
