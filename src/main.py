"""
For managing logs at one place.

Functions:

    dl_validation_api(object) -> object

"""
import sys
from ap_scraper import ap_scraper_api
from ts_scraper import ts_scraper_api
from mp_scraper import mp_scraper_api
from p_scraper import p_scraper_api
from logging_helper import get_logger
from utils import return_response, val_req_params
from errors import errors


logger = get_logger("driving_validation")


def dl_validation_api(request):
    """
    Returns the dl_validation_api function return value as API response.

            Parameters:
                    request: object

            Returns:
                    Function Call return value as API response
    """
    try:
        req_parsms = val_req_params(request)

        if req_parsms == False:
            return return_response(errors["INVALID_REQUEST"])

        txnid, dlno, dob = req_parsms
        if txnid == "" or dlno == "" or dob == "":
            return return_response(errors["INVALID_REQUEST"])

        try:
            if dlno[:2] == "AP":
                return ap_scraper_api(txnid, dlno)

            elif dlno[:2] == "TS":
                return ts_scraper_api(txnid, dlno, dob)

            elif dlno[:2] == "MP":
                return mp_scraper_api(txnid, dlno, dob)

            elif dlno[:3] == "DL-":
                return p_scraper_api(txnid, dlno, dob)

            elif dlno[:2] == "KA":
                return p_scraper_api(txnid, dlno, dob)
            else:
                return p_scraper_api(txnid, dlno, dob)
        except Exception:
            logger.error("%s - Website rounting : %s", txnid, sys.exc_info())
            return return_response(errors["INTERNAL_ERROR"])
    except Exception as ex:
        logger.error("Global Error : %s", ex)
        return return_response(errors["EMPTY_REQUEST_BODY"])
