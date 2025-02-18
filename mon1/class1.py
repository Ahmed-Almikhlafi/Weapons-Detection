import pymongo as pm

connect = pm.MongoClient("mongodb://localhost:27017/")

class createmongodb:
    def __init__(self,namedb,name1rstcoll):
        self.namedb = namedb
        self.name1rstcoll = name1rstcoll


    def creatnewdb(self): # function to create new database
        self.mydatabase = connect[self.namedb]
        self.mycollection = self.mydatabase[self.name1rstcoll]

        self.numf = input("HOW MANY FIELD YOU WANT TO INPUT : ")
        self.listk = []
        for i in self.numf:
            val = input(f"Field " + (i + 1) + " : ")
            self.listk.append(val)

        self.insetnewfield(self.namedb, self.name1rstcoll)

        # doc1 = {"name":"Sam AL mekhlafi","major":"AI.eng"}
        # self.mycollection.insert_one(doc1)

    def creatnewcoll(self,namedb,namecoll): # function to create new collection
        self.newcollname=namecoll
        self.mdbname = namedb
        self.mydatabase = connect[self.mdbname]
        self.mycollection = self.mydatabase[self.newcollname]
        self.insetnewfield(namedb, namecoll)
        # doc0 = {"id":0,"name": "mongodb"} # must create function to send doc
        # self.mycollection.insert_one(doc0)

    def insetnewfield(self,namedb,namecoll): # function to insert new field
        self.newcollname = namecoll
        self.mdbname = namedb
        self.mydatabase = connect[self.mdbname]
        self.mycollection = self.mydatabase[self.newcollname]
        # mycollection = self.mycollection
        doc1 = self.createnewfiel(self.mycollection)

        doc0 = {"id": 0, "name": "mongodb"}# must create function to send doc
        self.mycollection.insert_one(doc1)

    def createnewfiel(self,mycollection):

        listk = mycollection.find_one().keys()

        if not listk:
            self.listk = listk

        self.listv = []

        for i in self.listk:
            val = input(i)
            self.listv.append(val)

        doc0 = dict(zip(self.listk, self.listv))
        return doc0



    def updatefield(self):
        print("c")





# newdb1= createmongodb("TOP_MARK","Admains")
# newdb1.creatnewdb()
# newdb1.insetnewfield("TOP_MARK","Admains")

newdb1= createmongodb("NEW_CAMPANY","EMPLOYEE")
newdb1.creatnewdb()