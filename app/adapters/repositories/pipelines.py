  
from typing import List
from bson import ObjectId


def pipeline_subchannel_reduced(channel_id:str, max_level: int) -> List[dict]:             
    return [
        {
            "$match": {
                "_id" : ObjectId(channel_id),
            }
        },
        {
            "$graphLookup": {
                "from": "channels",
                "startWith": "$_id",
                "connectFromField": "_id",
                "connectToField": "parents",
                "as": "sub_channels",
                "maxDepth": max_level,
            },
        },
        {   
            "$project": {
                "_id": "$_id",
                "title" : "$title",
                "parents" : "$parents",
                "sub_channels": "$sub_channels",
            },
        },
        {
            "$unwind": "$sub_channels"
        },
        { 
            "$project": {
                "_id": "$sub_channels._id",
                "title": "$sub_channels.title",
                "parents": "$sub_channels.parents",
                "contents": "$sub_channels.contents",
            },
        }         
    ]   
    
def pipeline_subchannel(channel_id:str, max_level: int) -> List[dict]:             
    return [
        {
            "$match": {
                "_id" : ObjectId(channel_id),
            }
        },
        {
            "$graphLookup": {
                "from": "channels",
                "startWith": "$_id",
                "connectFromField": "_id",
                "connectToField": "parents",
                "as": "sub_channels",
                "depthField": 'level',
                "maxDepth": max_level - 1,
            },
        }
    ]