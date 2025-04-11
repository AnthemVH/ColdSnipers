import sqlite3

conn = sqlite3.connect("AIDatabase",check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS EmbeddingPlacements (EmbeddingCode text,Information text)''')
print(cursor.fetchall())
cursor.execute("SELECT * FROM EmbeddingPlacements")
conn.commit()



def AddModule(module_name):
    cursor.execute(f"INSERT INTO EmbeddingPlacements (EmbeddingCode) VALUES ('{module_name}')")
    conn.commit()

def UpdateModule(module_name,information):
    cursor.execute(f"UPDATE EmbeddingPlacements SET Information = '{information}' WHERE EmbeddingCode = '{module_name}'")
    conn.commit()

def AddEvent(event_name, event_information):
    print(f"Adding event: {event_name}, {event_information}")  # Debugging log

    # Retrieve the current 'Information' for 'EventList'
    cursor.execute("SELECT Information FROM EmbeddingPlacements WHERE EmbeddingCode = 'EventList'")
    result = cursor.fetchone()

    print(f"Current EventList: {result}")  # Debugging log

    if result is None:
        # If there is no row for 'EventList', insert a new row with the event data
        print("No EventList row found. Inserting new row.")  # Debugging log
        event_list = f"name:{event_name} Information:{event_information}"
        cursor.execute("INSERT INTO EmbeddingPlacements (EmbeddingCode, Information) VALUES ('EventList', ?)", (event_list,))
        print("Inserted new EventList row.")  # Debugging log
    elif not result[0]:
        # If the Information column is empty, update it with the new event
        print("EventList row found but Information column is empty.")  # Debugging log
        event_list = f"name:{event_name} Information:{event_information}"
        cursor.execute("UPDATE EmbeddingPlacements SET Information = ? WHERE EmbeddingCode = 'EventList'", (event_list,))
        print("Updated existing EventList row with new event.")  # Debugging log
    else:
        # If there is existing event data, append the new event to it
        print(f"Existing EventList data: {result[0]}")  # Debugging log
        event_list = result[0] + f";name:{event_name} Information:{event_information}"
        cursor.execute("UPDATE EmbeddingPlacements SET Information = ? WHERE EmbeddingCode = 'EventList'", (event_list,))
        print("Appended new event to existing EventList.")  # Debugging log
    
    conn.commit()
    print("Event added successfully.")  # Debugging log

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

AddEvent("test1", "test2")

