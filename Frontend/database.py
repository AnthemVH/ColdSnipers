import sqlite3

conn = sqlite3.connect("AIDatabase",check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS EmbeddingPlacements (EmbeddingCode text,Information text)''')

cursor.execute("Select * from EmbeddingPlacements")
print(cursor.fetchall())

def AddModule(module_name):
    cursor.execute(f"INSERT INTO EmbeddingPlacements (EmbeddingCode) VALUES ('{module_name}')")
    conn.commit()

def UpdateModule(module_name,information):
    cursor.execute(f"UPDATE EmbeddingPlacements SET Information = '{information}' WHERE EmbeddingCode = '{module_name}'")
    conn.commit()

def Retrieve_Module(Code):
    cursor.execute(f"Select Information from EmbeddingPlacements where EmbeddingCode = '{Code}'")
    Information = f'{Code}' + cursor.fetchone()
    return Information


def AddEvent(Event_name,Event_information):
    cursor.execute("SELECT Information from EmbeddingPlacements Where EmbeddingCode = 'EventList'")
    Eventlist = cursor.fetchone()
    Eventlist += "name : " + Event_name + " Information " + Event_information
    cursor.execute(f"UPDATE EmbeddingPlacements SET Information = '{Eventlist}' WHERE EmbeddingCode = 'EventList'")
    conn.commit()

def RemoveEvent(New_Event):
    cursor.execute(f"UPDATE EmbeddingPlacements SET Information = '{New_Event}' WHERE EmbeddingCode = 'EventList'")
    conn.commit()

def RetrieveModules():
    cursor.execute("Select * from EmbeddingPlacements Where NOT EmbeddingCode = 'EventList' ")
    Modules = cursor.fetchall()
    return Modules

def RetrieveEvents():
    cursor.execute("Select * from EmbeddingPlacements Where EmbeddingCode = 'EventList' ")
    Events = cursor.fetchone()
    return Events