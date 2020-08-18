import form as form
import DB_Config
from flask import Flask
from flask import render_template, redirect, url_for,request,session,g

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'any secret string'
mongo = DB_Config.mongo

@app.before_request
def before_request():
    if 'user_id' in session:
        user = mongo.user.find_one({"id": session['user_id']})
        g.user = user

@app.route("/", methods =['GET', 'POST'])
def login():
    error = None
    session.pop('user_id', None)
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        users = mongo.user.find_one({"User_Email": username})
        if users == None:
            error = 'Invalid credentials'
            return render_template('login.html', title='Login', form=form, error=error)
        elif users['User_Email'] == username and users['Password'] == password:
            session['user_id']= users['id']
            return redirect(url_for('dashboard'))

    return render_template('login.html', title='Login', form=form)

@app.route("/dashboard")
def dashboard():

    technical = mongo.course.find({'Training_Id': "1"})
    domain = mongo.course.find({'Training_Id': "2"})
    learning_development = mongo.course.find({'Training_Id': "3"})
    return render_template('user.html', technical= technical,domain = domain, learning_development = learning_development)

@app.route("/logout", methods = ['GET', 'POST'])
def logout():
    session.clear()
    g.pop('user')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
