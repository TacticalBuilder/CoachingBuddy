# The Rowing Winter Training Progress Tracker. More radical than 6x2k!

# Python Driven, MongoDB supported, Flask Interfaced meter and roster attribute management system.
# MongoDB uses binary JSON Documents (BSON) to store data in a NoSQL manner. Needs Downloaded.
# Flask uses html/JS templates to render webpages with variable information (plus if, else, and for capability).
# Needs added to your python files. Requires the folders templates (for html) and statics (for css) in the program
# directory

# Major Objective: To Make a single tool that can be accessed by anyone with permission to store workouts,
#  calculate progress, track current and old rowers and their attributes, as well as show training progress

# Major To Dos:
#   - Add a Login that recognizes multiple passwords and can activate the Mongo database related to the login
#   - Figure out how to run this as/on a  network server so that it can be remotely accessed.
#   - Make the flask html templates render the relevant select tags with only the correct rower names
#   - Standardize the BSON file names and keys
from flask import *
from pymongo import MongoClient
from support import find_rower, find_by

# ~~~Flask interface set up~~~
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
app = Flask(__name__)
app.config.from_object(__name__)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~


# redirects to home - should be the login screen
@app.route('/', methods=['GET', 'POST'])
def start():
    return redirect(url_for('home'))


# brings up initial screen
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

# ~~~~~~~~ROWER MANAGEMENT PAGES~~~~~~~~~~~~~~~~~~
#  brings up the rower management screen for 'GET', Searches the rower collection of Mongo otherwise, rendering results
@app.route('/rowerHome')
def rowerhome():
    if request.form.get('method') == 'GET':
        return render_template('rowerhome.html')
    else:
        if request.form.get('arc') == 'y':
            keyword = request.form.get('search')
            keyword = keyword.split(' ')
            fname = keyword[0]
            lname = keyword[1]
            cursor = MongoClient().hampton.rowers.find({'name': {'first': fname, 'last': lname}})
            title = 'Matching Rowers'
            message = list()
            for doc in cursor:
                message.append(str(doc))
            return render_template('displayStats.html', name_title=title, rower_stats=message)
        else:
            return render_template('rowerhome.html')


# screen for changing rower information
@app.route('/rowerAddDrop')
def manage_rower():
    if request.method == 'GET':
        return render_template('rowerAddDrop.html', message='Welcome! Make updates to current rowers here')
    else:
        act = request.form.get('add_change')
        if act == 'add':
            bad = False
            fname = request.form.get('firname')
            lname = request.form.get('lasname')
            sex = request.form.get('gender')
            year = request.form.get('yeardes')
            height = 0
            weight = 0
            try:
                height = int(request.form.get('height'))
                weight = int(request.form.get('weight'))
            except TypeError:
                bad = True
            if fname is not None or fname != ' ' or fname != '':
                bad = True
            if lname is not None or lname != ' ' or lname != '':
                bad = True
            if sex is not None:
                bad = True
            if year is not None:
                bad = True
            if bad:
                return render_template('rowerAddDrop.html', message='Incomplete form, could not add rower')
            else:
                new_row = {'name': {'first': fname, 'last': lname}, 'height': height, 'weight': weight, 'gender': sex,
                           'team': 'novice', 'status': 'ACTIVE'}
                post = MongoClient().hampton.rowers.insert_one(new_row).inserted_id
                message = str(fname) + ' ' + str(lname) + ' successfully added to roster! Object @ ' + str(post)
                return render_template('rowerAddDrop.html', message=message)
        if act == 'change':
            rower = request.form.get('rower')
            rower = get_rower(rower)
            attrib = request.form.get('attrib')
            new_attrib = request.form.get('replacement')
            rowr = MongoClient().hampton.rowers.find('initl')
            if attrib is None or new_attrib is '' or rower is None:
                return


# ~~~~~~~~~~~~METER MANAGEMENT PAGES~~~~~~~~~~~~~~~
# meters home page
@app.route('/metersHome', methods=['GET', 'POST'])
def metershome():
    return render_template('meterHome.html')


