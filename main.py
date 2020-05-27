from google.cloud import storage
from google.cloud import secretmanager
import os
import json
import pytz
import datetime

def gcs_writer(blob_text):
    # Setting time and defining vars
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    est_now = utc_now.astimezone(pytz.timezone("America/Detroit"))
    formated_time = est_now.strftime('"%Y-%m-%d - %H:%M"')
    destination_blob_name = formated_time+"weather_tracking"
    bucket_name = os.environ.get('bucket_name')
    # Building client and writing the blob to bucket
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(blob_text)

def weather_call():
    import requests
    #setting vars
    project_id = os.environ.get('project_id')
    # getting secrets
    secrets = secretmanager.SecretManagerServiceClient()
    wkey = secrets.access_secret_version("projects/"+project_id+"/secrets/wtracker_api_key/versions/1").payload.data.decode("utf-8")
    # Define the call variables & construct api string
    weather_api_key = wkey
    zip_code = os.environ.get('zip_code')
    country_code = os.environ.get('country_code')
    api_call = "https://api.openweathermap.org/data/2.5/weather?zip="+zip_code+","+country_code+"&appid="+weather_api_key
    # create request
    response = requests.get(api_call)
    response_json = json.loads(response.text)
    exported_json = json.dumps(response_json)
    return(exported_json)

def main(data,context):
    # make the api call
    blob_text = weather_call()
    # write the string to the bucket
    gcs_writer(blob_text)
