import pymongo
import json
from bson import ObjectId, datetime
import datetime
from datetime import date
from collections import OrderedDict

class JSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, ObjectId) or isinstance(o, (datetime.date, datetime.datetime)):
            return str(o)
        return json.JSONEncoder.default(self, o)

def get_pagewise_invoices(user_id, page_index, role,db_name, collection_name):
    try:
        import datetime
        # mongo_db_credentials = mongo_auth.set_mongodb_credentials()
        mongo_client = pymongo.MongoClient("Host:Port",
                             username='user',
                            password='pass',
                           authMechanism='SCRAM-SHA-256', document_class=OrderedDict)
        # if db_name not in mongo_client.list_database_names():
        #     return
        mongo_db_client = mongo_client[db_name]
        mongo_collections = mongo_db_client[collection_name]
        
        
        skip_count = (page_index-1)*8
        if role.lower()=="admin" or role.lower()=="approver":
            print("count1:",datetime)
            count = mongo_collections.find().count()
            result_list = list(mongo_collections.find().sort("_id",-1).skip(skip_count).limit(8))
        if role.lower()=="data_annotator":
            print("ROLE", role)
            print("count1:", datetime)
            count = mongo_collections.find({"is_modified": 1}).count()
            result_list = list(mongo_collections.find({"is_modified": 1}).sort("_id",-1).limit(10))
        else:
            count = mongo_collections.find({"user_id":ObjectId(user_id)}, {'_id':1}).count()
            result_list = list(mongo_collections.find({"user_id":ObjectId(user_id)}).sort("_id", -1).skip(skip_count).limit(8))
        
        json_result = JSONEncoder().encode(result_list)
        all_result_json = OrderedDict({"all_result": json.JSONDecoder(object_pairs_hook=OrderedDict).decode(json_result),"count":count})
        return all_result_json
    except Exception as error:
        print("get_pagewise_invoices error",error)
        # LOGGER.exception(error) 