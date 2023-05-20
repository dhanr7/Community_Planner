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

array_manual_constraints = {}
array_ai_constraints = {}

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
    array_manual_constraints.clear()
    if request.method == "POST":
        if (request.form['redirect'] == 'schedule_button'):
            if str(request.form.get("eventTypeLabel"))  != "Custom":
                array_manual_constraints.update({"Event Type": str(request.form.get("eventTypeLabel")), 
                                                "Event Name": str(request.form.get('event-name')), 
                                                "Event Date": datetime.datetime.strftime(datetime.datetime.strptime(str(request.form.get('event-date')), '%Y-%m-%d'), "%Y-%m-%d %H:%M:%S"), 
                                                "Event Start Time": datetime.datetime.strftime(datetime.datetime.strptime(str(request.form.get("event-start-time")), "%H:%M"), "%H:%M:%S"), 
                                                "Event End Time": datetime.datetime.strftime(datetime.datetime.strptime(str(request.form.get("event-end-time")), "%H:%M"), "%H:%M:%S"), 
                                                "Event Description": str(request.form.get("event-description")), 
                                                "Number of Participants": str(request.form.get("event-participants")), 
                                                "Participant Names": str(request.form.get("participant-names"))})
                print(array_manual_constraints)
                if (eventObject.checkIfEventBlocked(array_manual_constraints) == True):
                    return redirect('manual_error')

            elif str(request.form.get("eventTypeLabel"))  == "Custom":
               array_manual_constraints.update({"Event Type": str(request.form.get("customLabelText")), 
                                                "Event Name": str(request.form.get('event-name')), 
                                                "Event Date": datetime.datetime.strftime(datetime.datetime.strptime(str(request.form.get('event-date')), '%Y-%m-%d'), "%Y-%m-%d %H:%M:%S"), 
                                                "Event Start Time": datetime.datetime.strftime(datetime.datetime.strptime(str(request.form.get("event-start-time")), "%H:%M"), "%H:%M:%S"), 
                                                "Event End Time": datetime.datetime.strftime(datetime.datetime.strptime(str(request.form.get("event-end-time")), "%H:%M"), "%H:%M:%S"), 
                                                "Event Description": str(request.form.get("event-description")), 
                                                "Number of Participants": str(request.form.get("event-participants")), 
                                                "Participant Names": str(request.form.get("participant-names"))})
               print(array_manual_constraints)
               if (eventObject.checkIfEventBlocked(array_manual_constraints) == True):
                    return redirect('manual_error')
            else:
                pass
            return redirect('manual_confirm')
    return render_template("manual.html")

@app.route('/manual_error', methods=['GET', 'POST'])
def manual_error():
    if request.method == "POST":
        if request.form["redirect"] == "update_params":
            return redirect(url_for('manual'))
        elif request.form['redirect'] == "main_redirect":
            return redirect(url_for('main'))
    return render_template("manual_error.html")

@app.route('/ai', methods=['GET', 'POST'])
def ai():
    return render_template("ai.html")

@app.route('/manual_confirm', methods=['GET', 'POST'])
def manual_confirmation(): 
    if request.method == "POST":
        if (request.form['option'] == 'proceed_button'):
            eventObject.blockDate(array_manual_constraints)
            return redirect(url_for('main'))
        elif (request.form['option'] == 'change_params'):
            eventObject.unblockDate(array_manual_constraints["Event Date"])
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