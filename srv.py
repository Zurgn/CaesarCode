import flask
import csv
import cypher
import datetime
import os

app = flask.Flask(__name__)

def get_next_index(filename):
    if not os.path.exists(filename):
        return 1
    with open(filename, 'r', encoding='utf-8') as f:
        return sum(1 for line in f) + 1

@app.route('/<user_id>', methods=['GET', 'POST'])
def handle_request(user_id):
    ID = '70223717'
    if user_id != ID:
        return flask.abort(404)
    if flask.request.method == 'POST':
        original_text = flask.request.form.get('text')
        encrypted_text = cypher.encrypt(original_text)
        index = get_next_index('messages.csv')
        with open('messages.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([index, encrypted_text, datetime.datetime.now(), flask.request.remote_addr])
        return flask.render_template("save.html", msg=encrypted_text)
    return flask.render_template("message.html")

@app.route('/reset')
def reset():
    if os.path.exists('messages.csv'):
        os.remove('messages.csv')
    return flask.render_template("reset.html")

@app.route('/get_all.json')
def get_all():
    messages_list = []
    if os.path.exists('messages.csv'):
        with open('messages.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                msg_obj = {
                    "id": row[0],
                    "datetime": row[2],
                    "ip": row[3],
                    "text": row[1]
                }
                messages_list.append(msg_obj)
    return flask.jsonify(messages=messages_list)

if __name__ == "__main__":
    app.run(debug=True)