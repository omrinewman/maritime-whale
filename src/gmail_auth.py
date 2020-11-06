from func_timeout import func_timeout, FunctionTimedOut
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from log import *

import os.path
import pickle

LIMIT = 45 # authorization time limit (in seconds)
# if modifying these scopes, delete the file .token.pickle.
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.compose"
]

def gmail_auth(logfile):
    creds = None
    # the file .token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time
    if os.path.exists("../conf/.token.pickle"):
        with open("../conf/.token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            req_ret = None
            try:
                req_ret = func_timeout(LIMIT, Request)
            except FunctionTimedOut:
                log(logfile, "Request was not completed within " + str(LIMIT) +
                             " seconds.")
                exit(1)
            except Exception as e:
                log(logfile, "Something unexpected happened when trying to " +
                             "refresh Google credentials.")
                exit(1)
            creds.refresh(req_ret)
        else:
            flow = InstalledAppFlow.from_client_secrets_file("../conf/" +
                                                             "credentials.json",
                                                             SCOPES)
            creds = None
            try:
                creds = func_timeout(LIMIT, flow.run_local_server)
            except FunctionTimedOut:
                log(logfile, "Authorization was not completed within " +
                              str(LIMIT) + " seconds.")
                exit(1)
            except Exception as e:
                log(logfile, str(e))
                log(logfile, "Something unexpected happened when trying to " +
                             "load Google credentials.")
                exit(1)
        # save the credentials for the next run
        with open("../conf/.token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return creds