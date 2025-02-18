import pymongo as pm

connect = pm.MongoClient("mongodb://localhost:27017/")


class createmongodb:
    def __init__(self, namedb, name1rstcoll):
        self.namedb = namedb
        self.name1rstcoll = name1rstcoll

    def creatnewdb(self):  # function to create new database
        self.mydatabase = connect[self.namedb]
        self.mycollection = self.mydatabase[self.name1rstcoll]
        return self.mycollection

    def createkeyfileds(self):
        list_k=[]
        numk=int(input("How many key : "))
        for i in range(numk):
            val_k=input("feild : ")
            list_k.append(val_k)
        return list_k
    def createvalfileds(self,listk):
        list_v=[]
        for i in listk:
            val_v=input(" ++ ")
            list_v.append(val_v)

        doc0 = dict(zip(listk,list_v))
        return doc0

    def insertf_feild(self):

        listk=self.createkeyfileds()
        doc0=self.createvalfileds(listk)
        mycollection=self.creatnewdb()
        mycollection.insert_one(doc0)


database1=createmongodb("Kali","aws")
database1.insertf_feild()
