import os
import pickle

# from .credentials import google_config

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# This is for airflow 1.10.4
from airflow.contrib.hooks.gcp_api_base_hook import GoogleCloudBaseHook

default_google_conn_id = 'google_cloud_default'

# def get_google_service_account_email():
#     """
#     Returns the service account email to share Drive files with.
#     """
#     return google_config['service-account']['client_email']

def initialize_credentials(conn_id=default_google_conn_id):
    """
    initialize_credentials: -> oauth2client.service_account.ServiceAccountCredentials

    Returns credentials that allows you to access your Google Drive &
    Sheets using the Google Sheets API.

    You still need to share spreadsheets with the service account email.
    """
    
    credentials = GoogleCloudBaseHook(conn_id)._get_credentials()

    # This prevents us from erroring out trying to construct credentials
    # from incomplete information.
#     service_account = google_config.get('service-account', {})
#     private_key = service_account.get('private_key', None)
#     if not private_key:
#         print(
#             "You're missing Google service account credentials",
#             "in credentials.py.",
#             "To access your Google Drive data,",
#             "fill out the Google service account information."
#         )
#         return None

#     credentials = ServiceAccountCredentials.from_json_keyfile_dict(
#         google_config['service-account'],
#         scopes=google_config['scopes'],
#     )
#     print(
#         'To access your Google Drive file, share the file with {email}'
#         .format(email=get_google_service_account_email())
#     )
#     return credentials
    return credentials

def create_drive(conn_id=default_google_conn_id, credentials=None):
    """
    create_engine:

    Sets up Google Drive API access using credentials (see above).
    """
    
    if credentials is None:
        credentials = initialize_credentials(conn_id)
    gauth = GoogleAuth()
    gauth.credentials = credentials
    drive = GoogleDrive(gauth)
    return drive

# Set up credentials
# credentials = initialize_credentials()

# This is a wrapper for pydrive.GoogleDrive
# GoogleDrive = None if credentials is None else create_client(credentials)
