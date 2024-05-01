from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
MYSQL_HOST = 'localhost'
MYSQL_USER = '60009220067'
MYSQL_PASSWORD = 'pass@123'
MYSQL_DB = 'Assistant'

# Create MySQL connection
db = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB
)

# Create table if not exists
def create_table():
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS assistants (
                     id INT AUTO_INCREMENT PRIMARY KEY,
                     name VARCHAR(255) NOT NULL,
                     mobile VARCHAR(20),
                     email VARCHAR(255),
                     salary DECIMAL(10, 2),
                     city VARCHAR(100),
                     country VARCHAR(100),
                     department VARCHAR(100),
                     role VARCHAR(100))''')
    db.commit()
    cursor.close()

@app.route('/', methods=["GET"])
def index():
    return render_template('index1.html')

# Create a new assistant
@app.route('/assistant', methods=['POST'])
def create_assistant():
    data = request.json
    name = data.get('name')
    mobile = data.get('mobile')
    email = data.get('email')
    salary = data.get('salary')
    city = data.get('city')
    country = data.get('country')
    department = data.get('department')
    role = data.get('role')

    if not name:
        return jsonify({'error': 'Name is required'}), 400

    cursor = db.cursor()
    cursor.execute('''INSERT INTO assistants (name, mobile, email, salary, city, country, department, role)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
                    (name, mobile, email, salary, city, country, department, role))
    db.commit()
    cursor.close()

    return jsonify({'id': cursor.lastrowid}), 201

# Get details of an assistant
@app.route('/assistant/<int:assistant_id>', methods=['GET'])
def get_assistant(assistant_id):
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM assistants WHERE id = %s''', (assistant_id,))
    assistant = cursor.fetchone()
    cursor.close()

    if not assistant:
        return jsonify({'error': 'Assistant not found'}), 404

    return jsonify({
        'id': assistant[0],
        'name': assistant[1],
        'mobile': assistant[2],
        'email': assistant[3],
        'salary': assistant[4],
        'city': assistant[5],
        'country': assistant[6],
        'department': assistant[7],
        'role': assistant[8]
    })

#Update an assistant
@app.route('/assistant/<int:assistant_id>', methods=['PUT'])
def update_assistant(assistant_id):
    try:
        data = request.json
        cursor = db.cursor()
        cursor.execute('''UPDATE assistants SET name=%s, mobile=%s, email=%s, salary=%s, city=%s, country=%s, department=%s, role=%s WHERE id=%s''', (data.get('name'), data.get('mobile'), data.get('email'), data.get('salary'),
                     data.get('city'), data.get('country'), data.get('department'), data.get('role'),
                        assistant_id))
        db.commit()
        cursor.close()

        return '', 204

    except Exception as e:
        # Log the error or return an error response
        return jsonify({'error': str(e)}), 500



# Delete an assistant
@app.route('/assistant/<int:assistant_id>', methods=['DELETE'])
def delete_assistant(assistant_id):
    cursor = db.cursor()
    cursor.execute('''DELETE FROM assistants WHERE id=%s''', (assistant_id,))
    db.commit()
    cursor.close()

    return '', 204

# Route to render create.html
@app.route('/create.html')
def create_page():
    return render_template('create.html')

# Route to render view.html
@app.route('/view.html')
def view_page():
    return render_template('view.html')

# Route to render update.html
@app.route('/update.html')
def update_page():
    return render_template('update.html')

# Route to render delete.html
@app.route('/delete.html')
def delete_page():
    return render_template('delete.html')

if __name__ == '__main__':
    app.run(debug=True)
