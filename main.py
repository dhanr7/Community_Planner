from flask import *
import flask
import time
import users_class as users_class

app = Flask(__name__)

admin = users_class.User("admin", "admin", "administrator")

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
        if (admin.authenticateCredentials(input_user, input_pwd) == True):
            return redirect('main')
        else:
            return abort(418)
            
    return render_template("authenticate.html")

@app.route('/main', methods = ['GET', 'POST'])
def main():
    if request.method == "POST":
        if (request.form['redirect'] == 'manual'):
            return redirect('manual')
        elif (request.form['redirect'] == 'ai'):
            return redirect('ai')
        else:
            pass
    return render_template("main_page.html")

@app.route('/manual', methods=['GET', 'POST'])
def manual():
    return render_template("manual.html")

@app.route('/ai', methods=['GET', 'POST'])
def ai():
    return render_template("ai.html")

@app.route('/endpage', methods = ['GET', 'POST'])
def endpage():
    return render_template('finish.html')

app.run()