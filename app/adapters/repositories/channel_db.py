from bson.objectid import ObjectId
from mongoengine import Document, StringField, ObjectIdField, ListField


class ChannelDB(Document):
    id = ObjectIdField(required=True, default=ObjectId, primary_key=True)
    title = StringField(required=True)
    language = StringField(required=True)
    picture = StringField(required=True)
    parents = ListField(ObjectIdField())
    contents = ListField(ObjectIdField())

    meta = {
        "collection": "channels",
        "strict": False,
    }