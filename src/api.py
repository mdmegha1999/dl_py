"""
Contains API endpoints / routing and their respective functionalities.

Functions:

    dl_validation() -> function call

"""
from flask import Flask, request
from flask_cors import CORS
from logging_helper import init_logger
from main import dl_validation_api


app = Flask(__name__)
cors = CORS(app)


logger = init_logger("driving_validation")


@app.route("/dl-validation", methods=["POST"])
def dl_validation():
    """
    Returns the dl_validation_api function return value as API response.

            Parameters:
                    None

            Returns:
                    Function Call return value as API response
    """
    logger.info("hit request dl validation")
    return dl_validation_api(request)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
