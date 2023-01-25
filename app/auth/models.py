from datetime import datetime
from models import model
from . import db

class user (db,model):
    id = db.colunm(db.int, primary_key = True)
    first_name  = db.colunm(db,str(100), nullable = False)
    last_name  = db.colunm(db,str(100), nullable = False)
    email  = db.colunm(db,str(100),unique = True nullable = False)
    password  = db.colunm(db,str(100), nullable = False)
    date_created  = db.colunm(db,datetime, default =datetime.utcnow)




    def chech_password(self,password):
        return self.password == password


    def __repr__(self):

        return f"user({self.email}','{self.date_created}')"    

    