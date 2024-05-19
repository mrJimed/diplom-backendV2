from flask import Flask
from flask_login import LoginManager

from controllers.history_controller import history_controller
from controllers.annotation_controller import annotation_controller
from controllers.user_controller import user_controller
from database import db
from db_models.user import User
from settings import SECRET_KEY, DB_CONNECTION

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONNECTION

app.register_blueprint(annotation_controller)
app.register_blueprint(user_controller)
app.register_blueprint(history_controller)

db.init_app(app)

login_manager = LoginManager()
login_manager.user_loader(lambda user_id: User.query.get(user_id))
login_manager.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5050)
