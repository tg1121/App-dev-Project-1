from flask import Flask
from database import db

app = None

def create_app():
    app = Flask(__name__, static_folder='static')
    app.debug = True 
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    import os
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(os.path.join(os.path.dirname(__file__), 'instance'), 'lmsdata.db')
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()


from controllers import *

if __name__ == "__main__":
    db.create_all()
    app.run()