# removes errant information for method 'POST' pulls up selection page for type 'GET'
@app.route('/meterRemoval', methods=['GET', 'POST'])
def meter_remove():
    if request.method == 'GET':
        obj_rem = request.form['Object_id']
        db = MongoClient().hampton.workouts
        if obj_rem is not None:
            db.remove({'_id': 'ObjectId(' + str(obj_rem) + ')'}, {'justOne': True})
        else:
            print('nothing to remove')
    else:
        obj_int = request.form.get('row_name')
        obj_date = request.form.get('piece_date')
        obj_date = timeconvert(obj_date)
        obj_time = request.form.get('piece_time')
        obj_time = obj_time.split(':')
        obj_tme = 0
        for x in range(0, len(obj_time) - 1):
            obj_tme += int(obj_time[x])
        obj_tme += float(obj_time[len(obj_time)])
        db = MongoClient().hampton.workspace
        curs = db.find({'time': obj_tme, 'date': obj_date, 'intial': obj_int})
        # WHAT DO WITH THE CURSOR

# adds a new workout to the MongoDB collection
@app.route('/materAdd', methods=['GET', 'POST'])
def meter_add():
    if request.method == 'POST':
        nmessage= request.form.get('new_message')

    else:
        return render_template('meterAdd.html', message='Welcome. Add a work out')
#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~PROGRESS MANAGEMENT PAGES~~~~~~~~~
# progress graph home pages
@app.route('/progressHome', methods=['GET', 'HOME'])
def progressHome():
    return render_template('progresshome.html')

# from here down is a mess rn 
@app.route('/stats', methods=['GET', 'POST'])
def getRower():
    looktyp = request.form.get('looktype')
    cursor = None
    title = None
    if looktyp == 'i':
        person = request.form.get('rower')
        person = get_rower(person)
        cursor = find_rower(person)
        title = 'Results for ' + str(person)
    if looktyp == 'f':
        gender = request.form.get('gender')
        teamdes = request.form.get('teamdes')
        weightdes = request.form.get('weightdes')
        yeardes = request.form.get('yeardes')
        cursor = find_by(gender, teamdes, weightdes, yeardes)
        title = 'Filtered Results'
    message = list()
    for doc in cursor:
        fname = doc["name"]["first"]
        lname = doc["name"]["last"]
        height = doc['height']
        weight = doc['weight']
        weightdes = doc['weightdes']
        year = doc['year']
        gender = doc['gender']
        team = doc['team']

        # startdate, enddate, pr list
        # create individual documents
        row_stats = 'rower: %s %s\nheight: %d\nweight: %d lbs\ngender: %s\n designations: %s, %s, %s', fname, lname,\
                    height, weight, gender, team, year, weightdes
    return render_template('displayStats.html', name_title=title, rower_stats=message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return None


@app.route('/meterAdd', methods=['GET', 'POST'])
def meterAdd():
    meth = request.form.get('method')
    if meth == 'post':
        mongo_serv = MongoClient()
        db = mongo_serv.hampton.training
        rower = request.form.get('rower')
        distance = request.form.get('dist')
        time = request.form.get('tim')
        split = request.form.get('split')
        date = request.form.get('piecedate')
        t_type = request.form.get('training')
        name = get_rower(rower)
        push = {"name": name, "distance": distance, "time": time, "split": split, "date": date, "type": t_type}
        post = db.insert_one(push).inserted_id
        render_template('meterAdd.html', message=('Training Piece Added!  DB Location: ' + str(post)))
    else:
        render_template('meterAdd.html', message='Add a workout to a rower\'s training files.')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


def timeconvert(time_string):
    return time_string


def get_rower(initials):
    if initials == 'CBL':
        return 'Conor Luksik'
    elif initials == 'TRV':
        return 'Trey Voelker'
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
if __name__ == '__main__':
    app.run()