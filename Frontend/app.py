from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_message = data.get('message')

    if user_message:
        #response = get_response(user_message)
        return jsonify({'response': response})
    return jsonify({'error': 'No message provided'})

if __name__ == '__main__':
    app.run(debug=True)
