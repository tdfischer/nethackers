from flask import Flask, render_template, request
import os.path

def fold_base64(s):
    return [c for c in s if c.isalnum() or c == '/' or c == '=' or c == '-' or
        c==' ' or c=='+']

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def reserve():
    tokens = request.form['key'].strip().split(' ', 2)
    algo = tokens[0]
    key = tokens[1]
    key = ''.join(fold_base64(key))
    nym = ''.join([c for c in request.form['nym'].strip() if c.isalnum()])
    authed_keys = open(os.path.expanduser('~/.ssh/authorized_keys'), 'a')
    authed_keys.write("command=\"nethack-shell
        %s\",no-port-forwarding,no-x11-forwarding %s %s\n"%(nym, algo, key))
    print("Registered %s with key %s"%(nym, key))
    return render_template('registered.html')

if __name__ == "__main__":
    app.run(debug=True)
