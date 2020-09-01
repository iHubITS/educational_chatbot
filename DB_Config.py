from pymongo import MongoClient

client = MongoClient("mongodb://IHub:ihub123@cluster0-shard-00-00.2smz4.mongodb.net:27017,cluster0-shard-00-01.2smz4.mongodb.net:27017,cluster0-shard-00-02.2smz4.mongodb.net:27017/IHUB_DB?ssl=true&replicaSet=atlas-rubazd-shard-0&authSource=admin&retryWrites=true&w=majority")
mongo = client.get_database("IHUB_DB")