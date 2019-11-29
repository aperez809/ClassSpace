import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'ClassSpace.sqlite')
    )

    if not test_config:
        # If instance config exists and not in test mode, load from file
        app.config.from_pyfile('config.py', silent=True)

    else:
        # Otherwise load the test config
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello', methods=['GET'])
    def hello():
        return 'Hello, World'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import dashboard
    app.register_blueprint(dashboard.bp)
    app.add_url_rule('/', endpoint='dashboard')

    return app
