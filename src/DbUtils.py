# coding=utf8
from pprint import pprint

from pymongo import MongoClient

from Utils import logInfo

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DB_NAME = 'thesis'
PUBLICATIONS = 'publication'
AUTHORS = 'authors'
QUOTES = 'quotes'
PUB_AUTHORS = 'publication_authors'

connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
dbName = connection[DB_NAME]
collectionPublications = dbName[PUBLICATIONS]
collectionAuthors = dbName[AUTHORS]
collectionPublicationsAuthors = dbName[PUB_AUTHORS]
collectionQuotes = dbName[QUOTES]

# def __init__(self):


def insert(data):
    if len(data["author"])>1:
        logInfo("MULTI AUTHOR FOUND")
    # TODO: Here can be implemented a multi authored layer
    author_id = insert_author(data["author"][0])
    data["author"] = author_id
    insert_publication(data)
    publication_id = data["_id"]
    insert_publication_author(publication_id, author_id)

def exists_in_db(query):
    if len(list(query)) > 0:
        return True
    return False

def insert_author(author):
    if exists_in_db(collectionAuthors.find({"name": author})):
        # TODO: verify if there is more than one and handle
        logInfo("Author found. Using existing one...")
        author_id = collectionAuthors.find_one({"name": author})["_id"]
    else:
        insertAuthor = {
            "name": author,
        }
        logInfo("Author not found. Creating new one...")
        author_id = collectionAuthors.insert_one(insertAuthor).inserted_id
    return author_id

def insert_publication(data):
    if not exists_in_db(collectionPublications.find({"_id": data["_id"]})):
        logInfo("Publication not found. Creating new one...")
        collectionPublications.insert_one(data)

def insert_publication_author(publicationId, authorId):
    publicationAuthorId = "" + str(publicationId) + "_" + str(authorId)

    insertPublicationAuthor = {
        "_id": publicationAuthorId,
        "id_publication": publicationId,
        "id_author": authorId,
        "type_author": "relator",  # relator, adjunto, autor
        "order_author": 1
    }

    if not exists_in_db(collectionPublicationsAuthors.find({"_id": publicationAuthorId})):
        logInfo("Publication <> Author relation not found. Creating new one...")
        collectionPublicationsAuthors.insert_one(insertPublicationAuthor)

def insert_quote(quote, publicationId):
    insertQuote = {
        "id_publication_caller": publicationId,
        "id_publication_receiver": "",
        "full_quote": quote,
        "pages": "",
        "chapters": ""
    }

    quoteId = ""
    if not exists_in_db(collectionQuotes.find({"full_quote": quote})):
        logInfo("Quote not found. Creating new one...")
        quoteId = collectionQuotes.insert_one(insertQuote).inserted_id
    return quoteId

def purge_db():
    val = input("Are you sure? (yes/no):\n > ")
    if val != "yes":
        return

    x = collectionPublications.delete_many({})
    print(x.deleted_count, " publications deleted.")
    x = collectionAuthors.delete_many({})
    print(x.deleted_count, " authors deleted.")
    x = collectionPublicationsAuthors.delete_many({})
    print(x.deleted_count, " publications-authors deleted.")
    x = collectionQuotes.delete_many({})
    print(x.deleted_count, " quotes deleted.")


def get_all_from_db():
    pipeline = [{
        '$lookup': {
            'from': PUBLICATIONS,
            'localField': 'id_publication',
            'foreignField': '_id',
            'as': 'publicationFields'
        }

    }, {
        "$replaceRoot": { "newRoot": {
            "$mergeObjects": [ {
                "$arrayElemAt": [ "$publicationFields", 0 ]
            }, "$$ROOT" ]
            }
        }
    }, {
    #     '$unwind': {
    #         'path': "$publication",
    #         'preserveNullAndEmptyArrays': True
    #     }
    # }, {
    #     '$group': {
    #         "_id": "$_id",
    #         "id_publication": {"$first": "$_id"}
    #     }
    # }, {
        '$lookup': {
            'from': AUTHORS,
            'localField': 'id_author',
            'foreignField': '_id',
            "pipeline": [
            {'$project': {
                "author_name": "$name"
                }}
            ],
            'as': 'authorFields'
        }
    }, {
        "$replaceRoot": { "newRoot": {
            "$mergeObjects": [ {
                "$arrayElemAt": [ "$authorFields", 0 ]
            }, "$$ROOT" ],
                # "author": "$authorFields.name"
            }
        }
    }, {
        '$project': {
            # '_id': False,
            "authorFields": 0,
            "publicationFields": 0
        }
    }]

    for doc in (collectionPublicationsAuthors.aggregate(pipeline)):
        pprint(doc)

# TODO: NoSQL would benifit from indexing ids
