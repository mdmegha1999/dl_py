"""
Scraper function for parivahan website -selenium

Functions:

    p_scraper_api(txnid, dlno, dob) -> object

"""
import os
import sys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

from errors import errors
import xpaths_directory as xd
from captcha_solver import solve_captcha
from utils import return_response, safe_execute, setup_chrome
from logging_helper import get_logger

load_dotenv()

url = os.getenv("PARIVAHAN")


logger = get_logger("driving_validation")


def p_scraper_api(txnid, dlno, dob):
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
        driver = setup_chrome(url, txnid)
        driving_no = '//*[@id="form_rcdl:tf_dlNO"]'
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, driving_no))
        )
        driver.find_element(By.XPATH, driving_no).send_keys(dlno)

        dob_no = '//*[@id="form_rcdl:tf_dob_input"]'
        driver.find_element(By.XPATH, dob_no).send_keys(dob)

        logger.info("%s solving captcha", txnid)
        captcha_process = solve_captcha(
            driver, txnid, xd.PCI, xd.PCII, xd.PCS, xd.PVS, 5, logger
        )

        if captcha_process == False:
            driver.quit()
            return return_response(errors["INTERNAL_ERROR"])

        try:
            WebDriverWait(driver, 0).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/form/div[1]/div[3]/div[1]/div/div[2]/div[1]/div",
                    )
                )
            )
            logger.error("%s invalid captcha", txnid)
            return return_response(errors["INTERNAL_ERROR"])
        except Exception:
            pass
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="form_rcdl:pg_show"]/div/div/div',
                    )
                )
            )
        except TimeoutError:
            logger.error("%s website not loaded / data table not found", txnid)
            return return_response(errors["INTERNAL_ERROR"])

        ws_data = {}
        tables = driver.find_elements(By.TAG_NAME, "table")

        logger.info("%s No. of data tables found : %s", txnid, len(tables))

        for table in tables[:3]:
            trs = table.find_elements(By.TAG_NAME, "tr")
            for tr in trs:
                tds = tr.find_elements(By.TAG_NAME, "td")
                # Dictionary function
                ws_data.update(
                    {
                        tds[0]
                        .text.lower()
                        .replace("'", "")
                        .replace(" ", "_"): tds[1]
                        .text
                    }
                )

        trs2 = tables[3].find_elements(By.TAG_NAME, "tr")
        for tr2 in trs2:
            tds = tr2.find_elements(By.TAG_NAME, "td")
            ws_data.update(
                {
                    tds[0]
                    .text.lower()
                    .replace("'", "")
                    .replace(" ", "_"): f"{tds[1].text} - {tds[2].text}"
                }
            )

        trs4 = tables[4].find_elements(By.TAG_NAME, "tr")
        ws_data.update(
            {
                trs4[0]
                .find_elements(By.TAG_NAME, "td")[0]
                .text.lower()
                .replace("'", "")
                .replace(" ", "_"): trs4[0]
                .find_elements(By.TAG_NAME, "td")[1]
                .text
            }
        )
        ws_data.update(
            {
                trs4[0]
                .find_elements(By.TAG_NAME, "td")[2]
                .text.lower()
                .replace("'", "")
                .replace(" ", "_"): trs4[0]
                .find_elements(By.TAG_NAME, "td")[3]
                .text
            }
        )

        values = []
        table5 = tables[5].find_elements(By.TAG_NAME, "tr")

        for tr in table5[1:]:
            ths = [
                key.text.lower().replace(" ", "_").replace("'", "")
                for key in tables[5].find_elements(By.TAG_NAME, "th")
            ]
            tds = [value.text for value in tr.find_elements(By.TAG_NAME, "td")]
            # print(ths, tds)
            values.append(dict(zip(ths, tds)))

        ws_data.update({"clas_of_vehicle_details": values})
        from time import sleep

        sleep(10)

        data = {
            # Personal Details
            "name": safe_execute(ws_data["holders_name"]),
            "dob": "",
            "cof": "",
            "address": "",
            "blood_group": "",
            "source_of_data": safe_execute(ws_data["source_of_data"]),
            "rh_factor": "",
            # Card Details
            "current_status": safe_execute(ws_data["current_status"]),
            "dl_no": safe_execute(ws_data["old_/_new_dl_no."]),
            "old_dl_no": "",
            "card_serial_no": "",
            # Issuing detials
            "issue_date": safe_execute(ws_data["initial_issue_date"]),
            "issuing_office": safe_execute(ws_data["initial_issuing_office"]),
            # endorsment details
            "last_endorsed_date": safe_execute(ws_data["last_endorsed_date"]),
            "last_endorsed_office": safe_execute(ws_data["last_endorsed_office"]),
            "last_completed_transaction": safe_execute(
                ws_data["last_completed_transaction"]
            ),
            # transport validity details
            "non_transport_validity": safe_execute(ws_data["non-transport"]),
            "transport_validity": safe_execute(ws_data["transport"]),
            # others
            "hazardous_valid_till": safe_execute(ws_data["hazardous_valid_till"]),
            "hill_valid_till": safe_execute(ws_data["hill_valid_till"]),
            # class of vehicle detials
            "class_of_vehicle_details": safe_execute(
                ws_data["clas_of_vehicle_details"]
            ),
        }
        logger.info("%s parivahan success transaction", txnid)
        driver.quit()
        return return_response(errors["SUCCESS"], data)

    except Exception:
        logger.error("global error parivahan : %s", sys.exc_info())
        return return_response(errors["INTERNAL_ERROR"])