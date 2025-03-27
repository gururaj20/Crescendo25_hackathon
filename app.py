from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from auth import auth

app = Flask(__name__)

# Configure Flask
app.config['JWT_SECRET_KEY'] ='00000'  
bcrypt = Bcrypt(app)  
jwt = JWTManager(app)  

# Register Blueprints
app.register_blueprint(auth, url_prefix='/auth')

@app.route('/')
def home():
    return "Welcome to the PPT Access Control System!"

if __name__ == '__main__':
    app.run(debug=True, port=5001)
