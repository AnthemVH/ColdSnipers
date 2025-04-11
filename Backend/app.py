from flask import Flask, render_template, request, redirect, session, url_for, jsonify
import os
from tensorai import Answer_prompt
from database import *

app = Flask(__name__)
app.secret_key = "your_secret_key"

def load_users():
    users = {}
    with open("users.txt", "r") as f:
        for line in f:
            username, password, is_admin = line.strip().split(",")
            users[username] = {"password": password, "admin": is_admin.lower() == "true"}
    return users

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        users = load_users()
        username = request.form["username"]
        password = request.form["password"]
        user = users.get(username)
        if user and user["password"] == password:
            session["user"] = username
            session["admin"] = user["admin"]
            return redirect(url_for("main"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/main")
def main():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("main.html", admin=session["admin"], user=session["user"])

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_message = data.get('message')

    if user_message:
        print(f"User message: {user_message}")
        response = Answer_prompt(user_message.lower())
        return jsonify({'response': response})
    return jsonify({'error': 'No message provided'})
@app.route('/admin')
def admin_panel():
    return render_template('index.html', user_name=session.get('user_name', 'Admin'))
from datetime import datetime

@app.route('/get_events')
def get_events():
    all_events = RetrieveEvents() 
    parsed_events = []

    for name, date_str in all_events:
        try:
            
            event_date = datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
            parsed_events.append({
                "name": name,
                "date": event_date.strftime("%Y-%m-%d")
            })
        except ValueError:
            print(f"Invalid date for event: {name}")
            continue

    return jsonify(parsed_events)

@app.route('/add_event', methods=['POST'])
def add_event():
    data = request.get_json()
    event_name = data.get("event_name")
    event_date = data.get("event_date")  

    try:
        datetime.strptime(event_date, "%Y-%m-%d")  
    except (ValueError, TypeError):
        return jsonify({"status": "error", "message": "Invalid date format"}), 400

    AddEvent(event_name, event_date)
    return jsonify({"status": "success"})


@app.route('/modify_event', methods=['POST'])
def modify_event():
    data = request.get_json()
    event_name = data.get("event_name")
    new_date = data.get("event_date")

    try:
        datetime.strptime(new_date, "%Y-%m-%d")
    except (ValueError, TypeError):
        return jsonify({"status": "error", "message": "Invalid date format"}), 400

    UpdateEvent(event_name, new_date)
    return jsonify({"status": "success"})


@app.route("/remove_event", methods=["POST"])
def remove_event():
    data = request.get_json()
    event_name = data.get("event_name")
    RemoveEvent(event_name)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)
