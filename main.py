from flask import *
import flask
import time
import users_class

app = Flask(__name__)

admin_user = "admin"
admin_pwd = "admin"

dict_user_pwds = {

}

@app.route('/')
def index():
    return render_template("intro_login.html")

@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    if request.method == "POST":
        input_user = request.form.get("username")
        input_pwd = request.form.get("password")
        if (input_user == admin_user) and (input_pwd == admin_pwd):
            return redirect('main')
        else:
            return abort(401)
            
    return render_template("authenticate.html")

@app.route('/main', methods = ['GET', 'POST'])
def main():
    return render_template("main_page.html")

@app.route('/manual', methods=['GET', 'POST'])
def manual():
    return None

app.run()