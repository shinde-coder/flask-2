from flask import *

app = Flask(__name__)

@app.route('/error')
def error():
    return "<strong>Enter Correct Password</strong>"

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/success', methods=['POST'])
def sucess():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('pass')


    if password == 'shinde':
        resp = make_response(render_template('success.html'))
        resp.set_cookie('email',email)
        return resp
    else:
        return redirect(url_for('error'))

@app.route('/profile')
def profile():
    email = request.cookies.get('email')
    #resp = make_response()
    return render_template('profile.html', name = email)

if __name__=='__main__':
    app.run(debug=True)

