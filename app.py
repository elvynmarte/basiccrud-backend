import mysql.connector
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from pydantic import BaseModel
from dotenv import load_dotenv
import re

app = Flask(__name__)

load_dotenv('.env')

dbname = os.getenv("DB_NAME")
dbhost = os.getenv("DB_HOST")
dbuser = os.getenv("DB_USER")
dbpass = os.getenv("DB_PASS")

# CORS: permite al frontend llamar al backend.
# Puedes afinarlo luego con una lista de orígenes.
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "*")
CORS(app, resources={r"/*": {"origins": FRONTEND_ORIGIN}})

#DB connection from .env file credentials
def Connect():
    try:
        conn = mysql.connector.connect(host=dbhost,database=dbname,user=dbuser,password=dbpass)
        print("connection success")
        return conn
    except:
        print("Connection error")

#validate email class
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# generic class
class Users(BaseModel):
    id:int = 0
    name:str = ""
    email:str = ""
    passw:str = ""
    cpassw:str=""
    npassw:str=""
    active:int = 0

class Items(BaseModel):
    id:int = 0
    type:int=0
    name:str=""
    quantity:int=0
    price:float=0
    active:bool=True

class Type(BaseModel):
    id:int = 0
    description:str=""
    active:int = 1

#authentication login method
@app.route("/get-login",methods=['POST'])
def getLogin():

    user = Users(**request.json)

    if not user.email or not user.passw:
        return {"error":"Fields: Email and Password must be necessary!"}

    if not validate_email(user.email):
        return {"error":"Invalid email format"}

    conn = Connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name, email, id FROM  crud_user where email = %s and pass = sha2(%s,256)",(user.email, user.passw,))
    usr = cursor.fetchall()

    res = {"error":"User not found!"}
    if len(usr) > 0:
        res = usr[0]

    conn.close()
    cursor.close()

    return res

#user methods
@app.get("/get-users")
def getUsers():
    conn = Connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM  crud_user where id > 1")
    usr = cursor.fetchall()
    conn.close()
    cursor.close()

    return usr

#insert / update
@app.route("/iu-user",methods=['POST'])
def iuUsers():
    usr = Users(**request.json)   

    if not usr.name and not usr.email and not usr.passw and usr.id <= 0:
        return {"error":"Fields: Name, Email and Password must be necessary!"}
    elif not usr.name and not usr.email:
        return {"error":"Fields: Name and Email must be necessary!"}

    if not validate_email(usr.email):
        return {"error":"Invalid email format!"}
    
    conn = Connect()    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM crud_user WHERE email = %s and (id != %s or %s=0)",(usr.email,usr.id,usr.id,))
    u = cursor.fetchall()
    if len(u) > 0:
        conn.close()
        cursor.close()
        return {"error":"A user with the same email exists currently, try to create an account with another email!"}
    else:               
        if usr.id <= 0:
            cursor.execute("INSERT INTO crud_user(name, email, pass)VALUES(%s,%s, sha2(%s,256))",(usr.name,usr.email,usr.passw,))
        else:
            cursor.execute("UPDATE crud_user SET name = %s, email=%s, active=%s WHERE id = %s",(usr.name,usr.email, usr.active, usr.id,))
        
        conn.commit()
        conn.close()
        cursor.close()
        return {"msg":"User has been saved successfully!"}

#reset pass
@app.route('/reset-pass',methods=['POST'])
def resetPass():
    usr = Users(**request.json)
    conn = Connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM crud_user WHERE pass= sha2(%s, 256) and id = %s",(usr.passw,usr.id,))
    res = cursor.fetchall()
    
    typemsg = "msg"
    msg = "Password has been changed successfully!"

    if len(res) > 0:
        if usr.npassw != usr.cpassw:
            msg = "Both password do not match!"
            typemsg = "error"
        else:
            cursor.execute("UPDATE crud_user SET pass = sha2(%s,256) WHERE id = %s",(usr.npassw,usr.id,))
            conn.commit()
    else:
        msg = "Current password is invalid!"; 
        typemsg = "error"

    conn.close()
    cursor.close()
    
    return {typemsg:msg}

# delete   
@app.route("/del-user",methods=['POST'])
def delUser():
    usr = Users(**request.json)
    conn = Connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("DELETE FROM crud_user WHERE id = %s",(usr.id,))
    conn.commit()
    conn.close()
    cursor.close()
    
    return {"msg":"User has been deleted!"}

# items methods
@app.route("/get-items",methods=['GET'])
def getItems():
    conn = Connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT p.*, t.description as desctype FROM  products p join type t on p.type = t.id  order by p.name")
    usr = cursor.fetchall()
    conn.close()
    cursor.close()

    return usr

#insert / update
@app.route("/iu-item",methods=['POST'])
def iuItems():
    pro = Items(**request.json)   

    if not pro.name and pro.price <=0 and pro.quantity <= 0:
        return {"error":"Fields: Description, Price and Quantity must be necessary!"}

              
    conn = Connect()    
    cursor = conn.cursor(dictionary=True)
                 
    if pro.id <= 0:
        cursor.execute("INSERT INTO products(name, type, price, quantity)VALUES(%s,%s,%s,%s)",
                       (pro.name, pro.type,pro.price,pro.quantity))
    else:
        cursor.execute("UPDATE products SET name = %s, type=%s, price=%s, quantity=%s WHERE id = %s",
                       (pro.name, pro.type,pro.price,pro.quantity,pro.id))
    
    conn.commit()
    conn.close()
    cursor.close()
    return {"msg":"Product has been saved!"}

# delete   
@app.route("/del-item",methods=['POST'])
def delItems():
    item = Items(**request.json)
    conn = Connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("DELETE FROM products WHERE id = %s",(item.id,))
    conn.commit()
    conn.close()
    cursor.close()
    
    return {"msg":"Product has been deleted!"}

#type methods
@app.route("/get-types",methods=['GET'])
def getTypes():
    conn = Connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT t.*, case when exists(select id from products where type = t.id limit 1) then 1 else 0 end as hasproduct" \
    " FROM  type t order by t.description")
    usr = cursor.fetchall()
    conn.close()
    cursor.close()

    return usr

#insert / update
@app.route("/iu-type",methods=['POST'])
def iuType():
    typ = Type(**request.json)   

    if not typ.description and typ.id <= 0:
        return {"error":"Field Description must be necessary!"}
              
    conn = Connect()    
    cursor = conn.cursor(dictionary=True)
                 
    if typ.id <= 0:
        cursor.execute("INSERT INTO type(description)VALUES(%s)", (typ.description,))
    else:
        cursor.execute("UPDATE type SET description = %s, active = %s WHERE id = %s", (typ.description,typ.active, typ.id,))
    
    conn.commit()
    conn.close()
    cursor.close()
    return {"msg":"Type has been saved!"}

# delete   
@app.route("/del-type",methods=['POST'])
def delType():
    typ = Type(**request.json)
    conn = Connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("DELETE FROM type WHERE id = %s and not exists(select id from products where type = %s)",(typ.id,typ.id))
    conn.commit()
    conn.close()
    cursor.close()
    
    return {"msg":"Type has been deleted!"}


