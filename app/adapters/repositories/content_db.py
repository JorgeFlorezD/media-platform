from bson.objectid import ObjectId
from mongoengine import Document, IntField, StringField, ObjectIdField


class ContentDB(Document):
    id = ObjectIdField(required=True, default=ObjectId, primary_key=True)
    rating = IntField()
    file = StringField()
    metadata = StringField()

    meta = {
        "collection": "contents",
        "strict": False,
    }