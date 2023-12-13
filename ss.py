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
    query = "INSERT INTO screenshot(text, attachment) VALUES (%s, %s)"   # Update the query
    cursor.execute(query, (user_text, attachment_path))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
