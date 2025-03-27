from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, JWTManager
import pymysql

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()

# Function to establish a database connection
def get_db_connection():
    try:
        return pymysql.connect(
            host="localhost",
            user="root",
            password="@Aditi123",  
            database="ppt_access_control",
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# User Registration API
@auth.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not name or not email or not password or not role:
        return jsonify({"error": "All fields (name, email, password, role) are required"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)", 
                       (name, email, hashed_password, role))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "User registered successfully!"}), 201
    except pymysql.MySQLError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

# User Login API
@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user and bcrypt.check_password_hash(user['password'], password):
            access_token = create_access_token(identity={"id": user['id'], "role": user['role']})
            return jsonify({"token": access_token, "role": user['role']})
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except pymysql.MySQLError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
