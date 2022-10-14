"""
For managing logs at one place.

Functions:

    dl_validation_api(object) -> object

"""
import sys
import datetime
from asyncio.log import logger
from flask import jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from logging_helper import get_logger


logger = get_logger("driving_validation")


def return_response(error_code, data=None):
    """
    Returns jsonified resonse with result as key and output as value.
    """
    error_code.update({"data": data})
    return jsonify(error_code)


def val_req_params(request):
    """
    Returns the dl_validation_api function return value as API response.

            Parameters:
                    request: object

            Returns:
                    bool
    """
    try:
        req = request.json
        logger.info("request : %s", req)

        dlno = req["dl_no"]
        dob = req["dob"]
        txnid = req["txnid"]

        datetime.datetime.strptime(dob, "%d-%M-%Y")
        if not len(dlno) in range(10, 19):
            return False

        return txnid, dlno, dob

    except Exception:
        logger.error("validating request params : %s", sys.exc_info())
        return False


def safe_execute(try_condition, default=""):
    """_summary_

    Args:
        default (_type_): _description_
        exception (_type_): _description_
        function (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        return try_condition
    except Exception:
        return default


def setup_chrome(url, txnid):
    """_summary_"""
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    logger.info("%s - intializing chrome", txnid)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get(url)
    logger.info("%s - opening website", txnid)
    driver.maximize_window()
    return driver
