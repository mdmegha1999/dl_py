"""_summary_

Returns:
    _type_: _description_
"""
import sys
from selenium.webdriver.common.by import By


def get_values(driver):
    """_summary_

    Args:
        driver (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        dl_no = '//*[@id="ctl00_ContentPlaceHolder1_grvDrivingLicenseSummary"]/tbody/tr[2]/td[3]'
        dl_no_element = driver.find_element(By.XPATH, dl_no).text

        dl_name = '//*[@id="ctl00_ContentPlaceHolder1_grvDrivingLicenseSummary"]/tbody/tr[2]/td[4]'
        dl_name_element = driver.find_element(By.XPATH, dl_name).text

        dl_f_name = '//*[@id="ctl00_ContentPlaceHolder1_grvDrivingLicenseSummary"]/tbody/tr[2]/td[5]'
        dl_f_name_element = driver.find_element(By.XPATH, dl_f_name).text

        dl_dob = '//*[@id="ctl00_ContentPlaceHolder1_grvDrivingLicenseSummary"]/tbody/tr[2]/td[6]'
        dl_dob_element = driver.find_element(By.XPATH, dl_dob).text

        dl_validity_ntv = '//*[@id="ctl00_ContentPlaceHolder1_grvDrivingLicenseSummary"]/tbody/tr[2]/td[7]'
        dl_validity_ntv_element = driver.find_element(By.XPATH, dl_validity_ntv).text

        dl_validity_tv = '//*[@id="ctl00_ContentPlaceHolder1_grvDrivingLicenseSummary"]/tbody/tr[2]/td[8]'
        dl_validity_tv_element = driver.find_element(By.XPATH, dl_validity_tv).text

        dl_card_sr_no = '//*[@id="ctl00_ContentPlaceHolder1_grvDrivingLicenseSummary"]/tbody/tr[2]/td[9]'
        dl_card_sr_no_element = driver.find_element(By.XPATH, dl_card_sr_no).text

        dl_issued_on = '//*[@id="ctl00_ContentPlaceHolder1_grvDrivingLicenseSummary"]/tbody/tr[2]/td[10]'
        dl_issued_on_element = driver.find_element(By.XPATH, dl_issued_on).text

        dl_issuing_rto_name = '//*[@id="ctl00_ContentPlaceHolder1_pnlModel"]/table/tbody/tr[5]/td[2]/table/tbody/tr[5]/td[4]'
        dl_issuing_rto_name_element = driver.find_element(
            By.XPATH, dl_issuing_rto_name
        ).text

        blood_group_candidate = '//*[@id="ctl00_ContentPlaceHolder1_pnlModel"]/table/tbody/tr[5]/td[2]/table/tbody/tr[3]/td[8]'
        blood_group_candidate_element = driver.find_element(
            By.XPATH, blood_group_candidate
        ).text

        rh_factor_candidate = '//*[@id="ctl00_ContentPlaceHolder1_pnlModel"]/table/tbody/tr[5]/td[2]/table/tbody/tr[3]/td[8]'
        rh_factor_candidate_element = driver.find_element(
            By.XPATH, rh_factor_candidate
        ).text

        data = {
            # Personal Details
            "name": dl_name_element,
            "dob": dl_dob_element,
            "cof": dl_f_name_element,
            "address": "",
            "blood_group": blood_group_candidate_element,
            "source_of_data": "",
            "rh_factor": rh_factor_candidate_element,
            # Card Details
            "current_status": "",
            "dl_no": dl_no_element,
            "old_dl_no": "",
            "card_serial_no": dl_card_sr_no_element,
            # Issuing detials
            "issue_date": dl_issued_on_element,
            "issuing_office": dl_issuing_rto_name_element,
            # endorsment details
            "last_endorsed_date": "",
            "last_endorsed_office": "",
            "last_completed_transaction": "",
            # transport validity details
            "non_transport_validity": dl_validity_ntv_element,
            "transport_validity": dl_validity_tv_element,
            # others
            "hazardous_valid_till": "",
            "hill_valid_till": "",
            # class of vehicle detials
            "class_of_vehicle_details": "",
        }
        return data
    except Exception:
        print(sys.exc_info())
        return ""
