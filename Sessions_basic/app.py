from flask import *
app = Flask(__name__)
app.secret_key='Shinde Santhosh'

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/success', methods=['POST'])
def success():
    if request.method=='POST':
        session['email'] = request.form.get('email')
    return render_template('success.html')

@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email',None)
        return render_template('logout.html')
    else:
        return '<h3>User already Logged out</h3>'

@app.route("/profile")
def profile():
    if 'email' in session:
        email= session['email']
        return render_template('profile.html', name=email)
    else:
        return '<h3>Plz login first</h3>'
if __name__=="__main__":
    app.run(debug=True)
