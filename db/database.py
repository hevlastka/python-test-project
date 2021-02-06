from model.model import db


def get_all(model):
    data = model.query.all()
    return data
