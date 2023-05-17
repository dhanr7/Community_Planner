from flask import *
import flask
import time
import users_class as users_class
import datetime
import appointment_scheduleManager_class as appClass

app = Flask(__name__)

admin = users_class.User("admin", "admin", "administrator")

eventObject = appClass.ScheduleManager()
eventObject.blockAllHolidayDates()

array_manual_constraints = []
array_ai_constraints = []

list_authentication_objects = [] #add all the objects and then later iterate through them to see if any user/pwd the user inputs matches any of these, if so authenticate and proceed.

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
            return abort(418) #abort(401) code
            
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
    if request.method == "POST":
        if (request.form['redirect'] == 'schedule_button'): #need to make customLabelText accurately get data & need to implement scheduleEvent class to add this date & time as blocked.
            #need to update scheduleEvents class to also handle timings as well for user scheduled "events" as well as storing name, description, etc.
            if str(request.form.get("eventTypeLabel") != "Custom"):
                array_manual_constraints.extend([("Event type: " + str(request.form.get("eventTypeLabel"))), ("Event name: " + str(request.form.get('event-name'))), ("Event date: " + str(request.form.get('event-date'))), ("Event start time: " + str(request.form.get("event-start-time"))), ("Event end time: " + str(request.form.get("event-end-time"))), ("Event Description: " + str(request.form.get("event-description"))), ("Number of Participants: " + str(request.form.get("event-participants"))), ("Participants attending: " + str(request.form.get("participant-names")))])
            elif str(request.form.get("eventTypeLabel") == "Custom"):
                array_manual_constraints.extend([("Event type: " + str(request.form.get("customLabelText"))), ("Event name: " + str(request.form.get('event-name'))), ("Event date: " + str(request.form.get('event-date'))), ("Event start time: " + str(request.form.get("event-start-time"))), ("Event end time: " + str(request.form.get("event-end-time"))), ("Event Description: " + str(request.form.get("event-description"))), ("Number of Participants: " + str(request.form.get("event-participants"))), ("Participants attending: " + str(request.form.get("participant-names")))])
            else:
                pass
            return redirect('manual_confirm')
    return render_template("manual.html")

@app.route('/ai', methods=['GET', 'POST'])
def ai():
    return render_template("ai.html")

@app.route('/manual_confirm', methods=['GET', 'POST'])
def manual_confirmation(): 
    if request.method == "POST":
        if (request.form['option'] == 'proceed_button'):
            return redirect(url_for('main'))
        elif (request.form['option'] == 'change_params'):
            return redirect(url_for('manual'))
        else:
            pass
    return render_template('manual_confirmation.html', array_manual_constraints=array_manual_constraints)

@app.route('/ai_confirm', methods=['GET', 'POST'])
def ai_confirmation():
    if request.method == "POST":
        if (request.form['option'] == 'proceed_button'):
            return redirect(url_for('main'))
        elif (request.form['option'] == 'change_params'):
            return redirect(url_for('ai'))
        else:
            pass
    return render_template("ai_confirmation.html")

app.run()