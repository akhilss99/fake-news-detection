import pymongo
from pymongo.server_api import ServerApi
#connectionString = 'Driver={ODBC Driver 13 for SQL Server};Server='+server_name+';PORT=1433;Database='+database+';Uid='+username+';Pwd='+ password


client = pymongo.MongoClient("mongodb+srv://akhil:akhil4newsdetection@newsdetection.epptsyk.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)
db = client.test
print(db.list_collections())