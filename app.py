from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL configuration
db_config = {
    'host': 'localhost',     # Replace with your MySQL host (usually 'localhost')
    'user': 'root',     # Replace with your MySQL username
    'password': '', # Replace with your MySQL password
    'database': 'My_Academy' # Replace with the name of the database you created
}

# Function to create a connection to the MySQL database
def create_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

# Define a handler for the root URL
@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Student Records API!"

# Endpoint for creating a new student record
@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    dob = data['dob']
    amount_due = data['amount_due']

    connection = create_connection()
    cursor = connection.cursor()

    # Insert the new student record into the database
    insert_query = "INSERT INTO students (first_name, last_name, dob, amount_due) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (first_name, last_name, dob, amount_due))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify(message='Student record created successfully'), 201

# Endpoint for reading a specific student record by student_id
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    connection = create_connection()
    cursor = connection.cursor()

    # Retrieve the student record from the database
    select_query = "SELECT * FROM students WHERE student_id = %s"
    cursor.execute(select_query, (student_id,))
    student = cursor.fetchone()

    cursor.close()
    connection.close()

    if student:
        student_data = {
            'student_id': student[0],
            'first_name': student[1],
            'last_name': student[2],
            'dob': str(student[3]),
            'amount_due': float(student[4])
        }
        return jsonify(student_data), 200
    else:
        return jsonify(message='Student not found'), 404

# Endpoint for updating a student record by student_id
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    dob = data['dob']
    amount_due = data['amount_due']

    connection = create_connection()
    cursor = connection.cursor()

    # Update the student record in the database
    update_query = "UPDATE students SET first_name = %s, last_name = %s, dob = %s, amount_due = %s WHERE student_id = %s"
    cursor.execute(update_query, (first_name, last_name, dob, amount_due, student_id))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify(message='Student record updated successfully'), 200

# Endpoint for deleting a student record by student_id
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    connection = create_connection()
    cursor = connection.cursor()

    # Delete the student record from the database
    delete_query = "DELETE FROM students WHERE student_id = %s"
    cursor.execute(delete_query, (student_id,))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify(message='Student record deleted successfully'), 200

# Endpoint for showing all student records
@app.route('/students', methods=['GET'])
def get_all_students():
    connection = create_connection()
    cursor = connection.cursor()

    # Retrieve all student records from the database
    select_query = "SELECT * FROM students"
    cursor.execute(select_query)
    students = cursor.fetchall()

    cursor.close()
    connection.close()

    student_list = []
    for student in students:
        student_data = {
            'student_id': student[0],
            'first_name': student[1],
            'last_name': student[2],
            'dob': str(student[3]),
            'amount_due': float(student[4])
        }
        student_list.append(student_data)

    return jsonify(student_list), 200

if __name__ == '__main__':
    app.run(debug=True)
