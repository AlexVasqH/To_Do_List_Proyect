from typing import Union
from models import task_model
from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from mysql.connector import errorcode
import json

##Conexión con la base de datos
def call_db():
    try:
        db_connection = mysql.connector.connect(host='127.0.0.1', user='root', password='alex1234', database='proyect_01')
        print("Database connection made!")
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database doesn't exist")
        elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("User name or password is wrong")
        else:
            print(error)
    
    return db_connection

app = FastAPI()

class Item(BaseModel):
    name : str
    price : float
    if_offer: Union[bool, None] = None

@app.get("/")
def read_root():
    call_db()
    task1 = task_model(title="Hola", body="Mundo")
    print(task1)
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_ga_id": item_id, "q": q}

@app.get("/prueba1")
def prueba():
    return {"prueba": "Alex"}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.post("/create_item")
def create_item(task_model: task_model):
    print(task_model.title,task_model.body)
    dbconection = call_db()
    curA = dbconection.cursor(buffered=True)
    insert_item = "INSERT INTO notes (title, note) VALUES (%s, %s)"
    curA.execute(insert_item, (task_model.title, task_model.body))
    dbconection.commit()
    dbconection.close()
    return {"mensaje":"Registrado correctamente"}

@app.get("/read")
def read_item():
    dbconection = call_db()
    curA = dbconection.cursor(buffered=True)
    read_item = "SELECT * FROM notes"
    curA.execute(read_item)
    lista = []
    for (id, title, body,date_registred) in curA:
        print(f"La lista es {id} {title} {body} {date_registred}")
        lista.append(f"La lista es {id} {title} {body} {date_registred}")
    print(type(curA))
    dbconection.commit()
    dbconection.close()
    return json.dumps(lista)

##Dentro del execute, se agrega la var con el query en modo texto y, si es que se va a agregar un dato, este recibe 
##Datos tipo lista, tupla o dic
@app.delete("/delete/{item_id}")
def delete_item(item_id: int):
    dbconection = call_db()
    curA = dbconection.cursor(buffered=True)
    lista1 = [item_id]
    delete_item = "DELETE FROM notes WHERE id = %s"
    curA.execute(delete_item, lista1)
    dbconection.commit()
    dbconection.close()
    return {"mensaje":"Eliminado correctamente"}

##Dentro del segundo parametro del curA.execute va una lista, si está con parentesis es considerado así
##Dentro del paréntesis puede haber int, str
##Los valores dentro de la lista debe estar en orden en el cual van a ser remplazados en los %s
@app.put("/update/{item_id}")
def update_item(item_id: int, task_model: task_model):
    dbconection = call_db()
    curA = dbconection.cursor(buffered=True)
    update_item = "UPDATE notes SET title = %s, note = %s WHERE id = %s"
    curA.execute(
        update_item,
        (task_model.title, task_model.body, item_id)
        )
    dbconection.commit()
    dbconection.close()
    return {"mensaje":"Modificado correctamente"}
