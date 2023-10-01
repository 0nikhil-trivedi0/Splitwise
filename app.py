import logging
from flask import Flask, jsonify

app = Flask(__name__)

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

from routes import user_route, expense_route
app.register_blueprint(user_route.user_routes, url_prefix='/api')
app.register_blueprint(expense_route.expense_routes, url_prefix='/api')

@app.errorhandler(400)
def bad_request_error(error):
    logger.error(f"Bad Request: {error}")
    return jsonify({"error": "Bad Request", "message": str(error)}), 400

@app.errorhandler(404)
def not_found_error(error):
    logger.error(f"Not Found: {error}")
    return jsonify({"error": "Not Found", "message": str(error)}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal Server Error: {error}")
    return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred"}), 500

if __name__ == "__main__":
    logger.info("Starting the application")
    app.run(debug=True)
