import flask
import csv
import cypher
import datetime
import os

app = flask.Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Сообщение</title></head>
<body>
    <form method="POST">
        <label>Введите сообщение:</label><br>
        <textarea style="width:95%" name="text"></textarea><br>
        <input type="submit" value="Отправить">
    </form>
</body>
</html>
"""

HTML_SAVE = """
        <HTML><BODY>
        <p>Сообщение сохранено:</p>
        <p>{{msg}}</p>
        </BODY></HTML>
        """

HTML_RESET = """
<!DOCTYPE html>
<HTML>
<BODY>
<p>messages.csv стёрт</p>
</BODY>
</HTML>
"""

def get_next_index(filename):
    if not os.path.exists(filename):
        return 1
    with open(filename, 'r', encoding='utf-8') as f:
        return sum(1 for line in f) + 1

@app.route('/<user_id>', methods=['GET', 'POST'])
def handle_request(user_id):
    if flask.request.method == 'POST':
        original_text = flask.request.form.get('text')
        encrypted_text = cypher.encrypt(original_text)
        index = get_next_index('messages.csv')
        with open('messages.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([index, encrypted_text, datetime.datetime.now(), flask.request.remote_addr])
        return flask.render_template_string(HTML_SAVE, msg=encrypted_text)
    return flask.render_template_string(HTML_TEMPLATE)

@app.route('/reset')
def reset():
    if os.path.exists('messages.csv'):
        os.remove('messages.csv')
    return flask.render_template_string(HTML_RESET)

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