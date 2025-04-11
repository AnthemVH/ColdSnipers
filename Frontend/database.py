import sqlite3

conn = sqlite3.connect("AIDatabase",check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS EmbeddingPlacements (EmbeddingCode text,Information text)''')

def AddModule(module_name):
    cursor.execute(f"INSERT INTO EmbeddingPlacements (EmbeddingCode) VALUES ('{module_name}')")
    conn.commit()

def UpdateModule(module_name,information):
    cursor.execute(f"UPDATE EmbeddingPlacements SET Information = '{information}' WHERE EmbeddingCode = '{module_name}'")
    conn.commit()

def AddEvent(event_name, event_information):
    cursor.execute("SELECT * FROM EmbeddingPlacements WHERE EmbeddingCode = 'EventList'")
    result = cursor.fetchone()
    print(result)
    
    if result is None:  # If the row does not exist, insert it
        event_list = "name:" + event_name + " Information:" + event_information
        cursor.execute("INSERT INTO EmbeddingPlacements (EmbeddingCode, Information) VALUES ('EventList', ?)", (event_list,))
    else:  # If the row exists, update it
        if result[0]:  # If there is existing event data
            event_list = result[0] + ";name:" + event_name + " Information:" + event_information
        else:  # If no event data exists
            event_list = "name:" + event_name + " Information:" + event_information
        
        cursor.execute("UPDATE EmbeddingPlacements SET Information = ? WHERE EmbeddingCode = 'EventList'", (event_list,))
    
    conn.commit()

def RemoveEvent(New_Event):
    cursor.execute(f"UPDATE EmbeddingPlacements SET Information = '{New_Event}' WHERE EmbeddingCode = 'EventList'")
    conn.commit()

def RetrieveModules():
    cursor.execute("Select * from EmbeddingPlacements Where NOT EmbeddingCode = 'EventList' ")
    Modules = cursor.fetchall()
    return Modules

def RetrieveEvents():
    cursor.execute("SELECT Information FROM EmbeddingPlacements WHERE EmbeddingCode = 'EventList'")
    result = cursor.fetchone()
    
    if result and result[0]:  # If there is event data
        events = []
        for event in result[0].split(";"):  # Split events by semicolon
            if "name:" in event and " Information:" in event:
                name, info = event.split(" Information:")
                name = name.replace("name:", "").strip()
                info = info.strip()
                events.append((name, info))
        return events
    return []  # Return an empty list if no events exist

def AddModule(module_name):
    try:
        cursor.execute("INSERT INTO EmbeddingPlacements (EmbeddingCode) VALUES (?)", (module_name,))
        conn.commit()
        print(f"Module '{module_name}' added successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while adding the module: {e}")