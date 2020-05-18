import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['test_mongo']
mycol = mydb['tests']

mydict = {"name:":"test","age":18}

x = mycol.insert_one(mydict)
print('x',x)