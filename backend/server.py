from flask import Flask, render_template, session, redirect, url_for
from auth import auth_bp
from homepages import homepages_bp
from video import video_bp
from database import init_db

app = Flask(__name__, static_folder="../frontend/static", template_folder="../frontend/templates")
app.secret_key = 'your_secret_key'
app.register_blueprint(auth_bp)
app.register_blueprint(homepages_bp)
app.register_blueprint(video_bp)
init_db()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/account')
def account():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    elif session.get('role') == 'admin':
        return redirect(url_for('homepages.admin_home'))
    else:
        return redirect(url_for('homepages.user_home'))



if __name__ == '__main__':
    app.run(debug=True)
