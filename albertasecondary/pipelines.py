# -*- coding: utf-8 -*-
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

class AlbertasecondaryPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings["MONGODB_SERVER"],
            settings["MONGODB_PORT"]
        )
        db = connection[settings["MONGODB_DB"]]
        self.collection = db[settings["MONGODB_COLLECTION"]]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            try:
                self.collection.insert(dict(item))
                log.msg("Data added to MangoDB!", level=log.DEBUG, spider=spider)
            except:
                log.msg("Failed of adding data!")
        return item