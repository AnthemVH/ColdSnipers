import sqlite3
from datetime import datetime

conn = sqlite3.connect("AIDatabase", check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS EmbeddingPlacements (EmbeddingCode TEXT, Information TEXT)''')
conn.commit()



def AddEvent(event_name, event_date):  
    try:
        
        datetime.strptime(event_date, "%Y-%m-%d")

        cursor.execute("SELECT Information FROM EmbeddingPlacements WHERE EmbeddingCode = 'EventList'")
        result = cursor.fetchone()

        new_event = f"name:{event_name} Date:{event_date}"

        if result is None:
            cursor.execute("INSERT INTO EmbeddingPlacements (EmbeddingCode, Information) VALUES ('EventList', ?)", (new_event,))
        elif not result[0]:
            cursor.execute("UPDATE EmbeddingPlacements SET Information = ? WHERE EmbeddingCode = 'EventList'", (new_event,))
        else:
            updated_list = result[0] + ";" + new_event
            cursor.execute("UPDATE EmbeddingPlacements SET Information = ? WHERE EmbeddingCode = 'EventList'", (updated_list,))
        
        conn.commit()
        print(f"Event '{event_name}' on {event_date} added successfully.")
    except ValueError:
        print(f"Invalid date format for event: {event_name}, {event_date}")


def RetrieveEvents():
    cursor.execute("SELECT Information FROM EmbeddingPlacements WHERE EmbeddingCode = 'EventList'")
    result = cursor.fetchone()

    if result and result[0]:
        events = []
        for raw_event in result[0].split(";"):
            if "name:" in raw_event and " Date:" in raw_event:
                try:
                    name_part, date_part = raw_event.split(" Date:")
                    name = name_part.replace("name:", "").strip()
                    date_str = date_part.strip()
                    
                    datetime.strptime(date_str, "%Y-%m-%d")
                    events.append((name, date_str))
                except Exception as e:
                    print(f"Skipping malformed event: {raw_event}")
        return events

    return []


def UpdateEvent(event_name, new_date):
    try:
        datetime.strptime(new_date, "%Y-%m-%d")  

        events = RetrieveEvents()
        updated_events = []

        for name, date in events:
            if name == event_name:
                updated_events.append(f"name:{name} Date:{new_date}")
            else:
                updated_events.append(f"name:{name} Date:{date}")

        combined_string = ";".join(updated_events)
        cursor.execute("UPDATE EmbeddingPlacements SET Information = ? WHERE EmbeddingCode = 'EventList'", (combined_string,))
        conn.commit()
        print(f"Updated '{event_name}' to new date: {new_date}")
    except ValueError:
        print("Invalid date format.")


def RemoveEvent(event_name):
    events = RetrieveEvents()
    updated_events = [f"name:{name} Date:{date}" for name, date in events if name != event_name]

    combined_string = ";".join(updated_events)
    cursor.execute("UPDATE EmbeddingPlacements SET Information = ? WHERE EmbeddingCode = 'EventList'", (combined_string,))
    conn.commit()
    print(f"Event '{event_name}' removed.")



def AddModule(module_name):
    try:
        cursor.execute("INSERT INTO EmbeddingPlacements (EmbeddingCode) VALUES (?)", (module_name,))
        conn.commit()
        print(f"Module '{module_name}' added successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while adding the module: {e}")

def UpdateModule(module_name, information):
    cursor.execute("UPDATE EmbeddingPlacements SET Information = ? WHERE EmbeddingCode = ?", (information, module_name))
    conn.commit()

def RetrieveModules():
    cursor.execute("SELECT * FROM EmbeddingPlacements WHERE NOT EmbeddingCode = 'EventList'")
    return cursor.fetchall()
