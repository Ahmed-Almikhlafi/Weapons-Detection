import pymongo as mon


con1 = mon.MongoClient("mongodb://localhost:27017/")

# print(con1)
# print(con1.list_database_names())

#   create mongoda database

# mydatabase = con1["campany"]
#mycollection = mydatabase["admains"]
#
# doc1 = {"name":"Sam AL mekhlafi","major":"AI.eng"}
#
# mycollection.insert_one(doc1)
# create another collection
# mycollection2 = mydatabase["emplyoee"]
# doc1 = {"name":"Sam AL mekhlafi","major":"AI.eng"}
#
# mycollection2.insert_one(doc1)

# read data from

mydatabase = con1["campany"]
mycollection = mydatabase["admains"]

# print(mycollection.find_one({"name":"Sofia"}))

# docr = mycollection.find()
#
# for c in docr:
#     if c["name"]=="Delshat AL mekhlafi":
#         print(c)

# update

oldf={"name":"Delshat AL mekhlafi"}
newf={"$set":{"name":"Sereen AL mekhlafi"}}

#mycollection.update_one(oldf,newf)

listk=[]
listk=mycollection.find_one().keys()
listv=[]


for i in listk:
    val=input(i)
    listv.append(val)



print(listv)

doc0=dict(zip(listk,listv))

print(doc0)

# print(mycollection.find_one().keys())



#print(con1.list_database_names())