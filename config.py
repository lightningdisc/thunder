from main import mongo_client

# REDEFINE
mongo_db = mongo_client.thunder # Mongo DB to use
db_collection = mongo_db["test"] #main collection
tags_collection = mongo_db["tags"] # tags collection