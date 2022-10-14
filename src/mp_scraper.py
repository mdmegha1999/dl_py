"""
Contains API endpoints / routing and their respective functionalities.

Functions:

    mp_scraper_api() -> function call

"""
import os
import sys
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


from dotenv import load_dotenv

from errors import errors
from logging_helper import get_logger
import mp_paths
from get_values import get_values
from utils import return_response, setup_chrome

load_dotenv()

url = os.getenv("MP")

logger = get_logger("driving_validation")

# @app.route("/mpdl",methods=["POST"])
def mp_scraper_api(txnid, dlno, dob):
    """_summary_

    Args:
        txnid (_type_): _description_
        dlno (_type_): _description_
        dob (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        driver = setup_chrome(url, txnid)
        driving_no = '//*[@id="ctl00_ContentPlaceHolder1_txtDrivingLicense"]'
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, driving_no))
        )
        driver.find_element(By.XPATH, driving_no).send_keys(dlno)

        dob_no = '//*[@id="ctl00_ContentPlaceHolder1_txtDOB"]'
        driver.find_element(By.XPATH, dob_no).send_keys(dob)

        submit_bnt = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, mp_paths.submit))
        )  # //*
        submit_bnt.click()

        details_show_button = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.XPATH, mp_paths.show_details_button))
        )  # //*
        details_show_button.click()
        sleep(4)
        # print("3")

        data_table_body = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="ctl00_ContentPlaceHolder1_pnlModel"]/table/tbody/tr[5]/td[2]/table/tbody/tr[1]/td[4]',
                )
            )
        )
        print("4")
        if data_table_body:
            data = get_values(driver)
            if data == "":
                logger.error("%s details fecting failed : %s", txnid, sys.exc_info())
                return return_response(errors["DETAILS_FETCHING_FAILED"])
        logger.info("%s => MP success transaction", txnid)
        driver.quit()
        return return_response(errors["SUCCESS"], data)
    except Exception:
        logger.error("Global Error  MP: %s", sys.exc_info())
        # selenium.common.exceptions.TimeoutException:
        return return_response(errors["INTERNAL_ERROR"])
