from flask import Flask, jsonify
from flask_cors import CORS


import mysql.connector
app = Flask(__name__); 
CORS(app)

@app.route("/issues")
def get_issues():
    conn = mysql.connector.connect(user='root', password='password', host='localhost', port=3307, database='github')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM issues;")
    rows = cursor.fetchall()
    return jsonify([{"id": r[0], "title": r[1], "program_name": r[2]} for r in rows])
app.run(port=5000)