from typing import Union

from fastapi import FastAPI

from pydantic import BaseModel

import mysql.connector
from mysql.connector import errorcode
def call_db():
    try:
        db_connection = mysql.connector.connect(host='127.0.0.1', user='root', password='', database='to_do_list_database')
        print("Database connection made!")
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database doesn't exist")
        elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("User name or password is wrong")
        else:
            print(error)
    else:
        db_connection.close()


app = FastAPI()

class Item(BaseModel):
    name : str
    price : float
    if_offer: Union[bool, None] = None

@app.get("/")
def read_root():
    call_db()
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

