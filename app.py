import os
import mysql.connector
import pandas as pd
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Database connection
mydb = mysql.connector.connect(
    host='192.168.105.33',
    port='3306',
    user='admin',
    password='root@123',
    database='student_performance'
)
mycursor = mydb.cursor()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file and file.filename.endswith('.csv'):
        current_directory = os.getcwd()
        file_path = os.path.join(current_directory, file.filename)
        file.save(file_path)
        try:
            insert_csv_to_db(file_path)
            os.remove(file_path)  # Clean up the saved file
            return jsonify({"message": "File successfully uploaded and data inserted"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "Allowed file type is csv"}), 400


def insert_csv_to_db(file_path):
    df = pd.read_csv(file_path)

    cursor = mycursor
    table_name = "student_performance"
    cols = ",".join([str(i) for i in df.columns.tolist()])

    for i, row in df.iterrows():
        sql = f"INSERT INTO {table_name} ({cols}) VALUES ({'%s, ' * (len(row) - 1)}%s)"
        cursor.execute(sql, tuple(row))

@app.route('/get', methods=['GET'])
def get_records():
    mycursor.execute("SELECT * FROM student_performance")
    result = mycursor.fetchall()
    records = []
    for row in result:
        record = {
            'id': row[0],
            'StudentName': row[1],
            'Gender': row[2],
            'Age': row[3],
            'GPA': row[4]
        }
        records.append(record)
    return jsonify(records)


@app.route('/update/<int:id>', methods=['PUT'])
def update_record(id):
    data = request.get_json()
    sql = "UPDATE student_performance SET StudentName=%s, Gender=%s, Age=%s,  GPA=%s WHERE id=%s"
    values = (data['StudentName'], data['Gender'], data['Age'], data['GPA'], id)
    mycursor.execute(sql, values)
    mydb.commit()
    return jsonify({'message': 'Record updated successfully'})


@app.route('/create', methods=['POST'])
def create_record():
    data = request.get_json()
    sql = "INSERT INTO student_performance (StudentName, Gender, Age,GPA) VALUES (%s, %s, %s, %s)"
    values = (data['StudentName'], data['Gender'], data['Age'], data['GPA'])
    mycursor.execute(sql, values)
    mydb.commit()
    return jsonify({'message': 'Record created successfully'})


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_record(id):
    sql = "DELETE FROM student_performance WHERE id=%s"
    mycursor.execute(sql, (id,))
    mydb.commit()
    return jsonify({'message': 'Record deleted successfully'})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
