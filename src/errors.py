"""
This module contains all the error responses to be sent
"""

errors = {
    "SUCCESS": {"respcode": 200, "respdesc": "success"},
    "EMPTY_REQUEST_BODY": {"respcode": 400, "respdesc": "bad request"},
    "INVALID_HEADERS": {"respcode": 400, "respdesc": "invalid headers"},
    "INVALID_REQUEST": {"respcode": 400, "respdesc": "invalid request"},
    "INTERNAL_ERROR": {"respcode": 502, "respdesc": "internal error occurred"},
    "DETAILS_NOT_FOUND": {"respcode": 502, "respdesc": "details not found"},
    "DETAILS_FETCHING_FAILED": {
        "respcode": 504,
        "respdesc": "details fetaching failed",
    },
    "PARSING_CONTENT_FAILED": {
        "respcode": 505,
        "respdesc": "offline aadhaar json conversion error",
    },
    "SERVER_BUSY": {"respcode": 506, "respdesc": "server busy"},
    "CONNECTION_ERROR": {"respcode": 502, "respdesc": "connection error"},
}
