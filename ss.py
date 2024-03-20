from flask import Flask, render_template, request, redirect, url_for
import os
from flaskext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL()
mysql.init_app(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# MySQL Configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'muaz-testing'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get the text data from the form
    user_text = request.form['userText']
    
   # Handle logo upload
    logo_path = None
    logo = request.files.get('logo')
    if logo:
        logo_filename = os.path.join(app.config['UPLOAD_FOLDER'], logo.filename)
        logo.save(logo_filename)
        logo_path = logo_filename

    # Handle attachment
    attachment_path = None
    attachment = request.files.get('attachment')
    if attachment:
        attachment_filename = os.path.join(app.config['UPLOAD_FOLDER'], attachment.filename)
        attachment.save(attachment_filename)
        attachment_path = attachment_filename

    # Connect to the database and insert the text and attachment path data
    conn = mysql.connect()
    cursor = conn.cursor()
    query = "INSERT INTO uploads(text, attachment_path, logo_path) VALUES (%s, %s, %s)"
    cursor.execute(query, (user_text, attachment_path, logo_path))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(port=5001, debug=True)
