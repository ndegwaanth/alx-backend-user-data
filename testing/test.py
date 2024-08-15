from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
auth = HTTPBasicAuth()


user = {
    "Anthony": generate_password_hash("helo"),
    "Ndegwa": generate_password_hash("world")
}

@auth.verify_password
def verify_password(username, password):
    if username in user and check_password_hash(user.get(username), password):
        return username


@app.route('/')
@auth.login_required
def entry():
    return "<h1>Hello</h1> {}".format(auth.current_user())


if __name__ == '__main__':
    app.run()  