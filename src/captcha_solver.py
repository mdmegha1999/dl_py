"""
Captcha solver - try to bypass the captcha steps

Functions:

    solve_captcha(txnid, dlno, dob) -> object

"""
import os
import base64
import random
import logging
from paddleocr import PaddleOCR

# Selenium Libraries
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# OCR Libraries
ocr = PaddleOCR(use_angle_cls=True, lang="en", use_gpu=False, show_log=False)


def init_logger(name: str) -> object:
    """
    Returns the logger object.

            Parameters:
                    name (str): string - file name

            Returns:
                    logger (object): return the logger object
    """
    os.makedirs("./captcha_logs", exist_ok=True)
    log = "./log/"
    logger = logging.getLogger(name)
    logger_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_handler = logging.FileHandler(f"{log+str(name)}.log")
    log_handler.setLevel(logging.INFO)
    log_handler.setFormatter(logging.Formatter(logger_format))
    logger.addHandler(log_handler)
    stream_h = logging.StreamHandler()
    stream_h.setLevel(logging.DEBUG)
    stream_h.setFormatter(logging.Formatter(logger_format))
    logger.addHandler(stream_h)
    logger.setLevel(logging.DEBUG)
    return logger


def _get_captcha(driver, captcha_image_xpath):
    """
    Returns the dl_validation_api function return value as API response.

            Parameters:
                    driver: object
            Returns:
                    value as API response
    """
    captcha_image = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.XPATH, captcha_image_xpath))
    )

    # get the captcha as a base64 string
    img_captcha_base64 = driver.execute_async_script(
        """
        var ele = arguments[0], callback = arguments[1];
        ele.addEventListener('load', function fn(){
        ele.removeEventListener('load', fn, false);
        var cnv = document.createElement('canvas');
        cnv.width = this.width; cnv.height = this.height;
        cnv.getContext('2d').drawImage(this, 0, 0);
        callback(cnv.toDataURL('image/jpeg').substring(22));
        }, false);
        ele.dispatchEvent(new Event('load'));
        """,
        captcha_image,
    )

    captcha_name = f"captcha_{random.randint(8000,10000)}.jpg"

    with open(captcha_name, "wb") as f:
        f.write(base64.b64decode(img_captcha_base64))

    try:
        captcha = ocr.ocr(captcha_name, cls=False)[0][1][0].replace(" ", "")
        os.remove(captcha_name)
        return captcha
    except Exception:
        os.remove(captcha_name)
        return None


def solve_captcha(
    driver,
    txnid,
    captcha_image_xpath,
    captcha_input_xpath,
    captcha_submit_xpath,
    validate_success_xpath,
    captcha_retries,
    logger=None,
):
    """_summary_

    Args:
        driver (object): _selenium webdriver_
        txnid (int): _transaction unique id_'
        captcha_image_xpath (string): _give xpath of captcha image in a string i.e., "your xpath"_
        captcha_input_xpath (string): _give xpath of input element where we need to enter captcha in string format_
        captcha_submit_xpath (string): _give xpath of submit button which we need to click after entering capatcha and all other required details_
        validate_success_xpath (string): _give xpath of some element to check if we successfully solved captcha and went to next step_
        log_file_name (string): _name of the log file where you want to write all your logs_
        captcha_retries (int): number of times captcha was retried before giving up

    Returns:
        _bool_: _if true it means we have solved the captcha else there is a failure case occured in captcha solving process_
    """
    if logger is None:
        logger = init_logger("captcha_solver")

    for i in range(0, int(captcha_retries)):
        # get captcha
        result = _get_captcha(driver, captcha_image_xpath)

        logger.info("%s %s captcha result : %s", txnid, i, result)

        if result is not None:
            captcha = result

            # find input captcha element
            # Enter input captcha XPATH here
            search = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.XPATH, captcha_input_xpath))
            )

            # Enter Captcha in the input box
            search.send_keys(str(captcha))
            # sleep(random.randint(5, 10))

            # Find send Submit button
            submit = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, captcha_submit_xpath))
            )  # //*
            # Click send OTP
            submit.click()
            # sleep(10)

        # try:
        #     error_data = WebDriverWait(driver, 1).until(
        #     EC.presence_of_element_located((By.XPATH,'/html/body/div[4]')))
        #     if error_data:
        #         logger.info(f'{txnid} => Invalid DOB or Driving_license_number')
        #         solved = True
        #         return False
        # except Exception:
        #     pass

        try:
            # Find Text to confirm we are redirected to next page and login successfully
            alert_success = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.XPATH, validate_success_xpath))
            )

            if alert_success:
                # logger.info('%s valid captcha: %s', txnid, captcha)
                return True
        except Exception:
            pass

    return False
