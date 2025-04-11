from flask import Flask, render_template, request, jsonify
from tensorai import respond
from database import *

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')
@app.route('/admin')
def admin():
    exam_data = RetrieveModules()
    event_data = RetrieveEvents()
    return render_template('admin.html', exam_data=exam_data, event_data=event_data)
@app.route('/add_event', methods=['POST'])
def add_event():
    data = request.get_json()
    event_name = data.get('event_name')
    event_info = data.get('event_info')

    if event_name and event_info:
        AddEvent(event_name, event_info)
        return jsonify({'message': 'Event added successfully!'})
    return jsonify({'error': 'Invalid data!'}), 400

#modify event
@app.route('/modify_event', methods=['POST'])
def modify_event():
    data = request.get_json()
    event_name = data.get('event_name')
    event_info = data.get('event_info')

    if event_name and event_info:
        RemoveEvent(event_name)
        AddEvent(event_name, event_info)
        return jsonify({'message': 'Event modified successfully!'})
    return jsonify({'error': 'Invalid data!'}), 400
#remove event
@app.route('/remove_event', methods=['POST'])
def remove_event():
    data = request.get_json()
    event_name = data.get('event_name')

    if event_name:
        RemoveEvent(event_name)
        return jsonify({'message': 'Event removed successfully!'})
    return jsonify({'error': 'Invalid data!'}), 400








@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_message = data.get('message')

    if user_message:
        print(f"User message: {user_message}")
        response = respond(user_message.lower())
        return jsonify({'response': response})
    return jsonify({'error': 'No message provided'})

if __name__ == '__main__':
    app.run(debug=True)
