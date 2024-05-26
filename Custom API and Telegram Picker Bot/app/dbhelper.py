import pymongo


class DBHelper:
    def __init__(self, mongoServer, dbName):
        self.client = pymongo.MongoClient(mongoServer) #"mongodb+srv://doadmin:REDACTED.mongo.ondigitalocean.com/admin?authSource=admin"
        self.db = self.client.get_database(dbName) #shirts22



    def picker_add(self, pickerID, name):
        self.coll = self.db.get_collection('pickers')
        self.coll.insert_one({"_id": pickerID, "name": name, "status": "inactive", "currently_picking": "","ordersPicked": 0})

        return True

    def picker_isNew(self, pickerID):
        self.coll = self.db.get_collection('pickers')
        if self.coll.count_documents({'_id': pickerID}, limit=1) != 0:
            return self.coll.find({"_id": pickerID})
        else:
            return False

    def picker_check(self, picker_id, key_to_check):
        self.coll = self.db.get_collection('pickers')
        try:
            value_found = self.coll.find_one({"_id": picker_id}).get(key_to_check)
            return value_found
        except AttributeError:
            return False

    def picker_update_status(self, picker_id, to_update, update_value):
        self.coll = self.db.get_collection('pickers')
        self.coll.update_one({"_id": picker_id}, {'$set': {to_update: update_value}})

        return True

    def picker_queue_next(self):
        self.coll = self.db.get_collection("pickers")
        try:
            picker = self.coll.find_one({"status": "active"})
            return picker
        except AttributeError:
            return False

    def order_add(self, to_add):
        self.coll = self.db.get_collection("orders")
        self.coll.insert_one(to_add)

    def order_update_status(self, order_id, to_update, update_value):
        self.coll = self.db.get_collection('orders')
        self.coll.update_one({"_id": order_id}, {'$set': {to_update: update_value}})

        return True

    def order_queue_next(self):
        self.coll = self.db.get_collection("orders")
        try:
            order = self.coll.find_one({"collected": "false"})
            return order
        except AttributeError:
            return False
# coll.insert_one({"_id": "22051305061103689",
#                  "items":
#                      ({
#                          "greenRag": [
#                              {
#                                  "size": "XS",
#                                  "qty": "1"
#                              },
#                              {
#                                  "size": "S",
#                                  "qty": "3"
#                              }
#                          ]
#                       }),
#                  "collection_status": "scanned",
#                  "order_status": "confirmed"
#                  })
