import json
from pymongo import MongoClient

# Read the iris dataset in memory. We will be using data from this dataset to interact 
# with mongodb for performing some basic CRUD operations 
with open("./iris.json", 'r') as f:
    data = json.load(f)
    f.close()

# Establish a connection in mongodb by creating a MongoClient object
client = MongoClient("mongodb://localhost:27017/")

# To create a database, use the client object and index a name of database.
# If the database exists, it will refer to the existing db else, create a new database
db = client["flower"]

# Create a collection called iris to store our iris dataset
iris = db["iris"]

# Inserting a document in the collection
result = iris.insert_one(data[0])

# Every inserted entry has an _id field which can be explicitly specified & if not specified
# MongoDB creates one implicitly. Let's look at the id for the document that we inserted.
print(f"The id for first inserted document is: {result.inserted_id}")

# We don't want such random ids, we want them to be meaningful. Hence let's name the ids serially
new_data = []
for idx, item in enumerate(data[1:]):
    item["_id"] = 1 + idx
    new_data.append(item)

# We can confirm that the collection is created by looking at all the collections in our database
print(db.list_collection_names())

# We can see that we have around 150 items in our iris dataset. We can insert them all into
# our collection using the insert_many method of the collections object.
all_items = iris.insert_many(new_data[1:])
print(f"The ids for all inserted documents are:\n{all_items.inserted_ids}")

# Finding all items in a collection
# The find method in the collections object can be used for finding all the documents
# The empty parantheses indicate to return all matches. You can add a filter here if you want
# items that meet some condition 
for item in iris.find({}):
    print(item)

# Only returning select fields from documents in a collection
# In the find method, we can specify the fields that we want as a dictionary
# By default the _id field is always 1, if we're not interested in it, manually we have to turn it off
for item in iris.find({}, {"species":1, "_id":0, "sepalLength": 1}):
    print(item)

# Sorting a document
# We can sort using the method sort. The arguments to this method are the field on which to sort 
# and whether ascending or descending order is exepected (1 for ascending, -1 for descending)
for item in iris.find({}, {"species":1, "_id":0, "sepalLength":1}).sort("sepalLength", -1):
    print(item)

# Updating a document
# We can update fields of a document using a query and a replacement dictionary as follows
query = {"_id": 20}
replace = {"$set": {"species": "NA"}}
iris.update_one(query, replace)

# Limiting the result
# In order to view only a certain part of the dataframe, we can use the limit command with other
# Commands. For eg. let's say we want to see the record with highest sepalLength, we can sort on
# sepal length in descending order and limit the number of results to a single one.
for item in iris.find({}).sort("sepalLength", -1).limit(1):
    print(item)

# Deleting documents
# We can delete items from the data by using delete_one or delete_many methods
# The former can be used to delete one item based on a condition and the latter can be used to delete
# Multiple objects on a condition. If no condition is given, it will empty the entire collection.
iris.delete_one({"_id": 20})

count_before_deletion = len([x for x in iris.find()])
iris.delete_many({"sepalLength": 4.4})
count_after_deletion = len([x for x in iris.find()])

print(f"Before Deletion: {count_before_deletion}\nAfter Deletion: {count_after_deletion}.")
iris.delete_many({})

# Deleting a collection
# We can delete an entire collection using the drop method. 
iris.drop()
print(f"Collection names: {db.list_collection_names()}.")