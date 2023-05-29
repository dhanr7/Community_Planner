from flask import *
import flask
import time
import users_class as users_class
import datetime
import appointment_scheduleManager_class as appClass
import os
import openai

#AI generate event description based on title, and generate title based on description, and (if possible, if time permits) multiple day event, ask AI to find the best times to break it down and what best to include in each

#make fullcalendar events look good without the hashes & extra datetime stuff
#admin have the power to override


app = Flask(__name__)

authenticator = users_class.User()
authenticator.addUser("admin", "admin", "administrator")
authenticator.addUser("student", "student", "student")

current_username = None

eventObject = appClass.ScheduleManager()
eventObject.blockAllHolidayDates()

array_manual_constraints = {}
array_ai_suggestions = {}

chosen_override_option_num = None
chosen_override_option_list = {}
new_override_option_list = {}

override_index = None

event_checkboxid_todelete = []

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        global current_username
        current_username = None
        if (request.form["login"] == "login"):
            return redirect('authenticate')
        elif (request.form["login"] == "new_user"):
            return redirect('new_user')
    return render_template("intro_login.html")

@app.route('/new_user', methods=["GET", "POST"])
def new_user_creation():
    if request.method == "POST":
        toVerifyAdminUser = str(request.form.get("admin_username"))
        toVerifyAdminPwd = str(request.form.get("admin_password"))
        if authenticator.checkIfUserExists(toVerifyAdminUser, toVerifyAdminPwd):
            print(str(request.form.get("username")), str(request.form.get("password")), str(request.form.get("typeClassifier")))
            authenticator.addUser(str(request.form.get("username")), str(request.form.get("password")), str(request.form.get("typeClassifier")))
            return redirect(url_for('index'))
        else:
            return abort(401, "Your administrator credentials were not verified or you are not authorized to create a new user at this time. Please try again.")
    return render_template("new_user.html")

@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    if request.method == "POST":
        input_user = request.form.get("username")
        input_pwd = request.form.get("password")
        if (authenticator.checkIfUserExists(input_user, input_pwd) == True):
            global current_username
            current_username = input_user
            print(authenticator.checkIfAdmin(input_user))
            return redirect('main')
        else:
            return abort(401)
    return render_template("authenticate.html")

@app.route('/main', methods = ['GET', 'POST'])
def main():
    with open("Community_Planner/event_dates.json", "r") as x:
        data = json.load(x)
    if request.method == "POST":
        if (request.form['redirect'] == 'manual'):
            return redirect('manual')
        elif (request.form['redirect'] == 'delete'):
            return redirect('delete')
        elif (request.form['redirect'] == 'override'):
            return redirect('override')
        else:
            pass
    return render_template("main_page.html", authenticator=authenticator, current_username=current_username, use_data = data)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    with open("Community_Planner/event_dates.json", "r+") as f:
        event_dates_data = json.load(f)
    f.close()
    if request.method == "POST":
        global event_checkboxid_todelete
        if len(event_checkboxid_todelete) > 0:
            event_checkboxid_todelete.clear()
        if (request.form['delete_button'] == 'delete_events_button'):
            event_checkboxid_todelete = request.form.getlist('event_input')
            event_checkboxid_todelete = [int(x) for x in event_checkboxid_todelete]
            print(event_checkboxid_todelete)
            with open("Community_Planner/event_dates.json", "r") as b:
                eD = json.load(b)
            for i, x in enumerate(eD):
                if (i in event_checkboxid_todelete):
                    print(i, x)
                    del eD[i]
            with open("Community_Planner/event_dates.json", "w") as b:
                json.dump(eD, b)
            b.close()
            return redirect('main')
        elif (request.form['delete_button'] == 'return_back'):
            return redirect('main')
    return render_template("delete.html", data=event_dates_data)

