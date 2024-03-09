from flask import Flask
from flask_login import LoginManager, UserMixin
from .dbconnect import connect_to_database

class User(UserMixin):
    def __init__(self,id,username,email):
        self.id=id
        self.user_name=username
        self.user_email = email

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "thisisasecretkehy"

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(username):
        connection = connect_to_database()
        cursor = connection.cursor()
        query = "SELECT * FROM auth WHERE username = %s"
        cursor.execute(query, (username,))
        user_data = cursor.fetchone()
        if user_data:
            return User(user_data[0],user_data[0],user_data[2])
        return None

    return app