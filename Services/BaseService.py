from bson.objectid import ObjectId
from typing import TypeVar, Generic
from pymongo.collection import Collection
from abc import ABC, abstractproperty
from database import db

T = TypeVar('T')

class StdObject:
    pass

class BaseService(ABC, Generic[T]):
    _fields = []
    _db_name = ''

    collection: Collection[T]
    db
     
    @abstractproperty
    def model_class(self):
        return None
    
    def __init__(self):
        self.db = db()
        self._db_name = self.__get_db_name()
        self._fields = self.__parse_fields()
        self.collection = self.db[self._db_name]
    
    def __parse_fields(self):
        mapped_fields = []
        for attribute in self.model_class.model_fields.keys():
            if attribute[:2] != 'id':
                mapped_fields.append(attribute)
        return mapped_fields

    def __get_db_name(self):
        return f'{self.model_class.__name__.lower()}s'
    
    def __attribute_fields(self, to_obj, from_obj):
        to_obj.id = str(from_obj['_id'])

        for field in self._fields:
            if field == 'id':
                continue
            setattr(to_obj, field, from_obj[field])    
            
        return to_obj

    def all(self) -> list[T]:
        items = []

        for item in self.collection.find():
            _o = StdObject()

            items.append(
                self.__attribute_fields(_o, item)
            )
                
        return items
    
    def get(self, id: str) -> T:
        _o = StdObject()

        item = self.collection.find_one({ '_id': id })

        self.__attribute_fields(_o, item)
        
        return _o

    def insert(self, item: T):
        item.id = None;
        result = self.collection.insert_one(item)
        
        return self.collection.find_one({ '_id': str(result.inserted_id) })

    def update(self, updated_item: T):
        item = self.collection.find_one({ '_id': updated_item.id })
        self.__attribute_fields(item, updated_item)
        self.collection.update_one(item)

        return self.collection.find_one({ '_id': updated_item.id })

    def delete(self, id: str):
        return self.collection.delete_one({ '_id': ObjectId(id) })

