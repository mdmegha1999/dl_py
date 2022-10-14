"""_summary_

        Returns:
        _type_: _description_
"""
import sys
import os
# from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

import xpaths_directory as xd
from errors import errors
from captcha_solver import solve_captcha
from logging_helper import get_logger
from utils import return_response, safe_execute, setup_chrome

load_dotenv()

url = os.getenv("AP")

logger = get_logger("driving_validation")


def ap_scraper_api(txnid, dlno):
    """
    Returns the dl_validation_api function return value as API response.

            Parameters:
                    txnid: int
                    dlno: string

            Returns:
                    value as API response
    """
    try:
        driver = setup_chrome(url, txnid)
        select_action = '//*[@id="search"]'
        driver.find_element(By.XPATH, select_action).click()

        license_details = '//*[@id="search"]/option[3]'
        driver.find_element(By.XPATH, license_details).click()

        license_number = '//*[@id="licenseNo"]'
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, license_number))
        )
        driver.find_element(By.XPATH, license_number).send_keys(dlno)

        logger.info("%s solving captcha", txnid)
        captcha_process = solve_captcha(
            driver, txnid, xd.APCI, xd.APCII, xd.APCS, xd.APVS, 5, logger
        )
        if captcha_process == False:
            driver.quit()
            return return_response(errors["INTERNAL_ERROR"])

        try:

            path_view_complete_details = (
                "/html/body/div/div/div[3]/div/div/div[2]/div/table/tbody/tr/td[5]"
            )
            view_complete_details = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, path_view_complete_details))
            )  # //*
            # Click View Button
            view_complete_details.click()

            ws_data = {}
            tables = driver.find_elements(By.TAG_NAME, "table")

            logger.info(len(tables))

            for table in tables:
                trs = table.find_elements(By.TAG_NAME, "tr")
                for tr in trs:
                    try:
                        ws_data.update(
                            {
                                tr.find_element(By.TAG_NAME, "th")
                                .text.lower()
                                .replace(" ", "_"): tr.find_element(By.TAG_NAME, "td")
                                .text
                            }
                        )
                    except Exception:
                        pass
            logger.info("%s ap success transaction", txnid)
            data = {
                # Personal Details
                "name": safe_execute(ws_data["name"]),
                "dob": safe_execute(ws_data["date_of_birth"]),
                "cof": safe_execute(ws_data["son/wife/daughter_of"]),
                "address": safe_execute(ws_data["present_address"]),
                "blood_group": "",
                "source_of_data": "",
                "rh_factor": "",
                # Card Details
                "current_status": "",
                "dl_no": safe_execute(ws_data["dl_number"]),
                "old_dl_no": safe_execute(ws_data["old_dl_no"]),
                "card_serial_no": "",
                # Issuing detials
                "issue_date": safe_execute(ws_data["issued_date"]),
                "issuing_office": safe_execute(ws_data["office_code"]),
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
                "hazardous_valid_till": safe_execute(ws_data["hazardous_validity"]),
                "hill_valid_till": "",
                # class of vehicle detials
                "class_of_vehicle_details": "",
            }
            driver.quit()
            return return_response(errors["SUCCESS"], data)
        except Exception:
            logger.error("%s DETAILS_FETCHING_FAILED : %s", txnid, sys.exc_info())
            return return_response(errors["DETAILS_FETCHING_FAILED"])
    except Exception:
        logger.error("global error andhra pradesh : %s", sys.exc_info())
        return return_response(errors["INTERNAL_ERROR"])
