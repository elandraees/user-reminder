from flask import Flask, request, jsonify
from reminder.controllers.v1.reminder_controller import reminder_bp
from stripebilling.controller.stripe_controller import stripe_bp
from user.controllers.v1.user_controller import user_bp
from flask_cors import CORS, cross_origin

app = Flask(__name__)

app.register_blueprint(reminder_bp)
app.register_blueprint(user_bp)
app.register_blueprint(stripe_bp)


# Local deployment:
# If debug is disabled, the development server on the local computer can be made available to
# users on the network by setting the host name to ‘0.0.0.0’.
if __name__ == '__main__':
    app.run(debug=True)
