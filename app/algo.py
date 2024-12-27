from app.db import DB, User


def get_feed_recommendation(db: DB):
    validUsers = db.get_valid_user_recommendations()
    if len(validUsers) <= 0:
        return

    maxUser: User = validUsers[0]
    maxScore = 0
    currentUser = db.get_current_user()
    for user in validUsers:
        score = calculate_recommendation_score(currentUser, user, db)
        if score > maxScore:
            maxUser = user
            maxScore = score

    return maxUser


def calculate_recommendation_score(currentUser: User, user: User, db: DB):
    score = 0

    return score
