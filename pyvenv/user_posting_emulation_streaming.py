import requests
from time import sleep
import random
import json
from sqlalchemy import text
from datetime import datetime
import boto3
from sqlalchemy import create_engine

random.seed(100)

class AWSDBConnector:
    def __init__(self):
        self.HOST = "pinterestdbreadonly.cq2e8zno855e.eu-west-1.rds.amazonaws.com"
        self.USER = 'project_user'
        self.PASSWORD = ':t%;yCY3Yjg'
        self.DATABASE = 'pinterest_data'
        self.PORT = 3306
        
    def create_db_connector(self):
        engine = create_engine(f"mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}?charset=utf8mb4")
        return engine

new_connector = AWSDBConnector()

def run_infinite_post_data_loop():
    while True:
        sleep(random.randrange(0, 2))
        random_row = random.randint(0, 11000)
        engine = new_connector.create_db_connector()

        with engine.connect() as connection:
            pin_string = text(f"SELECT * FROM pinterest_data LIMIT {random_row}, 1")
            pin_selected_row = connection.execute(pin_string)

            for row in pin_selected_row:
                pin_result = dict(row)
                
                invoke_url = "https://kdnbpq3ufb.execute-api.us-east-1.amazonaws.com/Pinetrest/Pinetrest/streams/stream_name/streaming-0abf7f0cd605-pin"
                
                payload = json.dumps({
                    "StreamName": "0abf7f0cd605-pin",
                    "Data": pin_result,
                    "PartitionKey": "desired-name"
                })

                headers = {'Content-Type': 'application/json'}
                response = requests.request("PUT", invoke_url, headers=headers, data=payload)
                print("pin", response.status_code)

            geo_string = text(f"SELECT * FROM geolocation_data LIMIT {random_row}, 1")
            geo_selected_row = connection.execute(geo_string)
            
            for row in geo_selected_row:
                geo_result = dict(row)
                invoke_url = "https://kdnbpq3ufb.execute-api.us-east-1.amazonaws.com/Pinetrest/Pinetrest/streams/stream_name/streaming-0abf7f0cd605-geo"
                
                payload = json.dumps({
                    "StreamName": "streaming-0abf7f0cd605-geo",
                    "Data": geo_result,
                    "PartitionKey": "desired-name"
                })

                headers = {'Content-Type': 'application/json'}
                response = requests.request("PUT", invoke_url, headers=headers, data=payload)
                print("geo", response.status_code)  

            user_string = text(f"SELECT * FROM user_data LIMIT {random_row}, 1")
            user_selected_row = connection.execute(user_string)
            
            for row in user_selected_row:
                user_result = dict(row)
                invoke_url = "https://kdnbpq3ufb.execute-api.us-east-1.amazonaws.com/Pinetrest/Pinetrest/streams/stream_name/streaming-0abf7f0cd605-user"
                
                payload = json.dumps({
                    "StreamName": "streaming-0abf7f0cd605-user",
                    "Data": user_result,
                    "PartitionKey": "desired-name"
                })

                headers = {'Content-Type': 'application/json'}
                response = requests.request("PUT", invoke_url, headers=headers, data=payload)
                print("user", response.status_code)   

if __name__ == "__main__":
    run_infinite_post_data_loop()
    print('Working')
