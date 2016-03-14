# support functions for the CoachingBuddy
from pymongo import MongoClient


def find_rower(name):
    name = name.split(' ')
    db = MongoClient().hampton.rowers
    cursor = db.find({"name": {"first": name[0], "last": name[1]}})
    return cursor


def find_by(sex, team, weight, year):
    db = MongoClient().hampton.rowers
    if sex is not None:
        if team is not None:
            if weight is not None:
                if year is not None:
                    cursor = db.find({"gender": sex, 'team': team, 'designation': weight, 'year': year})
                else:
                    cursor = db.find({"gender": sex, 'team': team, 'designation': weight})
            else:
                if year is not None:
                    cursor = db.find({"gender": sex, 'team': team, 'year': year})
                else:
                    cursor = db.find({"gender": sex, 'team': team})
        else:
            if weight is not None:
                if year is not None:
                    cursor = db.find({"gender": sex, 'designation': weight, 'year': year})
                else:
                    cursor = db.find({"gender": sex, 'designation': weight})
            else:
                if year is not None:
                    cursor = db.find({"gender": sex, 'year': year})
                else:
                    cursor = db.find({"gender": sex})
    else:
        if team is not None:
            if weight is not None:
                if year is not None:
                    cursor = db.find({'team': team, 'designation': weight, 'year': year})
                else:
                    cursor = db.find({'team': team, 'designation': weight})
            else:
                if year is not None:
                    cursor = db.find({'team': team, 'year': year})
                else:
                    cursor = db.find({'team': team})
        else:
            if weight is not None:
                if year is not None:
                    cursor = db.find({'designation': weight, 'year': year})
                else:
                    cursor = db.find({'designation': weight})
            else:
                if year is not None:
                    cursor = db.find({'year': year})
                else:
                    cursor = db.find()

    return cursor