@app.route('/override', methods=['GET', 'POST'])
def override(): #main page to select what to override
    with open("Community_Planner/event_dates.json", "r+") as f:
        event_dates_data = json.load(f)
    f.close()
    if request.method == "POST":
        global chosen_override_option_num, chosen_override_option_list
        global override_index
        chosen_override_option_list.clear()
        if (request.form['override_button'] == 'override_events_button'):
            chosen_override_option_num = int(request.form.get('event_input'))
            print(chosen_override_option_num)
            with open('Community_Planner/event_dates.json', 'r') as q:
                eD = json.load(q)
            for i, x in enumerate(eD):
                if (int(i) == int(chosen_override_option_num)):
                    print(i, x)
                    chosen_override_option_list = eD[i]
                    override_index = i
            q.close()
            chosen_override_option_list['Event Date'] = datetime.datetime.strftime(datetime.datetime.strptime(chosen_override_option_list['Event Date'], '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d')
            print(chosen_override_option_list)
            return redirect('override_option')
        elif (request.form['override_button'] == 'return_back'):
            return redirect('main')
    return render_template('override.html', data=event_dates_data)

@app.route('/override_option', methods=['GET', 'POST'])
def override_option(): #page that gives the items to oveeride/allows for the admin to override and push it back to the JSON events file.
    new_override_option_list.clear()
    if request.method == "POST":
        if (request.form['redirect'] == 'override_button'):
            if (str(request.form.get("event-start-time")) == str(chosen_override_option_list['Event Start Time'])) and (str(request.form.get("event-end-time")) == str(chosen_override_option_list['Event End Time'])):
                new_override_option_list.update({
                    "Event Type": str(request.form.get("eventTypeLabel")),
                    "Event Name": str(request.form.get('event-name')),
                    "Event Date": datetime.datetime.strftime(datetime.datetime.strptime(str(request.form.get('event-date')), '%Y-%m-%d'), "%Y-%m-%d %H:%M:%S"), 
                    "Event Start Time": datetime.datetime.strftime(datetime.datetime.strptime(str(request.form.get("event-start-time")), "%H:%M:%S"), "%H:%M:%S"), 
                    "Event End Time": datetime.datetime.strftime(datetime.datetime.strptime(str(request.form.get("event-end-time")), "%H:%M:%S"), "%H:%M:%S"), 
                    "Event Description": str(request.form.get("event-description")), 
                    "Number of Participants": str(request.form.get("event-participants")), 
                    "Participant Names": str(request.form.get("participant-names"))
                })
            elif (str(request.form.get("event-start-time")) == str(chosen_override_option_list['Event Start Time'])):
                new_override_option_list.update({
                    "Event Type": str(request.form.get("eventTypeLabel")),
                    "Event Name": str(request.form.get('event-name')),
                    "Event Date": datetime.datetime.strftime(datetime.datetime.strptime(str(request.form.get('event-date')), '%Y-%m-%d'), "%Y-%m-%d %H:%M:%S"), 
                    "Event Start Time": datetime.datetime.strftime(datetime.datetime.strptime(str(request.form.get("event-start-time")), "%H:%M:%S"), "%H:%M:%S"), 
                    "Event End Time": datetime.datetime.strftime(datetime.datetime.strptime(str(request.form.get("event-end-time")), "%H:%M"), "%H:%M:%S"), 
                    "Event Description": str(request.form.get("event-description")), 
                    "Number of Participants": str(request.form.get("event-participants")), 
                    "Participant Names": str(request.form.get("participant-names"))
                })
            elif (str(request.form.get("event-end-time")) == str(chosen_override_option_list['Event End Time'])):
                new_override_option_list.update({
                    "Event Type": str(request.form.get("eventTypeLabel")),
                    "Event Name": str(request.form.get('event-name')),
                    "Event Date": datetime.datetime.strftime(datetime.datetime.strptime(str(request.form.get('event-date')), '%Y-%m-%d'), "%Y-%m-%d %H:%M:%S"), 
                    "Event Start Time": datetime.datetime.strftime(datetime.datetime.strptime(str(request.form.get("event-start-time")), "%H:%M"), "%H:%M:%S"), 
                    "Event End Time": datetime.datetime.strftime(datetime.datetime.strptime(str(request.form.get("event-end-time")), "%H:%M:%S"), "%H:%M:%S"), 
                    "Event Description": str(request.form.get("event-description")), 
                    "Number of Participants": str(request.form.get("event-participants")), 
                    "Participant Names": str(request.form.get("participant-names"))
                })
            else:
                new_override_option_list.update({
                    "Event Type": str(request.form.get("eventTypeLabel")),
                    "Event Name": str(request.form.get('event-name')),
                    "Event Date": datetime.datetime.strftime(datetime.datetime.strptime(str(request.form.get('event-date')), '%Y-%m-%d'), "%Y-%m-%d %H:%M:%S"), 
                    "Event Start Time": datetime.datetime.strftime(datetime.datetime.strptime(str(request.form.get("event-start-time")), "%H:%M"), "%H:%M:%S"), 
                    "Event End Time": datetime.datetime.strftime(datetime.datetime.strptime(str(request.form.get("event-end-time")), "%H:%M"), "%H:%M:%S"), 
                    "Event Description": str(request.form.get("event-description")), 
                    "Number of Participants": str(request.form.get("event-participants")), 
                    "Participant Names": str(request.form.get("participant-names"))
                })
            print(new_override_option_list)
            eventObject.overrideEvent(new_override_option_list, override_index)
            return redirect(url_for('main'))
    return render_template("override_option.html", chosen_override_list=chosen_override_option_list)

@app.route('/override_error', methods=['GET', 'POST'])
def override_error():
    if request.method == "POST":
        if request.form['redirect'] == 'update_params':
            return redirect('override_option')
        elif request.form['redirect'] == 'main_redirect':
            return redirect('main')
    return render_template('override_error.html')

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
                print(array_manual_constraints) #solely for debugging purposes
                if (eventObject.checkIfEventBlocked(array_manual_constraints) == True):
                    return redirect('manual_error') #make sure to add the description of the event that was already scheduled

            elif str(request.form.get("eventTypeLabel"))  == "Custom":
               array_manual_constraints.update({"Event Type": str(request.form.get("customLabelText")), 
                                                "Event Name": str(request.form.get('event-name')), 
                                                "Event Date": datetime.datetime.strftime(datetime.datetime.strptime(str(request.form.get('event-date')), '%Y-%m-%d'), "%Y-%m-%d %H:%M:%S"), 
                                                "Event Start Time": datetime.datetime.strftime(datetime.datetime.strptime(str(request.form.get("event-start-time")), "%H:%M"), "%H:%M:%S"), 
                                                "Event End Time": datetime.datetime.strftime(datetime.datetime.strptime(str(request.form.get("event-end-time")), "%H:%M"), "%H:%M:%S"), 
                                                "Event Description": str(request.form.get("event-description")), 
                                                "Number of Participants": str(request.form.get("event-participants")), 
                                                "Participant Names": str(request.form.get("participant-names"))})
               print(array_manual_constraints) #solely for debugging purposes
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

@app.route('/manual_confirm', methods=['GET', 'POST'])
def manual_confirmation(): 
    if request.method == "POST":
        if (request.form['option'] == 'proceed_button'):
            eventObject.blockDate(array_manual_constraints)
            return redirect(url_for('main'))
        elif (request.form['option'] == 'change_params'):
            eventObject.unblockDate(array_manual_constraints["Event Date"]) #update to reflect datetime object for "Event Date"
            return redirect(url_for('manual'))
        else:
            pass
    return render_template('manual_confirmation.html', array_manual_constraints=array_manual_constraints)

app.run()