#!/usr/bin/env python3

__author__ = "Girish Mallula"
__version__ = "0.1.0"
__license__ = "chandramgc@gmail.com"

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from datetime import datetime
from src.api.routes.api import router as api_router
from src.api.errors.http_error import http_error_handler
from src.api.errors.validation_error import http422_error_handler
from src.core.config import ALLOWED_HOSTS, API_PREFIX, DEBUG, PROJECT_NAME, VERSION

def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.include_router(api_router, prefix=API_PREFIX)

    return application

import sys, os
sys.path.append(os.getcwd())
app = get_application()

"""
def main(args):
    try:
        logger = setLogger('FASTAPI',args.log)

        # Beginning main application
        jobStartTime_dt = datetime.now()        
        logger.info("Job method started : " + jobStartTime_dt.strftime("%m/%d/%Y %I:%M:%S.%f %p"))

        # Current application
        customers = Customers()
        customers.app

        # Ending main application
        jobEndTime_dt = datetime.now()
        logger.info("Job method ended   : " + jobEndTime_dt.strftime("%m/%d/%Y %I:%M:%S.%f %p"))
        logger.info("Job duration       : " + str(int((jobEndTime_dt - jobStartTime_dt).total_seconds())) + " sec" )
    except:
        traceback.print_exc()

if __name__ == '__main__':
    print('Starting main application...')

    import sys, os
    sys.path.append(os.getcwd())

    # This is executed when run from the command line
    parser = argparse.ArgumentParser()

    # Optional argument which requires a parameter (eg. -l test)
    parser.add_argument("-l", "--log", action="store", dest="log", default="INFO")

    # Syntex for requires a parameter
    # parser.add_argument("--module", action="store", dest="module", default="sharepoint")

    args = parser.parse_args()
    main(args)

"""
        