# Weather_Tracker
A personal tool I'm putting together to connect to openweathermap.org and collect hourly weather data. 

Core tool is going to be designed to run in a google cloud function triggered off from an hourly pub/sub chronjob. 
The retrieved data will then be parsed and stored in a private GCS bucket. Utilizing cloud KMS for secret management.

Requirements:
GCP project with the following -
SA account set up with:
  Storage object creater
  Storage object viewer
  Cloud KMS Decrypt
GCS bucket with a folder with an encrypted copy of the .json key for the service account
more TBD
