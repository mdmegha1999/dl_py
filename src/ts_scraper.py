"""_summary_

    Returns:
        _type_: _description_
"""
import os
import sys
import datetime

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

import xpaths_directory as xd
from logging_helper import get_logger
from errors import errors
from captcha_solver import solve_captcha
from utils import return_response, safe_execute, setup_chrome

load_dotenv()
url = os.getenv("TG")

logger = get_logger("driving_validation")


def ts_scraper_api(txnid, dlno, dob):
    """
    Returns the dl_validation_api function return value as API response.

            Parameters:
                    txnid: int
                    dlno: string
                    dob: string

            Returns:
                    value as API response
    """
    try:
        date, month, year = dob.split("-")
        try:
            datetime.datetime.strptime(date, "%d")  # Regex for the dob format
        except Exception:
            logger.error("%s => Invalid Date , %s", txnid, date)
            return return_response(errors["INVALID_REQUEST"])

        try:
            datetime.datetime.strptime(month, "%M")  # Regex for the dob format
        except Exception:
            logger.error("%s => Invalid Month , %s", txnid, month)
            return return_response(errors["INVALID_REQUEST"])

        try:
            datetime.datetime.strptime(year, "%Y")  # Regex for the dob format
        except Exception:
            logger.error("%s => Invalid Year , %s", txnid, year)
            return return_response(errors["INVALID_REQUEST"])

        driver = setup_chrome(url, txnid)

        Enter_License_No = '//*[@id="ctl00_OnlineContent_txtDlNo"]'
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, Enter_License_No))
        )
        driver.find_element(By.XPATH, Enter_License_No).send_keys(dlno)

        date1 = "/html/body/form/table[2]/tbody/tr[1]/td/div/table/tbody/tr[4]/td[2]/input[1]"
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, date1))
        )
        driver.find_element(By.XPATH, date1).send_keys(date)

        month1 = "/html/body/form/table[2]/tbody/tr[1]/td/div/table/tbody/tr[4]/td[2]/input[2]"
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, month1))
        )
        driver.find_element(By.XPATH, month1).send_keys(month)

        year1 = "/html/body/form/table[2]/tbody/tr[1]/td/div/table/tbody/tr[4]/td[2]/input[3]"
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, year1))
        )
        driver.find_element(By.XPATH, year1).send_keys(year)

        logger.info("%s Solving Captcha..", txnid)
        captcha_process = solve_captcha(
            driver, txnid, xd.TSCI, xd.TSCII, xd.TSCS, xd.TSVS, 5, logger
        )
        if captcha_process == False:
            driver.quit()
            return return_response(errors["INTERNAL_ERROR"])

        try:

            data_tbody = driver.find_element(By.XPATH,
                '//*[@id="ctl00_OnlineContent_gvLic"]/tbody'
            )
            trs = data_tbody.find_elements(By.TAG_NAME, "tr")
            ths = [
                key.text.lower().replace(" ", "_").replace("'", "")
                for key in trs[0].find_elements(By.TAG_NAME, "th")
            ]
            tds = [value.text for value in trs[1].find_elements(By.TAG_NAME, "td")]
            ws_data = dict(zip(ths, tds))
            data = {
                # Personal Details
                "name": safe_execute(ws_data["applicant_name"]),
                "dob": "",
                "cof": "",
                "address": "",
                "blood_group": "",
                "source_of_data": "",
                "rh_factor": "",
                # Card Details
                "current_status": "",
                "dl_no": safe_execute(ws_data["license_number"]),
                "old_dl_no": "",
                "card_serial_no": "",
                # Issuing detials
                "issue_date": "",
                "issuing_office": safe_execute(ws_data["office_name"]),
                # endorsment details
                "last_endorsed_date": "",
                "last_endorsed_office": "",
                "last_completed_transaction": "",
                # transport validity details
                "non_transport_validity": safe_execute(
                    ws_data["non_transport_validity"]
                ),
                "transport_validity": safe_execute(ws_data["transport_validity"]),
                # others
                "hazardous_valid_till": "",
                "hill_valid_till": "",
                # class of vehicle detials
                "class_of_vehicle_details": safe_execute(
                    ws_data["transport_class_of_vehicles"]
                ),
            }
            logger.info("%s => TS success transaction", txnid)
            driver.quit()
            return return_response(errors["SUCCESS"], data)
        except Exception:
            logger.error("%s DETAILS_FETCHING_FAILED : %s", txnid, sys.exc_info())
            return return_response(errors["DETAILS_FETCHING_FAILED"])

    except Exception:
        logger.error("Global Error  TS: %s", sys.exc_info())
        return return_response(errors["INTERNAL_ERROR"])
